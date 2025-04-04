import subprocess
import sys


def verify_ffmpeg_installed() -> bool:
    """Verifica se o FFmpeg está disponível no sistema"""
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def install_ffmpeg() -> None:
    """Sua lógica original de instalação multi-plataforma"""
    if sys.platform in ["win32", "win64"]:
        subprocess.run(["winget", "install", "ffmpeg"], check=True, shell=True)
    elif sys.platform in "linux":
        subprocess.run(["sudo apt install -y ffmpeg"], check=True, shell=True)
    else:
        raise OSError("Sistema operacional não suportado")
