from pathlib import Path
from unittest.mock import mock_open, patch

from app.core.config import DownloadConfig, _load_config


def test_default_config_paths():
    config = DownloadConfig()
    assert config.base_dir == Path("downloads")
    assert config.video_subdir == "downloaded_videos"
    assert config.playlist_subdir == "downloaded_playlists"


def test_video_base_path():
    config = DownloadConfig()
    assert config.video_base_path == Path("downloads/downloaded_videos")


def test_playlist_base_path():
    config = DownloadConfig()
    assert config.playlist_base_path == Path("downloads/downloaded_playlists")


def test_get_video_output_dir_video():
    config = DownloadConfig()
    result = config.get_video_output_dir("MyPlaylist", is_audio=False)
    assert result == Path("downloads/downloaded_videos/MyPlaylist/video")


def test_get_video_output_dir_audio():
    config = DownloadConfig()
    result = config.get_video_output_dir("MyPlaylist", is_audio=True)
    assert result == Path("downloads/downloaded_videos/MyPlaylist/audio")


def test_get_playlist_output_dir_video():
    config = DownloadConfig()
    result = config.get_playlist_output_dir("MyPlaylist", is_audio=False)
    assert result == Path("downloads/downloaded_playlists/MyPlaylist/video")


def test_get_playlist_output_dir_audio():
    config = DownloadConfig()
    result = config.get_playlist_output_dir("MyPlaylist", is_audio=True)
    assert result == Path("downloads/downloaded_playlists/MyPlaylist/audio")


def test_load_config_from_yaml():
    yaml_content = """
downloads_dir: /custom/path
video_subdir: my_videos
"""
    with patch("app.core.config._find_config_path") as mock_find:
        mock_find.return_value = Path("fake_config.yaml")
        with patch("pathlib.Path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data=yaml_content)):
                result = _load_config()
                assert result["downloads_dir"] == "/custom/path"
                assert result["video_subdir"] == "my_videos"
                assert result["audio_quality"] == "192"


def test_load_config_defaults_on_missing_file():
    with patch("app.core.config._find_config_path") as mock_find:
        mock_find.return_value = Path("nonexistent.yaml")
        with patch("pathlib.Path.exists", return_value=False):
            result = _load_config()
            assert result["downloads_dir"] == "downloads"
            assert result["audio_quality"] == "192"
