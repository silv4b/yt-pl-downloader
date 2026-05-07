"""Testes unitários para detecção e instalação do FFmpeg."""

from unittest.mock import patch

import pytest

from app.core.ffmpeg_utils import install_ffmpeg, verify_ffmpeg_installed
from app.exceptions import FFmpegInstallError


def test_verify_ffmpeg_installed_when_in_path():
    """Verifica que detecta FFmpeg quando está no PATH."""
    with patch("shutil.which", return_value="/usr/bin/ffmpeg"):
        assert verify_ffmpeg_installed() is True


def test_verify_ffmpeg_installed_when_not_in_path():
    """Verifica que retorna False quando FFmpeg não está no PATH."""
    with patch("shutil.which", return_value=None):
        assert verify_ffmpeg_installed() is False


def test_install_ffmpeg_windows():
    """Verifica que instala FFmpeg via winget no Windows."""
    mock_result = type("obj", (object,), {"returncode": 0, "stderr": ""})()
    with patch("platform.system", return_value="Windows"):
        with patch("subprocess.run", return_value=mock_result) as mock_run:
            install_ffmpeg()
            mock_run.assert_called_once()
            cmd = mock_run.call_args[0][0]
            assert "winget" in cmd
            assert "Gyan.FFmpeg" in cmd


def test_install_ffmpeg_linux():
    """Verifica que instala FFmpeg via apt no Linux."""
    mock_result = type("obj", (object,), {"returncode": 0, "stderr": ""})()
    with patch("platform.system", return_value="Linux"):
        with patch("subprocess.run", return_value=mock_result) as mock_run:
            install_ffmpeg()
            mock_run.assert_called_once()
            cmd = mock_run.call_args[0][0]
            assert "apt" in cmd
            assert "ffmpeg" in cmd


def test_install_ffmpeg_unsupported_os():
    """Verifica que levanta exceção para sistemas não suportados."""
    with patch("platform.system", return_value="FreeBSD"):
        with pytest.raises(FFmpegInstallError, match="Unsupported operating system"):
            install_ffmpeg()


def test_install_ffmpeg_raises_on_failure():
    """Verifica que levanta exceção quando instalação falha."""
    mock_result = type("obj", (object,), {"returncode": 1, "stderr": "error"})()
    with patch("platform.system", return_value="Windows"):
        with patch("subprocess.run", return_value=mock_result):
            with pytest.raises(FFmpegInstallError, match="installation failed"):
                install_ffmpeg()


def test_install_ffmpeg_raises_on_file_not_found():
    """Verifica que levanta exceção quando gerenciador não é encontrado."""
    with patch("platform.system", return_value="Windows"):
        with patch("subprocess.run", side_effect=FileNotFoundError):
            with pytest.raises(FFmpegInstallError, match="not found"):
                install_ffmpeg()


def test_install_ffmpeg_raises_on_called_process_error():
    """Verifica que levanta exceção quando subprocesso falha."""
    with patch("platform.system", return_value="Windows"):
        with patch("subprocess.run", side_effect=Exception("fail")):
            with pytest.raises(Exception):
                install_ffmpeg()
