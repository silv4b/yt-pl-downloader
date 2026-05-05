import os
import yt_dlp
from app.core.utils import sanitize_filename


def choose_between_video_or_audio() -> dict:
    print("Deseja baixar vídeos (.mp4) ou áudios (.mp3)")
    print("[V] Vídeo (default), [A]: Áudio.", end=" ")
    format = input(": ")

    if format.lower().strip() == "v":
        print("Extraindo vídeos da playlist.")
        return {
            "format": "best[ext=mp4]/bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "noplaylist": False,
            "quiet": False,
            "postprocessors": [
                {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
            ],
        }, "video"
    elif format.lower().strip() == "a":
        print("Extraindo áudios da playlist.")
        return {
            "format": "bestaudio/best",
            "merge_output_format": "mp3",
            "noplaylist": False,
            "quiet": False,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "extractaudio": True,
        }, "audio"
    else:
        print("Erro ...")
        exit(1)


def download_playlist(link: str) -> None:
    if link.strip() == "":
        print("Nenhum link fornecido, encerrando.")
        exit(1)

    download_dir = "downloads"
    ydl_options = choose_between_video_or_audio()
    ydl_parameters = ydl_options[0]
    ydl_format = ydl_options[1]

    with yt_dlp.YoutubeDL(ydl_parameters) as ydl:
        try:
            playlist_info = ydl.extract_info(link, download=False)
        except Exception as e:
            print(f"Erro ao extrair informação da playlist: {e}")
            exit(1)

        playlist_title = sanitize_filename(playlist_info["title"])
        playlist_path = os.path.join(
            download_dir, "downloaded_playlists", playlist_title, ydl_format
        )

        os.makedirs(
            playlist_path, exist_ok=True
        )  # cria a pasta de downloads para os playlists

        total_video_count = len(playlist_info["entries"])
        print("\nTotal de vídeos na playlist: 🎦", total_video_count)

        for index, video in enumerate(playlist_info["entries"], start=1):
            sanitized_title = sanitize_filename(video["title"])
            temp_filename = f"{index:02d}_{sanitized_title}.mp4"
            temp_filepath = os.path.join(playlist_path, temp_filename)
            ydl_parameters["outtmpl"] = temp_filepath

            with yt_dlp.YoutubeDL(ydl_parameters) as ydl2:
                try:
                    print(f"\nBaixando ({index}/{total_video_count}): {video['title']}")
                    ydl2.download([video["webpage_url"]])
                    print(f"Baixado: {video['title']} com sucesso!")
                    print(f"Vídeos restantes: {total_video_count - index}")
                except Exception as e:
                    print(f"Erro ao baixar {video['title']}: {e}")

    print("🎉 Todos os arquivos foram baixados e renomeados com sucesso! 🎉")


def playlist_downloader() -> None:
    print("Youtube Playlist Downloader [Enter para sair]")
    download_playlist(link=input("URL da Playlist do YouTube ✨: "))
