"""Testes unitários para detecção e instalação do Deno."""

from unittest.mock import patch

import pytest

from app.core.deno_utils import install_deno, verify_deno_installed
from app.exceptions import FFmpegInstallError


def test_verify_deno_installed_when_in_path():
    """Verifica que detecta Deno quando está no PATH."""
    with patch("shutil.which", return_value="/usr/bin/deno"):
        assert verify_deno_installed() is True


def test_verify_deno_installed_when_not_in_path():
    """Verifica que retorna False quando Deno não está no PATH."""
    with patch("shutil.which", return_value=None):
        with patch("platform.system", return_value="Linux"):
            assert verify_deno_installed() is False


def test_verify_deno_installed_via_winget():
    """Verifica que detecta Deno via winget no Windows."""
    mock_result = type("obj", (object,), {"returncode": 0, "stdout": "DenoLand.Deno 1.0.0"})()
    with patch("shutil.which", return_value=None):
        with patch("platform.system", return_value="Windows"):
            with patch("subprocess.run", return_value=mock_result):
                assert verify_deno_installed() is True


def test_verify_deno_installed_via_local_path():
    """Verifica que detecta Deno via caminho local no Windows."""
    with patch("shutil.which", return_value=None):
        with patch("platform.system", return_value="Windows"):
            with patch("subprocess.run", side_effect=FileNotFoundError):
                with patch.dict("os.environ", {"USERPROFILE": "C:\\Users\\test"}):
                    with patch("os.path.isfile", return_value=True):
                        assert verify_deno_installed() is True


def test_install_deno_windows():
    """Verifica que instala Deno via winget no Windows."""
    mock_result = type("obj", (object,), {"returncode": 0, "stderr": ""})()
    with patch("platform.system", return_value="Windows"):
        with patch("subprocess.run", return_value=mock_result) as mock_run:
            install_deno()
            mock_run.assert_called_once()
            cmd = mock_run.call_args[0][0]
            assert "winget" in cmd
            assert "DenoLand.Deno" in cmd


def test_install_deno_linux():
    """Verifica que instala Deno via curl no Linux."""
    mock_result = type("obj", (object,), {"returncode": 0, "stderr": ""})()
    with patch("platform.system", return_value="Linux"):
        with patch("subprocess.run", return_value=mock_result) as mock_run:
            install_deno()
            mock_run.assert_called_once()
            cmd = mock_run.call_args[0][0]
            assert "curl" in cmd[2]


def test_install_deno_unsupported_os():
    """Verifica que levanta exceção para sistemas não suportados."""
    with patch("platform.system", return_value="FreeBSD"):
        with pytest.raises(FFmpegInstallError, match="Unsupported operating system"):
            install_deno()


def test_install_deno_raises_on_failure():
    """Verifica que levanta exceção quando instalação falha."""
    mock_result = type("obj", (object,), {"returncode": 1, "stderr": "error"})()
    with patch("platform.system", return_value="Windows"):
        with patch("subprocess.run", return_value=mock_result):
            with pytest.raises(FFmpegInstallError, match="installation failed"):
                install_deno()


def test_install_deno_raises_on_file_not_found():
    """Verifica que levanta exceção quando gerenciador não é encontrado."""
    with patch("platform.system", return_value="Windows"):
        with patch("subprocess.run", side_effect=FileNotFoundError):
            with pytest.raises(FFmpegInstallError, match="not found"):
                install_deno()
