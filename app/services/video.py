import os
import yt_dlp
from app.core.utils import make_alpha_numeric, sanitize_filename


def video_downloader() -> None:
    BASE_DIR = "downloads/downloaded_videos_only"

    link = input("Digite a URL do vídeo do YouTube: ✨ ")

    print("\nEscolha o formato:")
    print("[V] Vídeo (MP4)")
    print("[A] Áudio (MP3)")
    choice = input("Opção (V/A): ").lower()

    # Primeiro obtemos as informações do vídeo
    with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
        video_info = ydl.extract_info(link, download=False)
        video_title = sanitize_filename(video_info["title"])
        safe_title = make_alpha_numeric(video_title)

    if choice == "a":
        # Configurações para áudio
        OUTPUT_DIR = os.path.join(BASE_DIR, safe_title, "audio")
        file_ext = "mp3"
        file_type = "áudio"
        ydl_parameters = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(OUTPUT_DIR, f"{safe_title}.%(ext)s"),
            "quiet": False,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "extractaudio": True,
        }
    else:
        # Configurações para vídeo (default)
        OUTPUT_DIR = os.path.join(BASE_DIR, safe_title, "video")
        file_ext = "mp4"
        file_type = "vídeo"
        ydl_parameters = {
            "format": "best[ext=mp4]/bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "outtmpl": os.path.join(OUTPUT_DIR, f"{safe_title}.%(ext)s"),
            "quiet": False,
            "postprocessors": [
                {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
            ],
        }

    # Cria a estrutura de pastas
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with yt_dlp.YoutubeDL(ydl_parameters) as ydl:
        try:
            print(f"\nBaixando {file_type}: {video_title}")
            ydl.download([link])

            print(f"\nDownload concluído com sucesso!")
            print(f"Pasta principal: {BASE_DIR}")
            print(f"Subpasta: {safe_title}/{'audio' if choice == 'a' else 'video'}")
            print(f"Arquivo: {safe_title}.{file_ext}")

        except Exception as e:
            print(f"Erro durante o download: {e}")
            return

    print(f"\nOperação finalizada!")
