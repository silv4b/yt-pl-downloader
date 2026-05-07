"""Utilitários para detecção e instalação do Deno.

O Deno é um ambiente de execução JavaScript usado pelo yt-dlp
para resolver desafios JS do YouTube, permitindo acesso a todos
os formatos e resoluções de vídeo.
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess

from app.exceptions import DenoInstallError


def verify_deno_installed() -> bool:
    """Verifica se o Deno está disponível no sistema.

    Verifica o PATH do sistema, a lista de pacotes do winget (Windows)
    e diretórios comuns de instalação.

    Returns:
        True se o Deno for encontrado, False caso contrário.
    """
    if shutil.which("deno") is not None:
        return True

    if platform.system() == "Windows":
        try:
            result = subprocess.run(
                ["winget", "list", "--id", "DenoLand.Deno", "-e"],
                capture_output=True,
                text=True,
                check=False,
            )
            if "DenoLand.Deno" in result.stdout and result.returncode == 0:
                return True
        except (FileNotFoundError, OSError):
            pass

        paths_to_check = [
            os.path.join(os.environ.get("USERPROFILE", ""), ".deno", "bin", "deno.exe"),
            os.path.join(os.environ.get("LOCALAPPDATA", ""), "deno", "deno.exe"),
        ]
        for path in paths_to_check:
            if os.path.isfile(path):
                return True

    deno_bin_dir = os.path.expanduser("~/.deno/bin")
    for name in ("deno", "deno.exe"):
        if os.path.isfile(os.path.join(deno_bin_dir, name)):
            os.environ["PATH"] = f"{deno_bin_dir}:{os.environ.get('PATH', '')}"
            return True

    return False


def install_deno() -> None:
    """Instala o Deno usando o gerenciador de pacotes do sistema.

    No Windows, usa o winget para instalar o DenoLand.Deno.
    No Linux, baixa e executa o script oficial de instalação.

    Raises:
        DenoInstallError: Se o gerenciador de pacotes não for encontrado
            ou a instalação falhar.
    """
    system = platform.system()

    if system == "Windows":
        cmd = [
            "winget",
            "install",
            "--id",
            "DenoLand.Deno",
            "-e",
            "--accept-source-agreements",
            "--accept-package-agreements",
        ]
    elif system == "Linux":
        cmd = ["sh", "-c", "curl -fsSL https://deno.land/install.sh | sh"]
    else:
        raise DenoInstallError(f"Sistema operacional não suportado: {system}")

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        raise DenoInstallError(f"Falha na instalação do Deno: {e}") from e
    except FileNotFoundError as e:
        raise DenoInstallError(f"Gerenciador de pacotes não encontrado: {e}") from e

    deno_bin_dir = os.path.expanduser("~/.deno/bin")
    for name in ("deno", "deno.exe"):
        if os.path.isfile(os.path.join(deno_bin_dir, name)):
            os.environ["PATH"] = f"{deno_bin_dir}:{os.environ.get('PATH', '')}"
            break

    if system == "Linux":
        _add_deno_to_profile()


def _add_deno_to_profile() -> None:
    """Adiciona ~/.deno/bin ao PATH do shell no arquivo de perfil.

    Adiciona a linha 'export PATH="$HOME/.deno/bin:$PATH"' ao arquivo
    de configuração do shell (.bashrc, .zshrc ou .profile), permitindo
    que o comando 'deno' fique disponível em novos terminais.
    """
    path_line = 'export PATH="$HOME/.deno/bin:$PATH"'
    shell = os.environ.get("SHELL", "")
    home = os.path.expanduser("~")

    if shell.endswith("zsh"):
        candidates = [
            os.path.join(home, ".zshenv"),
            os.path.join(home, ".zshrc"),
        ]
    elif shell.endswith("bash"):
        candidates = [
            os.path.join(home, ".bashrc"),
            os.path.join(home, ".bash_profile"),
        ]
    else:
        candidates = [os.path.join(home, ".profile")]

    config_file = None
    for candidate in candidates:
        if os.path.isfile(candidate):
            config_file = candidate
            break

    if config_file is None:
        config_file = candidates[0]

    try:
        with open(config_file) as f:
            if path_line in f.read():
                return
    except FileNotFoundError:
        pass

    try:
        with open(config_file, "a") as f:
            f.write(f"\n# Adicionado por yt-pl-downloader\n{path_line}\n")
    except OSError:
        pass
