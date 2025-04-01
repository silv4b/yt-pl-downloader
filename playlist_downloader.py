import os
from time import sleep
import yt_dlp
import re
import unicodedata


def remove_accents(text: str) -> str:
    """Remove acentos de caracteres Unicode."""
    normalized_text = unicodedata.normalize("NFKD", text)
    return "".join([c for c in normalized_text if not unicodedata.combining(c)])


def sanitize_filename(filename: str) -> str:
    """Normaliza e sanitiza nomes de arquivos removendo acentos, espaços e caracteres inválidos."""
    filename = remove_accents(filename)
    filename = re.sub(r"[^\w\s-]", "", filename)  # Remove caracteres especiais
    filename = re.sub(r"[\s]+", "_", filename)  # Substitui espaços por underlines
    return filename.strip()


def make_download_folder(folder: str) -> None:
    """Verifica se existe a pasta de downloads onde são organizadas as playlists baixadas, se não existir, a pasta é criada."""
    print("Verificando se pasta de downloads existe ...")
    sleep(1)
    if not os.path.exists(folder):
        print("Pasta de download não definida!\nCriando ...")
        sleep(1)
        os.makedirs(folder)
        print(f"Pasta de download {folder} criada ✅")
    else:
        print("Pasta de download definida! ✅")


def main() -> None:
    make_download_folder("downloads")

    download_dir = "downloads"
    link = input("URL da Playlist do YouTube ✨: ")

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


if __name__ == "__main__":
    main()
