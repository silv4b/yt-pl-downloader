"""Serviço de download de playlist.

Baixa todos os vídeos de uma playlist do YouTube como MP4 ou MP3,
com duas barras de progresso: uma para o progresso geral da playlist
e outra para o vídeo atual sendo baixado.
"""

from __future__ import annotations

from app.core.utils import sanitize_filename
from app.exceptions import DownloadError, PlaylistExtractionError
from app.models.playlist import PlaylistInfo
from app.models.video import VideoInfo
from app.services.downloader import BaseDownloader


class PlaylistDownloader(BaseDownloader):
    """Baixa todos os vídeos de uma playlist do YouTube."""

    def download(self, url: str, is_audio: bool = False) -> PlaylistInfo:
        """Baixa uma playlist inteira da URL fornecida.

        Extrai metadados da playlist, itera por todos os vídeos e
        baixa cada um com nomes de arquivo numerados. Vídeos que
        falham ao baixar são ignorados sem interromper o processo.

        Duas barras de progresso são exibidas:
        - Geral: Progresso da playlist (vídeos completos / total)
        - Atual: Download do vídeo individual (bytes, velocidade, ETA)

        Args:
            url: URL da playlist do YouTube.
            is_audio: Se True, extrai áudio como MP3 para todos os vídeos.
                Se False, baixa como vídeo MP4.

        Returns:
            PlaylistInfo com título, URL e lista de vídeos baixados.

        Raises:
            PlaylistExtractionError: Se a playlist não contiver vídeos.
        """
        from app.cli.menu import create_playlist_progress

        info = self._extract_info(url)
        entries = info.get("entries")
        if not entries:
            raise PlaylistExtractionError("No videos found in playlist")

        playlist_title = sanitize_filename(info.get("title", "unknown_playlist"))
        output_dir = self.config.get_playlist_output_dir(playlist_title, is_audio)
        output_dir.mkdir(parents=True, exist_ok=True)

        videos = []
        total_videos = len([e for e in entries if e is not None])
        file_type = "audio" if is_audio else "video"

        with create_playlist_progress() as prog:
            overall_task = prog.add_task(
                f"[cyan]{playlist_title[:50]}",
                total=total_videos,
            )
            vid_task = prog.add_task(
                "",
                total=None,
                visible=False,
            )

            for index, video_info in enumerate(entries, start=1):
                if video_info is None:
                    continue

                video_title = sanitize_filename(video_info.get("title", f"video_{index}"))
                video_url = video_info.get("webpage_url") or video_info.get("url")
                if not video_url:
                    continue

                known_size = video_info.get("filesize") or video_info.get("filesize_approx") or 0

                video = VideoInfo(title=video_title, url=video_url)
                ydl_opts = self._get_ydl_options(output_dir, is_audio)
                ydl_opts["outtmpl"] = str(output_dir / f"{index:02d}_{video_title}.%(ext)s")

                def hook(d: dict, vt=video_title, ks=known_size) -> None:
                    """Atualiza as barras de progresso com o status do vídeo atual."""
                    if d.get("status") == "downloading":
                        downloaded = d.get("downloaded_bytes", 0)
                        total = d.get("total_bytes") or d.get("total_bytes_estimate") or ks
                        prog.update(
                            vid_task,
                            description=f"[dim]{file_type}: {vt[:40]}",
                            visible=True,
                            total=total if total and total > 0 else None,
                            completed=downloaded,
                        )
                    elif d.get("status") == "finished":
                        prog.update(vid_task, visible=False)

                ydl_opts["progress_hooks"] = [hook]

                try:
                    self._download(video_url, ydl_opts)
                    videos.append(video)
                    prog.advance(overall_task)
                except DownloadError:
                    continue

        return PlaylistInfo(title=playlist_title, url=url, videos=videos)
