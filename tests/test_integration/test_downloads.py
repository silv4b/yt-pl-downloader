"""Testes de integração para downloads reais do YouTube.

Executa downloads de verdade (não mockados) para validar que
o sistema completo funciona: extração de metadados, criação
de diretórios, download de arquivos e conversão de formatos.

Estes testes são marcados com @pytest.mark.integration e podem
ser ignorados com a variável de ambiente SKIP_INTEGRATION=1.
"""

import os
import shutil
import tempfile
from pathlib import Path

import pytest

from app.core.config import DownloadConfig
from app.services.playlist_downloader import PlaylistDownloader
from app.services.video_downloader import VideoDownloader

PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLb1K1Zkw7ZanmbODnKgIKarEcEoPXqBXj"
VIDEO_URL = "https://www.youtube.com/watch?v=4x-7ZzfaZQk"


@pytest.fixture
def test_config():
    """Cria uma configuração temporária que é limpa após cada teste.

    Usa um diretório temporário isolado para não interferir
    com downloads reais do usuário.
    """
    tmp_dir = tempfile.mkdtemp(prefix="yt_test_")
    config = DownloadConfig(
        base_dir=Path(tmp_dir),
        video_subdir="test_videos",
        playlist_subdir="test_playlists",
    )
    yield config
    shutil.rmtree(tmp_dir, ignore_errors=True)


@pytest.mark.integration
@pytest.mark.skipif(
    os.getenv("SKIP_INTEGRATION") == "1",
    reason="Testes de integração ignorados",
)
class TestVideoDownloadMP4:
    """Testa download de vídeo individual em formato MP4."""

    def test_download_video_as_mp4(self, test_config):
        """Baixa um vídeo como MP4 e verifica se o arquivo existe e tem tamanho válido."""
        downloader = VideoDownloader(test_config)
        video = downloader.download(VIDEO_URL, is_audio=False)

        assert video.title, "O título do vídeo não deve estar vazio"
        assert video.url == VIDEO_URL

        output_dir = test_config.get_video_output_dir(video.title, is_audio=False)
        assert output_dir.exists(), f"O diretório de saída deve existir: {output_dir}"

        mp4_files = list(output_dir.glob("*.mp4"))
        assert len(mp4_files) > 0, f"Deve haver pelo menos um arquivo .mp4 em {output_dir}"

        file_size = mp4_files[0].stat().st_size
        assert file_size > 1_000_000, f"O arquivo MP4 deve ter mais de 1MB, obtido {file_size}"


@pytest.mark.integration
@pytest.mark.skipif(
    os.getenv("SKIP_INTEGRATION") == "1",
    reason="Testes de integração ignorados",
)
class TestVideoDownloadMP3:
    """Testa download de vídeo individual com extração de áudio MP3."""

    def test_download_video_as_mp3(self, test_config):
        """Baixa um vídeo como MP3 e verifica se o arquivo existe e tem tamanho válido."""
        downloader = VideoDownloader(test_config)
        video = downloader.download(VIDEO_URL, is_audio=True)

        assert video.title, "O título do vídeo não deve estar vazio"
        assert video.url == VIDEO_URL

        output_dir = test_config.get_video_output_dir(video.title, is_audio=True)
        assert output_dir.exists(), f"O diretório de saída deve existir: {output_dir}"

        mp3_files = list(output_dir.glob("*.mp3"))
        assert len(mp3_files) > 0, f"Deve haver pelo menos um arquivo .mp3 em {output_dir}"

        file_size = mp3_files[0].stat().st_size
        assert file_size > 100_000, f"O arquivo MP3 deve ter mais de 100KB, obtido {file_size}"


@pytest.mark.integration
@pytest.mark.skipif(
    os.getenv("SKIP_INTEGRATION") == "1",
    reason="Testes de integração ignorados",
)
class TestPlaylistDownload:
    """Testa download de playlist completa em formatos MP4 e MP3."""

    def test_download_playlist_as_mp4(self, test_config):
        """Baixa uma playlist como MP4 e verifica se os arquivos existem."""
        downloader = PlaylistDownloader(test_config)
        playlist = downloader.download(PLAYLIST_URL, is_audio=False)

        assert playlist.title, "O título da playlist não deve estar vazio"
        assert playlist.url == PLAYLIST_URL
        assert playlist.total_videos > 0, "A playlist deve ter pelo menos um vídeo"

        output_dir = test_config.get_playlist_output_dir(playlist.title, is_audio=False)
        assert output_dir.exists(), f"O diretório de saída deve existir: {output_dir}"

        mp4_files = list(output_dir.glob("*.mp4"))
        assert len(mp4_files) > 0, f"Deve haver pelo menos um arquivo .mp4 em {output_dir}"

    def test_download_playlist_as_mp3(self, test_config):
        """Baixa uma playlist como MP3 e verifica se os arquivos existem."""
        downloader = PlaylistDownloader(test_config)
        playlist = downloader.download(PLAYLIST_URL, is_audio=True)

        assert playlist.title, "O título da playlist não deve estar vazio"
        assert playlist.url == PLAYLIST_URL
        assert playlist.total_videos > 0, "A playlist deve ter pelo menos um vídeo"

        output_dir = test_config.get_playlist_output_dir(playlist.title, is_audio=True)
        assert output_dir.exists(), f"O diretório de saída deve existir: {output_dir}"

        mp3_files = list(output_dir.glob("*.mp3"))
        assert len(mp3_files) > 0, f"Deve haver pelo menos um arquivo .mp3 em {output_dir}"
