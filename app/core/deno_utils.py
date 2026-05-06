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

from app.exceptions import FFmpegInstallError


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

    return False


def install_deno() -> None:
    """Instala o Deno usando o gerenciador de pacotes do sistema.

    No Windows, usa o winget para instalar o DenoLand.Deno.
    No Linux, baixa e executa o script oficial de instalação.

    Raises:
        FFmpegInstallError: Se o gerenciador de pacotes não for encontrado
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
        raise FFmpegInstallError(f"Unsupported operating system: {system}")

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise FFmpegInstallError(f"Deno installation failed: {result.stderr}")
    except subprocess.CalledProcessError as e:
        raise FFmpegInstallError(f"Deno installation failed: {e.stderr}") from e
    except FileNotFoundError as e:
        raise FFmpegInstallError(f"Package manager not found: {e}") from e
