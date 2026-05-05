from __future__ import annotations


class DownloadError(Exception):
    """Base exception for all download-related errors."""


class FFmpegNotFoundError(DownloadError):
    """Raised when FFmpeg is not found on the system."""


class FFmpegInstallError(DownloadError):
    """Raised when FFmpeg installation fails."""


class InvalidURLError(DownloadError):
    """Raised when the provided URL is invalid."""


class PlaylistExtractionError(DownloadError):
    """Raised when playlist metadata cannot be extracted."""


__all__ = [
    "DownloadError",
    "FFmpegInstallError",
    "FFmpegNotFoundError",
    "InvalidURLError",
    "PlaylistExtractionError",
]
