from __future__ import annotations

import inquirer
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)
from rich.rule import Rule

console = Console()


def print_header(title: str) -> None:
    console.print(
        Panel(
            f"[bold cyan]{title}[/bold cyan]",
            style="blue",
            border_style="bright_blue",
        )
    )


def print_menu(show_deno_option: bool = False) -> str:
    choices = [
        ("Baixar vídeo individual", "v"),
        ("Baixar playlist completa", "p"),
    ]
    if show_deno_option:
        choices.append(("Instalar Deno (melhorar downloads)", "d"))
    choices.append(("Sair", "q"))

    questions = [
        inquirer.List(
            "action",
            message="O que deseja fazer?",
            choices=choices,
        )
    ]
    return inquirer.prompt(questions)["action"]


def prompt_url(message: str = "URL do YouTube") -> str:
    questions = [
        inquirer.Text(
            "url",
            message=message,
            validate=lambda _, x: len(x.strip()) > 0,
        )
    ]
    return inquirer.prompt(questions)["url"].strip()


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


def prompt_deno_install() -> bool:
    questions = [
        inquirer.Confirm(
            "install",
            message="Deseja instalar o Deno agora?",
        )
    ]
    return inquirer.prompt(questions)["install"]


def print_success(message: str) -> None:
    console.print()
    console.print(Rule(style="green"))
    console.print(f"[bold green]✓ {message}[/bold green]")
    console.print(Rule(style="green"))


def print_error(message: str) -> None:
    console.print()
    console.print(Rule(style="red"))
    console.print(f"[bold red]✗ Erro: {message}[/bold red]")
    console.print(Rule(style="red"))


def print_info(message: str) -> None:
    console.print()
    console.print(f"[bold cyan]→ {message}[/bold cyan]")


def print_warning(message: str) -> None:
    console.print()
    console.print(
        Panel(
            f"[yellow]{message}[/yellow]",
            style="yellow",
            border_style="yellow",
            title="⚠ Atenção",
        )
    )


def create_progress() -> Progress:
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None),
        DownloadColumn(binary_units=True),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        console=console,
        transient=True,
    )


def create_playlist_progress() -> Progress:
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None),
        "[progress.percentage]{task.percentage:>3.0f}%",
        DownloadColumn(binary_units=True),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        console=console,
        transient=True,
        expand=True,
    )
