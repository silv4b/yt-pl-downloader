"""Script de build para gerar executável do YouTube Downloader.

Usa PyInstaller com configurações otimizadas para empacotar
todas as dependências (yt-dlp, Rich, inquirer, PyYAML).

Uso:
    python build.py
"""

import os
import shutil
import subprocess
import sys


def main():
    print("=" * 50)
    print("  YouTube Downloader - Build")
    print("=" * 50)

    # Limpar builds anteriores
    for path in ["build", "dist", "__pycache__"]:
        if os.path.exists(path):
            try:
                shutil.rmtree(path)
                print(f"[INFO] Removido: {path}/")
            except PermissionError:
                print(f"[AVISO] Não foi possível remover {path}/ — arquivo em uso")

    name = "yt-pl-downloader"
    platform_suffix = "-win" if sys.platform == "win32" else "-linux"
    output_name = f"{name}{platform_suffix}"

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--name",
        output_name,
        "--collect-all",
        "yt_dlp",
        "--collect-all",
        "rich",
        "--hidden-import",
        "inquirer",
        "--hidden-import",
        "yaml",
        "--hidden-import",
        "readchar",
        "--copy-metadata",
        "readchar",
        "--copy-metadata",
        "inquirer",
        "main.py",
    ]

    print(f"\n[INFO] Executando: {' '.join(cmd)}\n")

    result = subprocess.run(cmd)

    if result.returncode == 0:
        print(f"\n{'=' * 50}")
        print("\tBuild concluído com sucesso!")
        print(f"{'=' * 50}")
        print(f"\nExecutável: dist/{output_name}{'.exe' if sys.platform == 'win32' else ''}")
    else:
        print("\n[ERRO] Build falhou!")
        sys.exit(1)


if __name__ == "__main__":
    main()
