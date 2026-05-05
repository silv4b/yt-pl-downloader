from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Any

import yt_dlp

from app.core.config import DownloadConfig
from app.exceptions import DownloadError, InvalidURLError

if TYPE_CHECKING:
    pass


class BaseDownloader(ABC):
    def __init__(self, config: DownloadConfig | None = None) -> None:
        self.config = config or DownloadConfig()
        self.config.ensure_dirs()

    def _extract_info(self, url: str, download: bool = False) -> Any:
        try:
            with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
                return ydl.extract_info(url, download=download)
        except yt_dlp.utils.DownloadError as e:
            raise InvalidURLError(f"Failed to extract info from URL: {e}") from e

    def _get_ydl_options(
        self, output_path: Path, is_audio: bool = False
    ) -> dict[str, Any]:
        if is_audio:
            return {
                "format": "bestaudio/best",
                "outtmpl": str(output_path / "%(title)s.%(ext)s"),
                "quiet": False,
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": self.config.audio_quality,
                    }
                ],
                "extractaudio": True,
            }
        else:
            return {
                "format": "best[ext=mp4]/bestvideo+bestaudio/best",
                "merge_output_format": "mp4",
                "outtmpl": str(output_path / "%(title)s.%(ext)s"),
                "quiet": False,
                "postprocessors": [
                    {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
                ],
            }

    def _download(self, url: str, ydl_opts: dict[str, Any]) -> None:
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except yt_dlp.utils.DownloadError as e:
            raise DownloadError(f"Download failed: {e}") from e

    @abstractmethod
    def download(self, url: str, is_audio: bool = False) -> Any: ...
