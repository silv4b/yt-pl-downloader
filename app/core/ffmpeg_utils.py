from __future__ import annotations
from app.exceptions import FFmpegInstallError
import platform
import shutil
import subprocess


def verify_ffmpeg_installed() -> bool:
    return shutil.which("ffmpeg") is not None


def install_ffmpeg() -> None:
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
        raise FFmpegInstallError(f"Unsupported operating system: {system}")

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise FFmpegInstallError(f"FFmpeg installation failed: {result.stderr}")
    except subprocess.CalledProcessError as e:
        raise FFmpegInstallError(f"FFmpeg installation failed: {e.stderr}") from e
    except FileNotFoundError as e:
        raise FFmpegInstallError(f"Package manager not found: {e}") from e
