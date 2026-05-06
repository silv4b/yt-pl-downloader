"""Serviço de download de vídeo individual.

Baixa um único vídeo do YouTube como MP4 ou extrai áudio como MP3,
com barra de progresso do Rich mostrando bytes, velocidade e tempo restante.
"""

from __future__ import annotations

from app.core.utils import sanitize_filename
from app.models.video import VideoInfo
from app.services.downloader import BaseDownloader


class VideoDownloader(BaseDownloader):
    """Baixa um único vídeo ou faixa de áudio do YouTube."""

    def download(self, url: str, is_audio: bool = False) -> VideoInfo:
        """Baixa um único vídeo da URL fornecida.

        Extrai metadados, cria o diretório de saída e baixa o arquivo
        com uma barra de progresso do Rich mostrando velocidade,
        bytes transferidos e tempo estimado restante.

        Args:
            url: URL do vídeo do YouTube.
            is_audio: Se True, extrai áudio como MP3.
                Se False, baixa como vídeo MP4.

        Returns:
            VideoInfo com título, URL, uploader e duração.
        """
        from app.cli.menu import create_progress

        info = self._extract_info(url)
        title = sanitize_filename(info.get("title", "unknown"))

        total_bytes = info.get("filesize") or info.get("filesize_approx") or 0

        video = VideoInfo(
            title=title,
            url=url,
            uploader=info.get("uploader"),
            duration=info.get("duration"),
        )
        output_dir = self.config.get_video_output_dir(title, is_audio)
        output_dir.mkdir(parents=True, exist_ok=True)
        file_type = "audio" if is_audio else "video"

        def make_hook(progress, task_id, known_total):
            """Cria um hook de progresso que atualiza a barra do Rich."""

            def _hook(d: dict) -> None:
                if d.get("status") == "downloading":
                    downloaded = d.get("downloaded_bytes", 0)
                    total = d.get("total_bytes") or d.get("total_bytes_estimate") or known_total
                    if total and total > 0:
                        progress.update(task_id, total=total, completed=downloaded)

            return _hook

        with create_progress() as prog:
            task = prog.add_task(
                f"[cyan]{file_type}: {title[:50]}",
                total=total_bytes if total_bytes > 0 else None,
            )
            ydl_opts = self._get_ydl_options(output_dir, is_audio, make_hook(prog, task, total_bytes))
            self._download(url, ydl_opts)

        return video
