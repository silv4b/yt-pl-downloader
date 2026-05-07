"""Serviço de download de playlist.

Baixa todos os vídeos de uma playlist do YouTube como MP4 ou MP3.
"""

from __future__ import annotations

from app.core.utils import sanitize_filename
from app.exceptions import DownloadError, PlaylistExtractionError
from app.models.playlist import PlaylistInfo
from app.models.video import VideoInfo
from app.services.downloader import BaseDownloader


class PlaylistDownloader(BaseDownloader):
    """Baixa vídeos de uma playlist do YouTube."""

    def extract_info(self, url: str) -> dict:
        """Extrai metadados da playlist sem baixar.

        Args:
            url: URL da playlist do YouTube.

        Returns:
            Dicionário de metadados do yt-dlp.
        """
        return self._extract_info(url)

    def download(
        self,
        url: str,
        is_audio: bool = False,
        quality: str | None = None,
    ) -> PlaylistInfo:
        """Baixa uma playlist inteira da URL fornecida.

        Extrai metadados da playlist, itera por todos os vídeos e
        baixa cada um com nomes de arquivo numerados. Vídeos que
        falham ao baixar são ignorados sem interromper o processo.

        Args:
            url: URL da playlist do YouTube.
            is_audio: Se True, extrai áudio como MP3 para todos os vídeos.
                Se False, baixa como vídeo MP4.
            quality: Filtro de formato do yt-dlp para qualidade específica.
                Se None, usa o melhor formato disponível.

        Returns:
            PlaylistInfo com título, URL e lista de vídeos baixados.

        Raises:
            PlaylistExtractionError: Se a playlist não contiver vídeos.
        """
        info = self._extract_info(url)
        entries = info.get("entries")
        if not entries:
            raise PlaylistExtractionError("Nenhum vídeo encontrado na playlist")

        playlist_title = sanitize_filename(info.get("title", "unknown_playlist"))
        output_dir = self.config.get_playlist_output_dir(playlist_title, is_audio)
        output_dir.mkdir(parents=True, exist_ok=True)

        videos = []

        for index, video_info in enumerate(entries, start=1):
            if video_info is None:
                continue

            video_title = sanitize_filename(video_info.get("title", f"video_{index}"))
            video_url = video_info.get("webpage_url") or video_info.get("url")
            if not video_url:
                continue

            video = VideoInfo(title=video_title, url=video_url)

            ydl_opts = self._get_ydl_options(output_dir, is_audio, quality=quality)
            ydl_opts["outtmpl"] = str(output_dir / f"{index:02d}_{video_title}.%(ext)s")

            try:
                self._download(video_url, ydl_opts)
                videos.append(video)
            except DownloadError:
                continue

        return PlaylistInfo(title=playlist_title, url=url, videos=videos)
