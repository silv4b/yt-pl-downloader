"""Classe base para operações de download do YouTube.

Fornece funcionalidade compartilhada para extração de metadados,
construção de opções do yt-dlp e execução de downloads com
relatório de progresso através de hooks.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol

import yt_dlp

from app.core.config import DownloadConfig
from app.exceptions import DownloadError, InvalidURLError


class ProgressHook(Protocol):
    """Protocolo para funções que recebem atualizações de progresso do yt-dlp."""

    def __call__(self, status: dict[str, Any], /) -> None: ...


class SilentLogger:
    """Suprime toda saída de log do yt-dlp para manter o terminal limpo.

    Usado junto com barras de progresso do Rich para evitar
    que mensagens de log se misturem com a exibição de progresso.
    """

    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass


class BaseDownloader:
    """Classe base para downloaders do YouTube.

    Gerencia configuração, criação de diretórios, extração de metadados,
    construção de opções do yt-dlp e execução de downloads.
    """

    def __init__(self, config: DownloadConfig | None = None) -> None:
        """Inicializa o downloader com a configuração fornecida.

        Args:
            config: Instância de DownloadConfig. Cria uma padrão se não for fornecida.
        """
        self.config = config or DownloadConfig()
        self.config.ensure_dirs()

    def _extract_info(self, url: str, download: bool = False) -> Any:
        """Extrai metadados de vídeo ou playlist de uma URL do YouTube.

        Args:
            url: URL do vídeo ou playlist do YouTube.
            download: Se True, também baixa a mídia (padrão: apenas metadados).

        Returns:
            Dicionário contendo metadados extraídos pelo yt-dlp.

        Raises:
            InvalidURLError: Se a URL for inválida ou inacessível.
        """
        try:
            opts = {"quiet": True, "no_warnings": True, "logger": SilentLogger()}
            with yt_dlp.YoutubeDL(opts) as ydl:
                return ydl.extract_info(url, download=download)
        except yt_dlp.utils.DownloadError as e:
            raise InvalidURLError(f"Failed to extract info from URL: {e}") from e

    def _get_ydl_options(
        self,
        output_path: Path,
        is_audio: bool = False,
        progress_hook: ProgressHook | None = None,
        quality: str | None = None,
    ) -> dict[str, Any]:
        """Constrói o dicionário de configuração do yt-dlp para o tipo de download.

        Args:
            output_path: Diretório onde o arquivo baixado será salvo.
            is_audio: Se True, configura extração de áudio para MP3.
                Se False, configura download de vídeo como MP4.
            progress_hook: Função de callback opcional para atualizações de progresso.
            quality: Filtro de formato do yt-dlp para qualidade específica.
                Ex: "bestvideo[height<=1080]+bestaudio/best".
                Se None, usa o melhor formato disponível.

        Returns:
            Dicionário de opções do yt-dlp pronto para uso.
        """
        base_opts: dict[str, Any] = {
            "quiet": True,
            "no_warnings": True,
            "logger": SilentLogger(),
        }
        if progress_hook:
            base_opts["progress_hooks"] = [progress_hook]

        if is_audio:
            return {
                **base_opts,
                "format": "bestaudio/best",
                "outtmpl": str(output_path / "%(title)s.%(ext)s"),
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": self.config.audio_quality,
                    }
                ],
                "extractaudio": True,
            }

        video_format = quality or "best[ext=mp4]/bestvideo+bestaudio/best"
        return {
            **base_opts,
            "format": f"{video_format}[vcodec^=avc1]/bestvideo[vcodec^=avc1]+bestaudio/best[ext=mp4]/best",
            "merge_output_format": "mp4",
            "outtmpl": str(output_path / "%(title)s.%(ext)s"),
        }

    def _download(self, url: str, ydl_opts: dict[str, Any]) -> None:
        """Executa o download usando yt-dlp com as opções fornecidas.

        Args:
            url: URL do YouTube para baixar.
            ydl_opts: Dicionário de configuração do _get_ydl_options().

        Raises:
            DownloadError: Se o download falhar.
        """
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except yt_dlp.utils.DownloadError as e:
            raise DownloadError(f"Download failed: {e}") from e
