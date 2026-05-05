from __future__ import annotations

import inquirer


def print_header(text: str) -> None:
    print(f"\n{'=' * 40}")
    print(f"  {text}")
    print(f"{'=' * 40}")


def prompt_main_action() -> str:
    questions = [
        inquirer.List(
            "action",
            message="O que deseja fazer?",
            choices=[
                ("Baixar vídeo individual", "video"),
                ("Baixar playlist completa", "playlist"),
                ("Sair", "quit"),
            ],
        )
    ]
    return inquirer.prompt(questions)["action"]


def prompt_url() -> str:
    questions = [
        inquirer.Text(
            "url",
            message="URL do YouTube",
            validate=lambda _, x: len(x) > 0,
        )
    ]
    return inquirer.prompt(questions)["url"]


def prompt_format() -> bool:
    questions = [
        inquirer.List(
            "format",
            message="Formato de saída",
            choices=[
                ("Vídeo (MP4)", "video"),
                ("Áudio (MP3)", "audio"),
            ],
        )
    ]
    return inquirer.prompt(questions)["format"] == "audio"


def prompt_ffmpeg_install() -> bool:
    questions = [
        inquirer.Confirm(
            "install",
            message="FFmpeg não encontrado. Deseja instalar agora?",
        )
    ]
    return inquirer.prompt(questions)["install"]


def print_success(message: str) -> None:
    print(f"\n✓ {message}")


def print_error(message: str) -> None:
    print(f"\n✗ Erro: {message}")


def print_info(message: str) -> None:
    print(f"\n→ {message}")
