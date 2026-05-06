from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .video import VideoInfo


@dataclass
class PlaylistInfo:
    title: str
    url: str
    videos: List[VideoInfo] = field(default_factory=list)

    @property
    def total_videos(self) -> int:
        return len(self.videos)
