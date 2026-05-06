"""Exceções customizadas para erros relacionados a downloads.

Todas as exceções herdam de DownloadError para permitir
capturar qualquer falha de download com um único bloco except.
"""

from __future__ import annotations


class DownloadError(Exception):
    """Exceção base para todos os erros relacionados a downloads."""


class FFmpegNotFoundError(DownloadError):
    """Lançada quando o FFmpeg não é encontrado no sistema e é necessário."""


class FFmpegInstallError(DownloadError):
    """Lançada quando a instalação automática do FFmpeg falha."""


class InvalidURLError(DownloadError):
    """Lançada quando a URL fornecida é inválida ou inacessível."""


class PlaylistExtractionError(DownloadError):
    """Lançada quando os metadados da playlist não podem ser extraídos da URL."""


__all__ = [
    "DownloadError",
    "FFmpegInstallError",
    "FFmpegNotFoundError",
    "InvalidURLError",
    "PlaylistExtractionError",
]
