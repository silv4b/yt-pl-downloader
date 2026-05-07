"""Utilitários para detecção e instalação do FFmpeg.

O FFmpeg é necessário para extração de áudio e conversão de
formatos durante o download de vídeos.
"""

from __future__ import annotations

import platform
import shutil
import subprocess

from app.exceptions import FFmpegInstallError


def verify_ffmpeg_installed() -> bool:
    """Verifica se o executável do FFmpeg está disponível no PATH do sistema.

    Returns:
        True se o FFmpeg for encontrado, False caso contrário.
    """
    return shutil.which("ffmpeg") is not None


def install_ffmpeg() -> None:
    """Instala o FFmpeg usando o gerenciador de pacotes do sistema.

    No Windows, usa o winget para instalar o Gyan.FFmpeg.
    No Linux, usa o apt para instalar o ffmpeg.

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
            "Gyan.FFmpeg",
            "-e",
            "--accept-source-agreements",
            "--accept-package-agreements",
        ]
    elif system == "Linux":
        cmd = ["sudo", "apt", "install", "-y", "ffmpeg"]
    else:
        raise FFmpegInstallError(f"Sistema operacional não suportado: {system}")

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        raise FFmpegInstallError(f"Falha na instalação do FFmpeg: {e}") from e
    except FileNotFoundError as e:
        raise FFmpegInstallError(f"Gerenciador de pacotes não encontrado: {e}") from e
