from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Protocol

import yt_dlp

from app.core.config import DownloadConfig
from app.exceptions import DownloadError, InvalidURLError


class ProgressHook(Protocol):
    def __call__(self, status: dict[str, Any], /) -> None: ...


class SilentLogger:
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass


class BaseDownloader(ABC):
    def __init__(self, config: DownloadConfig | None = None) -> None:
        self.config = config or DownloadConfig()
        self.config.ensure_dirs()

    def _extract_info(self, url: str, download: bool = False) -> Any:
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
    ) -> dict[str, Any]:
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
        else:
            return {
                **base_opts,
                "format": "best[ext=mp4]/bestvideo+bestaudio/best",
                "merge_output_format": "mp4",
                "outtmpl": str(output_path / "%(title)s.%(ext)s"),
                "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
            }

    def _download(self, url: str, ydl_opts: dict[str, Any]) -> None:
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except yt_dlp.utils.DownloadError as e:
            raise DownloadError(f"Download failed: {e}") from e

    @abstractmethod
    def download(self, url: str, is_audio: bool = False) -> Any: ...
