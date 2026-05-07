"""Testes unitários para detecção e instalação do Deno."""

import subprocess
from unittest.mock import mock_open, patch

import pytest

from app.core.deno_utils import _add_deno_to_profile, install_deno, verify_deno_installed
from app.exceptions import DenoInstallError


def test_verify_deno_installed_when_in_path():
    """Verifica que detecta Deno quando está no PATH."""
    with patch("shutil.which", return_value="/usr/bin/deno"):
        assert verify_deno_installed() is True


def test_verify_deno_installed_when_not_in_path():
    """Verifica que retorna False quando Deno não está no PATH."""
    with patch("shutil.which", return_value=None):
        with patch("platform.system", return_value="Linux"):
            with patch("os.path.isfile", return_value=False):
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
            with patch("os.path.isfile", return_value=False):
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
            with patch("os.path.isfile", return_value=False):
                with patch("app.core.deno_utils._add_deno_to_profile"):
                    install_deno()
                    mock_run.assert_called_once()
                    cmd = mock_run.call_args[0][0]
                    assert "curl" in cmd[2]


def test_install_deno_unsupported_os():
    """Verifica que levanta exceção para sistemas não suportados."""
    with patch("platform.system", return_value="FreeBSD"):
        with pytest.raises(DenoInstallError, match="não suportado"):
            install_deno()


def test_install_deno_raises_on_failure():
    """Verifica que levanta exceção quando instalação falha."""
    with patch("platform.system", return_value="Windows"):
        with patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, ["winget"])):
            with pytest.raises(DenoInstallError, match="Falha na instalação"):
                install_deno()


def test_install_deno_raises_on_file_not_found():
    """Verifica que levanta exceção quando gerenciador não é encontrado."""
    with patch("platform.system", return_value="Windows"):
        with patch("subprocess.run", side_effect=FileNotFoundError):
            with pytest.raises(DenoInstallError, match="não encontrado"):
                install_deno()


def test_add_deno_to_profile_appends_line():
    """Verifica que adiciona a linha do PATH no profile do shell bash."""
    with patch("os.environ.get", return_value="/bin/bash"):
        with patch("os.path.expanduser", return_value="/home/test"):
            with patch("os.path.isfile", return_value=False):
                m = mock_open()
                with patch("builtins.open", m):
                    _add_deno_to_profile()
                    write_calls = m.return_value.write.call_args_list
                    written = "".join(c.args[0] for c in write_calls)
                    assert "$HOME/.deno/bin" in written


def test_add_deno_to_profile_skips_when_already_present():
    """Verifica que não adiciona duplicata se a linha já existe no profile."""
    with patch("os.environ.get", return_value="/bin/bash"):
        with patch("os.path.expanduser", return_value="/home/test"):
            with patch("os.path.isfile", return_value=True):
                m = mock_open(read_data='export PATH="$HOME/.deno/bin:$PATH"')
                with patch("builtins.open", m):
                    _add_deno_to_profile()
                    m.return_value.write.assert_not_called()


def test_add_deno_to_profile_detects_zsh():
    """Verifica que detecta zsh e usa .zshrc como profile."""
    with patch("os.environ.get", return_value="/usr/bin/zsh"):
        with patch("os.path.expanduser", return_value="/home/test"):
            with patch("os.path.isfile", side_effect=lambda p: p.endswith(".zshrc")):
                m = mock_open()
                with patch("builtins.open", m):
                    _add_deno_to_profile()
                    opened = [c.args[0] for c in m.call_args_list]
                    assert any(".zshrc" in str(f) for f in opened)
