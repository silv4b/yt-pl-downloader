from app.services.playlist import playlist_downloader
from app.services.video import video_downloader
from app.core.utils import clear_terminal
from app.core.ffmpeg_utils import verify_ffmpeg_installed, install_ffmpeg
from app.core.utils import clear_terminal


def check_and_install_ffmpeg() -> bool:
    """Verifica e instala o FFmpeg em uma interação com o usuário"""
    if not verify_ffmpeg_installed():
        clear_terminal()
        print("FFmpeg não encontrado (necessário para conversão de formatos)")
        print("Deseja instalar agora? [Y/N]: ", end="")
        choice = input().lower()

        if choice == "y":
            try:
                install_ffmpeg()
                print("FFmpeg instalado com sucesso! ✔️")
                return True
            except Exception as e:
                print(f"Falha na instalação: {e} ❌")
                return False
        else:
            print("Operação cancelada pelo usuário ⚠️")
            return False
    return True


def choose_between_video_playlist() -> str:
    """Verifica se o usuário quer baixar vídeo ou playlist"""
    print("\nDeseja baixar:")
    print("[V] Vídeo individual")
    print("[P] Playlist completa")
    print("[Q] Sair")
    choice = input("Opção: ").lower().strip()
    return choice


def main() -> None:
    clear_terminal()
    print("=== YouTube Downloader ===")

    # Verificação inicial do FFmpeg
    if not check_and_install_ffmpeg():
        exit(1)

    while True:
        choice = choose_between_video_playlist()

        if choice == "v":
            video_downloader()
        elif choice == "p":
            playlist_downloader()
        elif choice == "q":
            print("Saindo...")
            break
        else:
            print("Opção inválida! Tente novamente.")


if __name__ == "__main__":
    main()
