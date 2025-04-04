import os
import yt_dlp


def make_alpha_numeric(string: str) -> str:
    cleaned_string = ""
    for char in string:
        if char.isalnum():
            cleaned_string += char
    return cleaned_string


def video_downloader() -> None:
    OUTPUT_DIR = "downloads/downloaded_videos_only"

    # Cria as pastas se não existirem
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    link = input("Enter YouTube Video URL: ✨ ")

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": os.path.join(OUTPUT_DIR, "%(title)s.%(ext)s"),  # Salva na subpasta
        "quiet": False,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            video_info = ydl.extract_info(link, download=False)
            video_title = make_alpha_numeric(video_info["title"])

            print(f"\nDownloading: {video_title}")
            ydl.download([link])
            print(f"\nDownloaded: {video_title} ✨ successfully!")
            print(f"Saved to: {OUTPUT_DIR}")

        except Exception as e:
            print(f"Error downloading video: {e}")

    print("\nVideo downloaded successfully! 🎉")
