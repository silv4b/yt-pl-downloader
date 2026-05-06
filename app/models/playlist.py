"""Modelo de metadados de playlist."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .video import VideoInfo


@dataclass
class PlaylistInfo:
    """Metadados de uma playlist do YouTube.

    Attributes:
        title: Título sanitizado da playlist.
        url: URL original do YouTube da playlist.
        videos: Lista de objetos VideoInfo para cada vídeo baixado.
    """

    title: str
    url: str
    videos: List[VideoInfo] = field(default_factory=list)

    @property
    def total_videos(self) -> int:
        """Retorna a quantidade de vídeos baixados com sucesso."""
        return len(self.videos)
