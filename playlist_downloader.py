import os
import re
import subprocess
import sys
import unicodedata
import yt_dlp


def remove_accents(text: str) -> str:
    """Remove acentos de caracteres Unicode."""
    normalized_text = unicodedata.normalize("NFKD", text)
    return "".join([c for c in normalized_text if not unicodedata.combining(c)])


def sanitize_filename(filename: str) -> str:
    """Normaliza e sanitiza nomes de arquivos removendo espaços e caracteres inválidos."""
    filename = remove_accents(filename)
    filename = re.sub(r"[^\w\s-]", "", filename)  # Remove caracteres especiais
    filename = re.sub(r"[\s]+", "_", filename)  # Substitui espaços por underlines
    return filename.strip()


def clear_terminal() -> None:
    if get_os_package_manager()[0] == "windows":
        subprocess.run(["cls"], shell=True)
    else:
        subprocess.run(["clear"], shell=True)


def make_download_folder(folder: str) -> None:
    """Verifica se existe a pasta de downloads onde são organizadas as playlists baixadas, se não existir, a pasta é criada."""
    print("Verificando se pasta de downloads existe ...")
    if not os.path.exists(folder):
        print("Pasta de download não definida!\nCriando ...")
        os.makedirs(folder)
        print(f"Pasta de download {folder} criada ✅")
    else:
        print("Pasta de download definida! ✅")


def get_os_package_manager() -> tuple:
    """Verifica o sistema operacional do usuário. Retornando o gerenciados de pacotes necessário para cada."""
    if sys.platform in ["win32", "win64"]:
        return "windows", "winget"
    elif sys.platform in ["linux"]:
        return "linux", "apt"


def execute_ffmpeg_installation() -> None:
    """Identifica e instala o FFmpeg no SO (windows ou linux)"""
    current_os_pm = get_os_package_manager()
    print(f"SO: {current_os_pm[0].capitalize()}")
    print(f"Instalar o FFmpeg?\n[Y]: sim, [n]: não.", end=" ")
    opc = input(": ")

    """
    (windows)
        winget install ffmpeg
        scoop install ffmpeg
    (linux)
        sudo apt install ffmpeg
    """

    if opc in "Yy" or opc == "":
        print(f"Tentando instalar FFmpeg via {current_os_pm[1]} do {current_os_pm[0]}")
        try:
            if current_os_pm[0] == "windows":
                subprocess.run(["winget", "install", "ffmpeg"], shell=True)
            else:
                subprocess.run(["sudo apt install ffmpeg"], shell=True)
        except:
            print("Não foi possível concluir a instalação.")
            exit(1)
    else:
        print("Encerrando.")
        exit(1)


def verify_ffmpeg_installation():
    """Verifica se o FFmpeg está instalado no PC (windows)"""

    # verificar se o FFmpeg está instalado
    print("Verificando instalação do FFmpeg ...")
    try:
        subprocess.run(["ffmpeg"])
    except Exception as e:
        print(f"FFmpeg não encontrado.\n{e}")
        print("Continuando para instalação ...")
        execute_ffmpeg_installation()
    else:
        print("FFmpeg encontrado\nContinuando ...")

    # criar um settings pra guardar essas informações (depois).


def playlist_downloader(link: str) -> None:
    if link.strip() == "":
        print("Nenhum link fornecido, encerrando.")
        return

    download_dir = "downloads"

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "noplaylist": False,
        "quiet": False,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            playlist_info = ydl.extract_info(link, download=False)
        except Exception as e:
            print(f"Erro ao extrair informação da playlist: {e}")
            exit(1)

        playlist_title = sanitize_filename(playlist_info["title"])
        playlist_path = os.path.join(download_dir, playlist_title)

        os.makedirs(playlist_path, exist_ok=True)

        total_video_count = len(playlist_info["entries"])
        print("\nTotal de vídeos na playlist: 🎦", total_video_count)

        new_names = []

        for index, video in enumerate(playlist_info["entries"], start=1):
            sanitized_title = sanitize_filename(video["title"])
            temp_filename = f"{index:02d}_{sanitized_title}.mp4"
            temp_filepath = os.path.join(playlist_path, temp_filename)

            ydl_opts["outtmpl"] = temp_filepath

            with yt_dlp.YoutubeDL(ydl_opts) as ydl2:
                try:
                    print(f"\nBaixando ({index}/{total_video_count}): {video['title']}")
                    ydl2.download([video["webpage_url"]])
                    print(f"✅ Baixado: {video['title']} successfully!")
                    print(f"📉 Vídeos restantes: {total_video_count - index}")

                    new_name = f"{index} - {sanitized_title}.mp4"
                    new_names.append(
                        (temp_filepath, os.path.join(playlist_path, new_name))
                    )
                except Exception as e:
                    print(f"❌ Erro ao baixar {video['title']}: {e}")

    print("🎉 Todos os vídeos baixados e renomeados com sucesso! 🎉")


def main() -> None:
    make_download_folder("downloads")
    verify_ffmpeg_installation()
    clear_terminal()
    print("Youtube Playlist Downloader")
    playlist_downloader(link=input("URL da Playlist do YouTube ✨: "))


if __name__ == "__main__":
    main()
