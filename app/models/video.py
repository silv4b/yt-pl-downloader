"""Modelos de dados para metadados de vídeo e playlist."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class VideoInfo:
    """Metadados de um único vídeo.

    Attributes:
        title: Título sanitizado do vídeo.
        url: URL original do YouTube do vídeo.
        uploader: Canal ou usuário que enviou o vídeo.
        duration: Duração do vídeo em segundos.
        thumbnail: URL da imagem em miniatura do vídeo.
    """

    title: str
    url: str
    uploader: Optional[str] = None
    duration: Optional[int] = None
    thumbnail: Optional[str] = None
