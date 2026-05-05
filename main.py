from __future__ import annotations

from app.cli.menu import (
    print_error,
    print_header,
    print_info,
    print_success,
    prompt_ffmpeg_install,
    prompt_format,
    prompt_main_action,
    prompt_url,
)
from app.core.config import config
from app.core.ffmpeg_utils import install_ffmpeg, verify_ffmpeg_installed
from app.core.utils import clear_terminal
from app.exceptions import DownloadError, FFmpegInstallError
from app.services.playlist_downloader import PlaylistDownloader
from app.services.video_downloader import VideoDownloader


def check_and_install_ffmpeg() -> bool:
    if verify_ffmpeg_installed():
        return True

    clear_terminal()
    print("FFmpeg não encontrado (necessário para conversão de formatos)")

    if prompt_ffmpeg_install():
        try:
            install_ffmpeg()
            print_success("FFmpeg instalado com sucesso!")
            return True
        except FFmpegInstallError as e:
            print_error(f"Falha na instalação: {e}")
            return False
    else:
        print_info("Operação cancelada pelo usuário")
        return False


def handle_video_download() -> None:
    url = prompt_url()
    if not url:
        print_error("URL vazia. Operação cancelada.")
        return

    is_audio = prompt_format()

    try:
        downloader = VideoDownloader(config)
        video = downloader.download(url, is_audio)
        output_dir = config.get_video_output_dir(video.title, is_audio)
        print_success(f"Download concluído! Salvo em: {output_dir}")
    except DownloadError as e:
        print_error(f"Falha no download: {e}")


def handle_playlist_download() -> None:
    url = prompt_url()
    if not url:
        print_error("URL vazia. Operação cancelada.")
        return

    is_audio = prompt_format()

    try:
        downloader = PlaylistDownloader(config)
        playlist = downloader.download(url, is_audio)
        output_dir = config.get_playlist_output_dir(playlist.title, is_audio)
        print_success(f"Playlist concluída! {len(playlist.videos)} vídeos salvos em: {output_dir}")
    except DownloadError as e:
        print_error(f"Falha no download: {e}")


def main() -> None:
    clear_terminal()
    print_header("YouTube Downloader")

    if not check_and_install_ffmpeg():
        return

    while True:
        choice = prompt_main_action()

        if choice == "video":
            handle_video_download()
        elif choice == "playlist":
            handle_playlist_download()
        elif choice == "quit":
            print_info("Saindo...")
            break


if __name__ == "__main__":
    main()
