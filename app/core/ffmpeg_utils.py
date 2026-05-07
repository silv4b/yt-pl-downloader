"""Utilitários para detecção e instalação do FFmpeg.

O FFmpeg é necessário para extração de áudio e conversão de
formatos durante o download de vídeos.
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess

from app.exceptions import FFmpegInstallError


def _find_ffmpeg_winget_path() -> str | None:
    """Procura pelo ffmpeg.exe no diretório de instalação do winget.

    O Gyan.FFmpeg é instalado como pacote portátil pelo winget em
    ``%LOCALAPPDATA%\\Microsoft\\WinGet\\Packages\\Gyan.FFmpeg_*\\`` e não é
    adicionado ao PATH do sistema automaticamente.

    Returns:
        O caminho do diretório que contém ffmpeg.exe, ou None se não
        encontrado.
    """
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    if not local_app_data:
        return None

    winget_packages = os.path.join(local_app_data, "Microsoft", "WinGet", "Packages")
    if not os.path.isdir(winget_packages):
        return None

    try:
        for entry in os.listdir(winget_packages):
            if entry.startswith("Gyan.FFmpeg"):
                pkg_dir = os.path.join(winget_packages, entry)
                if os.path.isdir(pkg_dir):
                    for root, _dirs, files in os.walk(pkg_dir):
                        if "ffmpeg.exe" in files:
                            return root
    except PermissionError:
        return None

    return None


def _add_to_path(directory: str) -> None:
    """Adiciona um diretório ao PATH do processo atual se ainda não estiver lá.

    Args:
        directory: Caminho absoluto do diretório a ser adicionado.
    """
    current = os.environ.get("PATH", "")
    if directory not in current:
        os.environ["PATH"] = directory + os.pathsep + current


def verify_ffmpeg_installed() -> bool:
    """Verifica se o executável do FFmpeg está disponível.

    Primeiro verifica o PATH do sistema com ``shutil.which``. Se não
    encontrar, procura nos diretórios de instalação do winget e adiciona
    ao PATH do processo atual se localizado.

    Returns:
        True se o FFmpeg for encontrado, False caso contrário.
    """
    if shutil.which("ffmpeg") is not None:
        return True

    path = _find_ffmpeg_winget_path()
    if path is not None:
        _add_to_path(path)
        return True

    return False


def install_ffmpeg() -> None:
    """Instala o FFmpeg usando o gerenciador de pacotes do sistema.

    No Windows, usa o winget para instalar o Gyan.FFmpeg.
    No Linux, usa o apt para instalar o ffmpeg.

    Após a instalação (ou se já estiver instalado), localiza o binário
    e o adiciona ao PATH do processo atual.

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

    winget_failed = False

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        if system != "Windows":
            raise FFmpegInstallError(f"Falha na instalação do FFmpeg: {e}") from e
        winget_failed = True
    except FileNotFoundError as e:
        raise FFmpegInstallError(f"Gerenciador de pacotes não encontrado: {e}") from e

    if system == "Windows":
        path = _find_ffmpeg_winget_path()
        if path is not None:
            _add_to_path(path)
            return
        if winget_failed:
            raise FFmpegInstallError(
                "Falha na instalação do FFmpeg via winget. Tente instalar manualmente: winget install Gyan.FFmpeg"
            )
        raise FFmpegInstallError(
            "FFmpeg instalado via winget mas o executável não foi encontrado. "
            "Tente reiniciar o terminal ou adicionar manualmente ao PATH."
        )
