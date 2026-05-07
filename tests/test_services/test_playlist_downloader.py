"""Testes unitários para o serviço de download de playlist."""

from pathlib import Path
from unittest.mock import patch

import pytest

from app.core.config import DownloadConfig
from app.exceptions import PlaylistExtractionError
from app.models.playlist import PlaylistInfo
from app.services.playlist_downloader import PlaylistDownloader


@pytest.fixture
def downloader():
    """Cria um PlaylistDownloader com configuração mockada."""
    with patch.object(DownloadConfig, "ensure_dirs"):
        return PlaylistDownloader(
            DownloadConfig(
                base_dir=Path("/tmp/test"),
                video_subdir="videos",
                playlist_subdir="playlists",
            )
        )


def test_playlist_download_succeeds(downloader):
    """Verifica que download de playlist retorna PlaylistInfo."""
    mock_info = {
        "title": "Test Playlist",
        "entries": [
            {
                "title": "Video 1",
                "webpage_url": "https://example.com/1",
            },
            {
                "title": "Video 2",
                "webpage_url": "https://example.com/2",
            },
        ],
    }
    with patch.object(downloader, "_extract_info", return_value=mock_info):
        with patch.object(downloader, "_download"):
            playlist = downloader.download("https://example.com/playlist")
            assert isinstance(playlist, PlaylistInfo)
            assert "Test" in playlist.title
            assert len(playlist.videos) == 2


def test_playlist_download_raises_on_empty(downloader):
    """Verifica que levanta exceção quando playlist não tem vídeos."""
    mock_info = {"title": "Empty Playlist", "entries": []}
    with patch.object(downloader, "_extract_info", return_value=mock_info):
        with pytest.raises(PlaylistExtractionError, match="Nenhum vídeo encontrado"):
            downloader.download("https://example.com/playlist")


def test_playlist_download_skips_none_entries(downloader):
    """Verifica que entradas None são ignoradas."""
    mock_info = {
        "title": "Test Playlist",
        "entries": [
            None,
            {"title": "Video 1", "webpage_url": "https://example.com/1"},
            None,
        ],
    }
    with patch.object(downloader, "_extract_info", return_value=mock_info):
        with patch.object(downloader, "_download"):
            playlist = downloader.download("https://example.com/playlist")
            assert len(playlist.videos) == 1


def test_playlist_download_skips_missing_url(downloader):
    """Verifica que vídeos sem URL são ignorados."""
    mock_info = {
        "title": "Test Playlist",
        "entries": [
            {"title": "Video 1", "webpage_url": None},
            {"title": "Video 2", "webpage_url": "https://example.com/2"},
        ],
    }
    with patch.object(downloader, "_extract_info", return_value=mock_info):
        with patch.object(downloader, "_download"):
            playlist = downloader.download("https://example.com/playlist")
            assert len(playlist.videos) == 1


def test_playlist_download_continues_on_error(downloader):
    """Verifica que download continua mesmo se um vídeo falhar."""
    from app.exceptions import DownloadError

    mock_info = {
        "title": "Test Playlist",
        "entries": [
            {"title": "Video 1", "webpage_url": "https://example.com/1"},
            {"title": "Video 2", "webpage_url": "https://example.com/2"},
        ],
    }

    def mock_download(url, opts):
        if "1" in url:
            raise DownloadError("Failed")

    with patch.object(downloader, "_extract_info", return_value=mock_info):
        with patch.object(downloader, "_download", side_effect=mock_download):
            playlist = downloader.download("https://example.com/playlist")
            assert len(playlist.videos) == 1


def test_playlist_download_audio(downloader):
    """Verifica que download de playlist em áudio funciona."""
    mock_info = {
        "title": "Test Playlist",
        "entries": [
            {"title": "Video 1", "webpage_url": "https://example.com/1"},
        ],
    }
    with patch.object(downloader, "_extract_info", return_value=mock_info):
        with patch.object(downloader, "_download"):
            playlist = downloader.download("https://example.com/playlist", is_audio=True)
            assert len(playlist.videos) == 1


def test_playlist_download_with_quality(downloader):
    """Verifica que download usa qualidade customizada."""
    mock_info = {
        "title": "Test Playlist",
        "entries": [
            {"title": "Video 1", "webpage_url": "https://example.com/1"},
        ],
    }
    quality = "bestvideo[height<=720]+bestaudio/best"
    with patch.object(downloader, "_extract_info", return_value=mock_info):
        with patch.object(downloader, "_download"):
            with patch.object(downloader, "_get_ydl_options", return_value={}) as mock_opts:
                downloader.download("https://example.com/playlist", quality=quality)
                mock_opts.assert_called_once()
                assert mock_opts.call_args[1]["quality"] == quality
