from __future__ import annotations

from app.core.logger import logger
from app.core.utils import sanitize_filename
from app.models.video import VideoInfo
from app.services.downloader import BaseDownloader


class VideoDownloader(BaseDownloader):
    def download(self, url: str, is_audio: bool = False) -> VideoInfo:
        logger.info("Extracting video information...")
        info = self._extract_info(url)

        title = sanitize_filename(info.get("title", "unknown"))
        video = VideoInfo(
            title=title,
            url=url,
            uploader=info.get("uploader"),
            duration=info.get("duration"),
        )

        output_dir = self.config.get_video_output_dir(title, is_audio)
        output_dir.mkdir(parents=True, exist_ok=True)

        ydl_opts = self._get_ydl_options(output_dir, is_audio)

        file_type = "audio" if is_audio else "video"
        logger.info("Downloading %s: %s", file_type, title)

        self._download(url, ydl_opts)

        logger.info("Download completed: %s", title)
        return video
