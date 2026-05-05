from __future__ import annotations
from app.core.logger import logger
from app.core.utils import sanitize_filename
from app.exceptions import DownloadError, PlaylistExtractionError
from app.models.playlist import PlaylistInfo
from app.models.video import VideoInfo
from app.services.downloader import BaseDownloader


class PlaylistDownloader(BaseDownloader):
    def download(self, url: str, is_audio: bool = False) -> PlaylistInfo:
        logger.info("Extracting playlist information...")
        info = self._extract_info(url)

        entries = info.get("entries")
        if not entries:
            raise PlaylistExtractionError("No videos found in playlist")

        playlist_title = sanitize_filename(info.get("title", "unknown_playlist"))
        output_dir = self.config.get_playlist_output_dir(playlist_title, is_audio)
        output_dir.mkdir(parents=True, exist_ok=True)

        videos = []
        total = len([e for e in entries if e is not None])

        ydl_opts = self._get_ydl_options(output_dir, is_audio)

        for index, video_info in enumerate(entries, start=1):
            if video_info is None:
                logger.warning("Skipping unavailable video at position %d", index)
                continue

            video_title = sanitize_filename(video_info.get("title", f"video_{index}"))
            video_url = video_info.get("webpage_url") or video_info.get("url")

            if not video_url:
                logger.warning("No URL found for video %d, skipping", index)
                continue

            video = VideoInfo(
                title=video_title,
                url=video_url,
            )

            ydl_opts["outtmpl"] = str(output_dir / f"{index:02d}_{video_title}.%(ext)s")

            file_type = "audio" if is_audio else "video"
            logger.info(
                "[%d/%d] Downloading %s: %s", index, total, file_type, video_title
            )

            try:
                self._download(video_url, ydl_opts)
                videos.append(video)
                logger.info("[%d/%d] Completed: %s", index, total, video_title)
            except DownloadError as e:
                logger.error(
                    "[%d/%d] Failed to download %s: %s", index, total, video_title, e
                )
                continue

        logger.info(
            "Playlist download completed: %s (%d/%d videos)",
            playlist_title,
            len(videos),
            total,
        )
        return PlaylistInfo(title=playlist_title, url=url, videos=videos)
