import os
import yt_dlp
from core.utils import make_alpha_numeric


def video_downloader() -> None:
    OUTPUT_DIR = "downloads/downloaded_videos_only"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    link = input("Enter YouTube Video URL: ✨ ")

    ydl_parameters = {
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": os.path.join(OUTPUT_DIR, "%(title)s.%(ext)s"),
        "quiet": False,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
    }

    with yt_dlp.YoutubeDL(ydl_parameters) as ydl:
        try:
            video_info = ydl.extract_info(link, download=False)
            video_title = make_alpha_numeric(video_info["title"])
            print(f"\nBaixando: {video_title}")
            ydl.download([link])
            print(f"\nBaixando: {video_title} ✨ com sucesso!")
            print(f"Salvo em: {OUTPUT_DIR}")
        except Exception as e:
            print(f"Erro ao baixar vídeo: {e}")

    print("\nVídeo baixando com sucesso! 🎉")
