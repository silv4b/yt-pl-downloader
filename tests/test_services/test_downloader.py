"""Testes unitários para a classe base BaseDownloader."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yt_dlp

from app.core.config import DownloadConfig
from app.exceptions import DownloadError, InvalidURLError
from app.services.downloader import BaseDownloader, SilentLogger


class ConcreteDownloader(BaseDownloader):
    """Implementação concreta para testes."""

    def download(self, url: str, is_audio: bool = False):
        return "downloaded"


@pytest.fixture
def downloader():
    """Cria um downloader com configuração temporária."""
    with patch.object(DownloadConfig, "ensure_dirs"):
        return ConcreteDownloader(
            DownloadConfig(
                base_dir=Path("/tmp/test"),
                video_subdir="videos",
                playlist_subdir="playlists",
            )
        )


def test_silent_logger_does_nothing():
    """Verifica que SilentLogger não faz nada."""
    logger = SilentLogger()
    logger.debug("test")
    logger.warning("test")
    logger.error("test")


def test_extract_info_returns_data(downloader):
    """Verifica que _extract_info retorna metadados."""
    mock_info = {"title": "Test", "formats": []}
    with patch("yt_dlp.YoutubeDL") as mock_ydl:
        mock_ydl.return_value.__enter__ = lambda self: self
        mock_ydl.return_value.__exit__ = lambda self, *a: None
        mock_ydl.return_value.extract_info.return_value = mock_info
        result = downloader._extract_info("https://example.com")
        assert result == mock_info


def test_extract_info_raises_on_error(downloader):
    """Verifica que _extract_info levanta InvalidURLError em caso de erro."""
    with patch("yt_dlp.YoutubeDL") as mock_ydl:
        mock_ydl.return_value.__enter__ = lambda self: self
        mock_ydl.return_value.__exit__ = lambda self, *a: None
        mock_ydl.return_value.extract_info.side_effect = yt_dlp.utils.DownloadError("test")
        with pytest.raises(InvalidURLError):
            downloader._extract_info("https://invalid.com")


def test_get_ydl_options_for_audio(downloader):
    """Verifica que _get_ydl_options retorna configuração para áudio."""
    opts = downloader._get_ydl_options(Path("/tmp"), is_audio=True)
    assert opts["format"] == "bestaudio/best"
    assert opts["extractaudio"] is True
    assert opts["quiet"] is True
    assert opts["no_warnings"] is True


def test_get_ydl_options_for_video(downloader):
    """Verifica que _get_ydl_options retorna configuração para vídeo."""
    opts = downloader._get_ydl_options(Path("/tmp"), is_audio=False)
    assert "vcodec^=avc1" in opts["format"]
    assert opts["merge_output_format"] == "mp4"
    assert opts["quiet"] is True


def test_get_ydl_options_with_quality(downloader):
    """Verifica que _get_ydl_options usa qualidade customizada."""
    opts = downloader._get_ydl_options(
        Path("/tmp"),
        is_audio=False,
        quality="bestvideo[height<=720]+bestaudio/best",
    )
    assert "720" in opts["format"]


def test_get_ydl_options_with_progress_hook(downloader):
    """Verifica que _get_ydl_options inclui hook de progresso."""
    hook = MagicMock()
    opts = downloader._get_ydl_options(
        Path("/tmp"),
        is_audio=False,
        progress_hook=hook,
    )
    assert opts["progress_hooks"] == [hook]


def test_download_succeeds(downloader):
    """Verifica que _download executa sem erros."""
    with patch("yt_dlp.YoutubeDL") as mock_ydl:
        mock_ydl.return_value.__enter__ = lambda self: self
        mock_ydl.return_value.__exit__ = lambda self, *a: None
        mock_ydl.return_value.download.return_value = None
        downloader._download("https://example.com", {})


def test_download_raises_on_error(downloader):
    """Verifica que _download levanta DownloadError em caso de falha."""
    with patch("yt_dlp.YoutubeDL") as mock_ydl:
        mock_ydl.return_value.__enter__ = lambda self: self
        mock_ydl.return_value.__exit__ = lambda self, *a: None
        mock_ydl.return_value.download.side_effect = yt_dlp.utils.DownloadError("test")
        with pytest.raises(DownloadError, match="Download failed"):
            downloader._download("https://example.com", {})
