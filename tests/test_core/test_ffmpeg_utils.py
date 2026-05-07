"""Testes unitários para detecção e instalação do FFmpeg."""

import subprocess
from unittest.mock import patch

import pytest

from app.core.ffmpeg_utils import install_ffmpeg, verify_ffmpeg_installed
from app.exceptions import FFmpegInstallError


def test_verify_ffmpeg_installed_when_in_path():
    """Verifica que detecta FFmpeg quando está no PATH."""
    with patch("shutil.which", return_value="/usr/bin/ffmpeg"):
        assert verify_ffmpeg_installed() is True


def test_verify_ffmpeg_installed_when_not_in_path():
    """Verifica que retorna False quando FFmpeg não está no PATH nem no winget."""
    with (
        patch("shutil.which", return_value=None),
        patch("app.core.ffmpeg_utils._find_ffmpeg_winget_path", return_value=None),
    ):
        assert verify_ffmpeg_installed() is False


def test_verify_ffmpeg_installed_when_in_winget():
    """Verifica que detecta FFmpeg quando está no diretório do winget."""
    with (
        patch("shutil.which", return_value=None),
        patch("app.core.ffmpeg_utils._find_ffmpeg_winget_path", return_value="C:\\winget\\ffmpeg\\bin"),
    ):
        assert verify_ffmpeg_installed() is True


def test_install_ffmpeg_windows():
    """Verifica que instala FFmpeg via winget no Windows."""
    mock_result = type("obj", (object,), {"returncode": 0, "stderr": ""})()
    with (
        patch("platform.system", return_value="Windows"),
        patch("subprocess.run", return_value=mock_result) as mock_run,
        patch("app.core.ffmpeg_utils._find_ffmpeg_winget_path", return_value="C:\\winget\\ffmpeg\\bin"),
    ):
        install_ffmpeg()
        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        assert "winget" in cmd
        assert "Gyan.FFmpeg" in cmd


def test_install_ffmpeg_linux():
    """Verifica que instala FFmpeg via apt no Linux."""
    mock_result = type("obj", (object,), {"returncode": 0, "stderr": ""})()
    with (
        patch("platform.system", return_value="Linux"),
        patch("subprocess.run", return_value=mock_result) as mock_run,
    ):
        install_ffmpeg()
        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        assert "apt" in cmd
        assert "ffmpeg" in cmd


def test_install_ffmpeg_unsupported_os():
    """Verifica que levanta exceção para sistemas não suportados."""
    with patch("platform.system", return_value="FreeBSD"):
        with pytest.raises(FFmpegInstallError, match="não suportado"):
            install_ffmpeg()


def test_install_ffmpeg_windows_already_installed():
    """Verifica que quando winget retorna já instalado, localiza e adiciona ao PATH."""
    with (
        patch("platform.system", return_value="Windows"),
        patch("subprocess.run", side_effect=subprocess.CalledProcessError(2316632107, ["winget"])),
        patch("app.core.ffmpeg_utils._find_ffmpeg_winget_path", return_value="C:\\winget\\ffmpeg\\bin"),
    ):
        install_ffmpeg()


def test_install_ffmpeg_raises_on_winget_failure():
    """Verifica que levanta exceção quando winget falha e ffmpeg não é encontrado."""
    with (
        patch("platform.system", return_value="Windows"),
        patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, ["winget"])),
        patch("app.core.ffmpeg_utils._find_ffmpeg_winget_path", return_value=None),
    ):
        with pytest.raises(FFmpegInstallError, match="Falha na instalação"):
            install_ffmpeg()


def test_install_ffmpeg_raises_on_file_not_found():
    """Verifica que levanta exceção quando gerenciador não é encontrado."""
    with patch("platform.system", return_value="Windows"):
        with patch("subprocess.run", side_effect=FileNotFoundError):
            with pytest.raises(FFmpegInstallError, match="não encontrado"):
                install_ffmpeg()


def test_install_ffmpeg_raises_on_linux_failure():
    """Verifica que levanta exceção quando apt falha no Linux."""
    with (
        patch("platform.system", return_value="Linux"),
        patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, ["apt"])),
    ):
        with pytest.raises(FFmpegInstallError):
            install_ffmpeg()
