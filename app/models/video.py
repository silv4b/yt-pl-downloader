from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class VideoInfo:
    title: str
    url: str
    uploader: Optional[str] = None
    duration: Optional[int] = None
    thumbnail: Optional[str] = None
