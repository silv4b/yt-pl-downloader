"""Aplicativo CLI do YouTube Downloader.

Ponto de entrada do aplicativo. Gerencia o fluxo de interação com o usuário,
verifica dependências (FFmpeg e Deno) e orquestra downloads de vídeos e
playlists através da camada de serviços.
"""

from __future__ import annotations

from app.cli.menu import (
    create_progress,
    open_folder,
    print_error,
    print_header,
    print_info,
    print_menu,
    print_success,
    print_warning,
    prompt_ffmpeg_install,
    prompt_format,
    prompt_open_folder,
    prompt_url,
    update_playlist_status,
)
from app.cli.quality import prompt_quality
from app.core.config import config
from app.core.deno_utils import install_deno, verify_deno_installed
from app.core.ffmpeg_utils import install_ffmpeg, verify_ffmpeg_installed
from app.core.utils import clear_terminal, sanitize_filename
from app.exceptions import DenoInstallError, DownloadError, FFmpegInstallError
from app.services.playlist_downloader import PlaylistDownloader
from app.services.video_downloader import VideoDownloader


def _maybe_open_folder(path: str) -> None:
    """Pergunta se o usuário deseja abrir a pasta e abre se confirmado.

    Args:
        path: Caminho da pasta de download.
    """
    if prompt_open_folder(path):
        open_folder(path)
        print_info("Pasta aberta no explorador.")


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
    except DenoInstallError as e:
        print_error(f"Falha na instalação: {e}")


def handle_video_download() -> None:
    """Gerencia o fluxo interativo para download de um único vídeo.

    Solicita URL, formato e qualidade, executa o download e exibe o caminho
    de saída em caso de sucesso ou mensagem de erro em caso de falha.
    """
    url = prompt_url()
    if not url:
        print_error("URL vazia. Operação cancelada.")
        return

    is_audio = prompt_format()
    quality = None
    if not is_audio:
        info = VideoDownloader(config)._extract_info(url)
        quality = prompt_quality(info, url)

    try:
        downloader = VideoDownloader(config)
        video = downloader.download(url, is_audio, quality)
        output_dir = config.get_video_output_dir(video.title, is_audio)
        print_success(f"Download concluído! Salvo em: {output_dir}")
        _maybe_open_folder(str(output_dir))
    except DownloadError as e:
        print_error(f"Falha no download: {e}")


def handle_playlist_download() -> None:
    """Gerencia o fluxo interativo para download de uma playlist.

    Lista todos os vídeos da playlist com tabela de status,
    exibe a barra de progresso abaixo da tabela para cada vídeo,
    e ao final pergunta se o usuário deseja abrir a pasta de download.
    """
    url = prompt_url()
    if not url:
        print_error("URL vazia. Operação cancelada.")
        return

    is_audio = prompt_format()
    quality = None
    if not is_audio:
        info = VideoDownloader(config)._extract_info(url)
        quality = prompt_quality(info, url)

    try:
        downloader = PlaylistDownloader(config)
        info = downloader._extract_info(url)
        entries = info.get("entries")
        if not entries:
            print_error("Playlist sem vídeos.")
            return

        total_videos = len([e for e in entries if e is not None])
        playlist_title = sanitize_filename(info.get("title", "unknown_playlist"))
        output_dir = config.get_playlist_output_dir(playlist_title, is_audio)
        output_dir.mkdir(parents=True, exist_ok=True)

        completed = set()
        failed = set()

        for index, video_info in enumerate(entries, start=1):
            if video_info is None:
                continue

            video_title = sanitize_filename(video_info.get("title", f"video_{index}"))
            video_url = video_info.get("webpage_url") or video_info.get("url")
            if not video_url:
                continue

            video_info_obj = video_info
            known_size = video_info_obj.get("filesize") or video_info_obj.get("filesize_approx") or 0
            file_type = "audio" if is_audio else "video"

            ydl_opts = downloader._get_ydl_options(output_dir, is_audio, quality=quality)
            ydl_opts["outtmpl"] = str(output_dir / f"{index:02d}_{video_title}.%(ext)s")

            def hook(d: dict) -> None:
                if d.get("status") == "downloading":
                    downloaded = d.get("downloaded_bytes", 0)
                    total = d.get("total_bytes") or d.get("total_bytes_estimate") or known_size
                    if total and total > 0:
                        progress.update(task, total=total, completed=downloaded)

            ydl_opts["progress_hooks"] = [hook]

            clear_terminal()
            print_header(f"Playlist — {playlist_title[:50]}")
            update_playlist_status(entries, completed, failed, index)

            try:
                with create_progress() as progress:
                    task = progress.add_task(
                        f"[cyan]{file_type}: {video_title[:50]}",
                        total=known_size if known_size > 0 else None,
                    )
                    downloader._download(video_url, ydl_opts)
                completed.add(index)
            except DownloadError:
                failed.add(index)

        clear_terminal()
        print_header(f"Playlist concluída — {playlist_title[:50]}")
        update_playlist_status(entries, completed, failed, None)
        print_success(f"Playlist concluída! {len(completed)} de {total_videos} vídeos salvos em: {output_dir}")
        _maybe_open_folder(str(output_dir))
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
