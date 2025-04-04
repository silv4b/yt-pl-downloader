import playlist_downloader as pld
import video_downloader as vd


def choose_between_video_playlist() -> str:
    print("Deseja baixar vídeo ou playlist")
    print("[V] Vídeo, [P]: Playlist.", end=" ")
    opc = input(": ")
    if opc.lower().strip() == "v":
        return "video"
    elif opc.lower().strip() == "p":
        return "playlist"


def main() -> None:
    print("[Enter para sair]")
    opc_download = choose_between_video_playlist()
    if opc_download == "video":
        vd.video_downloader()
    elif opc_download == "playlist":
        pld.download_playlist()
    else:
        print("Saindo ...")
        exit(1)


if __name__ == "__main__":
    print("Youtube Downloader")
    main()
