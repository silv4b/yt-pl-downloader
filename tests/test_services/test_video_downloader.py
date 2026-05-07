"""Testes unitários para o serviço de download de vídeo."""

from pathlib import Path
from unittest.mock import patch

import pytest

from app.core.config import DownloadConfig
from app.exceptions import InvalidURLError
from app.models.video import VideoInfo
from app.services.video_downloader import VideoDownloader


@pytest.fixture
def downloader():
    """Cria um VideoDownloader com configuração mockada."""
    with patch.object(DownloadConfig, "ensure_dirs"):
        return VideoDownloader(
            DownloadConfig(
                base_dir=Path("/tmp/test"),
                video_subdir="videos",
                playlist_subdir="playlists",
            )
        )


def test_video_download_succeeds(downloader):
    """Verifica que download de vídeo retorna VideoInfo."""
    mock_info = {
        "title": "Test Video",
        "url": "https://example.com",
        "uploader": "Channel",
        "duration": 120,
        "filesize": 1000000,
    }
    with patch.object(downloader, "_extract_info", return_value=mock_info):
        with patch.object(downloader, "_download"):
            video = downloader.download("https://example.com")
            assert isinstance(video, VideoInfo)
            assert "Test" in video.title
            assert "Video" in video.title
            assert video.url == "https://example.com"
            assert video.uploader == "Channel"
            assert video.duration == 120


def test_video_download_audio(downloader):
    """Verifica que download de áudio configura diretório corretamente."""
    mock_info = {"title": "Test Audio", "url": "https://example.com"}
    with patch.object(downloader, "_extract_info", return_value=mock_info):
        with patch.object(downloader, "_download"):
            video = downloader.download("https://example.com", is_audio=True)
            assert isinstance(video, VideoInfo)
            assert "Test" in video.title


def test_video_download_with_quality(downloader):
    """Verifica que download usa qualidade customizada."""
    mock_info = {"title": "Test", "url": "https://example.com"}
    with patch.object(downloader, "_extract_info", return_value=mock_info):
        with patch.object(downloader, "_download"):
            with patch.object(downloader, "_get_ydl_options", return_value={}) as mock_opts:
                downloader.download(
                    "https://example.com",
                    quality="bestvideo[height<=720]+bestaudio/best",
                )
                mock_opts.assert_called_once()
                call_args = mock_opts.call_args[0]
                assert len(call_args) == 4
                assert call_args[3] == "bestvideo[height<=720]+bestaudio/best"


def test_video_download_raises_on_error(downloader):
    """Verifica que download levanta DownloadError em caso de falha."""
    with patch.object(downloader, "_extract_info", side_effect=InvalidURLError("Bad URL")):
        with pytest.raises(InvalidURLError):
            downloader.download("https://invalid.com")


def test_video_download_sanitizes_title(downloader):
    """Verifica que título é sanitizado para nome de pasta."""
    mock_info = {"title": "Video! @#$% Name", "url": "https://example.com"}
    with patch.object(downloader, "_extract_info", return_value=mock_info):
        with patch.object(downloader, "_download"):
            video = downloader.download("https://example.com")
            assert "Video" in video.title
            assert "Name" in video.title
