from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

_DEFAULTS = {
    "downloads_dir": "downloads",
    "video_subdir": "downloaded_videos",
    "playlist_subdir": "downloaded_playlists",
    "default_video_format": "mp4",
    "default_audio_format": "mp3",
    "audio_quality": "192",
}


def _find_config_path() -> Path:
    for base in [Path(__file__).parent.parent.parent, Path.cwd()]:
        path = base / "config.yaml"
        if path.exists():
            return path
    return Path.cwd() / "config.yaml"


def _load_config() -> dict:
    config_path = _find_config_path()
    if not config_path.exists():
        return dict(_DEFAULTS)
    with open(config_path, encoding="utf-8") as f:
        loaded = yaml.safe_load(f) or {}
    return {**_DEFAULTS, **loaded}


@dataclass(frozen=True)
class DownloadConfig:
    base_dir: Path = Path(_DEFAULTS["downloads_dir"])
    video_subdir: str = _DEFAULTS["video_subdir"]
    playlist_subdir: str = _DEFAULTS["playlist_subdir"]
    default_video_ext: str = _DEFAULTS["default_video_format"]
    default_audio_ext: str = _DEFAULTS["default_audio_format"]
    audio_quality: str = _DEFAULTS["audio_quality"]

    @property
    def video_base_path(self) -> Path:
        return self.base_dir / self.video_subdir

    @property
    def playlist_base_path(self) -> Path:
        return self.base_dir / self.playlist_subdir

    def get_video_output_dir(self, title: str, is_audio: bool = False) -> Path:
        subdir = "audio" if is_audio else "video"
        return self.video_base_path / title / subdir

    def get_playlist_output_dir(self, title: str, is_audio: bool = False) -> Path:
        subdir = "audio" if is_audio else "video"
        return self.playlist_base_path / title / subdir

    def ensure_dirs(self) -> None:
        self.video_base_path.mkdir(parents=True, exist_ok=True)
        self.playlist_base_path.mkdir(parents=True, exist_ok=True)


_raw = _load_config()
config = DownloadConfig(
    base_dir=Path(_raw["downloads_dir"]),
    video_subdir=_raw["video_subdir"],
    playlist_subdir=_raw["playlist_subdir"],
    default_video_ext=_raw["default_video_format"],
    default_audio_ext=_raw["default_audio_format"],
    audio_quality=_raw["audio_quality"],
)
