"""Aplicativo CLI do YouTube Downloader.

Ponto de entrada do aplicativo. Gerencia o fluxo de interação com o usuário,
verifica dependências (FFmpeg e Deno) e orquestra downloads de vídeos e
playlists através da camada de serviços.
"""

from __future__ import annotations

from app.cli.menu import (
    print_error,
    print_header,
    print_info,
    print_menu,
    print_success,
    print_warning,
    prompt_ffmpeg_install,
    prompt_format,
    prompt_url,
)
from app.core.config import config
from app.core.deno_utils import install_deno, verify_deno_installed
from app.core.ffmpeg_utils import install_ffmpeg, verify_ffmpeg_installed
from app.core.utils import clear_terminal
from app.exceptions import DownloadError, FFmpegInstallError
from app.services.playlist_downloader import PlaylistDownloader
from app.services.video_downloader import VideoDownloader


def check_and_install_ffmpeg() -> bool:
    """Verifica se o FFmpeg está instalado e oferece instalação se ausente.

    Returns:
        True se o FFmpeg estiver disponível, False se a instalação foi recusada ou falhou.
    """
    if verify_ffmpeg_installed():
        return True

    clear_terminal()
    print_info("FFmpeg não encontrado (necessário para conversão de formatos)")

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


def check_deno() -> bool:
    """Verifica se o Deno está instalado e avisa o usuário se estiver ausente.

    O Deno melhora a qualidade da extração do YouTube. Sem ele,
    alguns formatos de vídeo podem não estar disponíveis.

    Returns:
        True se o Deno estiver disponível, False caso contrário.
    """
    if verify_deno_installed():
        return True

    print_warning(
        "O Deno não está instalado. Ele melhora a extração de vídeos do YouTube,\n"
        "permitindo acesso a mais formatos e resoluções.\n\n"
        "Sem o Deno, alguns vídeos podem não estar disponíveis na melhor qualidade.\n"
        "Você pode instalar o Deno a qualquer momento pelo menu principal."
    )
    return False


def handle_install_deno() -> None:
    """Instala o Deno e notifica o usuário do resultado."""
    try:
        install_deno()
        print_success("Deno instalado com sucesso! Reinicie o aplicativo para aplicar.")
    except Exception as e:
        print_error(f"Falha na instalação: {e}")


def handle_video_download() -> None:
    """Gerencia o fluxo interativo para download de um único vídeo.

    Solicita URL e formato, executa o download e exibe o caminho
    de saída em caso de sucesso ou mensagem de erro em caso de falha.
    """
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
    """Gerencia o fluxo interativo para download de uma playlist.

    Solicita URL e formato, executa o download e exibe o caminho
    de saída e quantidade de vídeos em caso de sucesso ou erro em caso de falha.
    """
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
    """Ponto de entrada do aplicativo.

    Inicializa a CLI, verifica dependências (FFmpeg e Deno)
    e executa o loop principal de interação até o usuário escolher sair.
    """
    clear_terminal()
    print_header("YouTube Downloader")

    if not check_and_install_ffmpeg():
        return

    deno_available = check_deno()

    while True:
        choice = print_menu(show_deno_option=not deno_available)

        if choice == "v":
            handle_video_download()
        elif choice == "p":
            handle_playlist_download()
        elif choice == "d":
            handle_install_deno()
            deno_available = verify_deno_installed()
        elif choice == "q":
            print_info("Saindo...")
            break


if __name__ == "__main__":
    main()
