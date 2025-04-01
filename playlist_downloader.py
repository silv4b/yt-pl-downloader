import os
import yt_dlp
import re
import unicodedata


def remove_accents(text):
    """Remove acentos de caracteres Unicode."""
    normalized_text = unicodedata.normalize("NFKD", text)
    return "".join([c for c in normalized_text if not unicodedata.combining(c)])


def sanitize_filename(filename):
    """Normaliza e sanitiza nomes de arquivos removendo acentos, espaços e caracteres inválidos."""
    filename = remove_accents(filename)
    filename = re.sub(r"[^\w\s-]", "", filename)  # Remove caracteres especiais
    filename = re.sub(r"[\s]+", "_", filename)  # Substitui espaços por underlines
    return filename.strip()


link = input("URL da Playlist do YT: ✨ ")

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
    download_dir = "downloads"
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
                new_names.append((temp_filepath, os.path.join(playlist_path, new_name)))
            except Exception as e:
                print(f"❌ Erro ao baixar {video['title']}: {e}")

    # for old_name, new_name in new_names:
    #     try:
    #         if os.path.exists(old_name):
    #             os.rename(old_name, new_name)
    #             print(f"✅ Renomeado: {old_name} -> {new_name}")
    #         else:
    #             print(f"❌ Erro: Arquivo {old_name} não encontrado")
    #     except Exception as e:
    #         print(f"❌ Erro ao renomear {old_name}: {e}")

print("\n" + "=" * 40)
print("🎉 Todos os vídeos baixados e renomeados com sucesso! 🎉")
print("=" * 40)

