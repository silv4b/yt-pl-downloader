"""Módulo de interface de usuário para o terminal.

Combina inquirer para prompts interativos (navegação com setas e Enter)
com Rich para output visual (painéis, barras de progresso, regras coloridas).
"""

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


def _prompt(questions: list) -> dict:
    """Executa um prompt do inquirer e retorna o resultado.

    Lança KeyboardInterrupt se o usuário cancelar com Ctrl+C.

    Args:
        questions: Lista de objetos de pergunta do inquirer.

    Returns:
        Dicionário com as respostas do usuário.
    """
    result = inquirer.prompt(questions)
    if result is None:
        raise KeyboardInterrupt()
    return result


def print_header(title: str) -> None:
    """Exibe um cabeçalho estilizado em painel no topo do terminal."""
    console.print(
        Panel(
            f"[bold cyan]{title}[/bold cyan]",
            style="blue",
            border_style="bright_blue",
        )
    )


def print_menu(show_deno_option: bool = False) -> str:
    """Exibe o menu principal de ações e retorna a escolha do usuário.

    Args:
        show_deno_option: Se True, inclui a opção "Instalar Deno" no menu.

    Returns:
        Um dos valores: "v" (vídeo), "p" (playlist), "d" (deno), "q" (sair).
    """
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
    return _prompt(questions)["action"]


def prompt_url(message: str = "URL do YouTube") -> str:
    """Solicita ao usuário uma URL do YouTube com validação.

    Args:
        message: Mensagem customizada do prompt (padrão: "URL do YouTube").

    Returns:
        A string da URL inserida pelo usuário, sem espaços extras.
    """
    questions = [
        inquirer.Text(
            "url",
            message=message,
            validate=lambda _, x: len(x.strip()) > 0,
        )
    ]
    return _prompt(questions)["url"].strip()


def prompt_format() -> bool:
    """Solicita ao usuário a escolha entre formato de vídeo (MP4) e áudio (MP3).

    Returns:
        True se o formato de áudio foi selecionado, False para vídeo.
    """
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
    return _prompt(questions)["format"] == "audio"


def prompt_ffmpeg_install() -> bool:
    """Pergunta ao usuário se deseja instalar o FFmpeg.

    Returns:
        True se o usuário confirmou a instalação.
    """
    questions = [
        inquirer.Confirm(
            "install",
            message="FFmpeg não encontrado. Deseja instalar agora?",
        )
    ]
    return _prompt(questions)["install"]


def prompt_deno_install() -> bool:
    """Pergunta ao usuário se deseja instalar o Deno.

    Returns:
        True se o usuário confirmou a instalação.
    """
    questions = [
        inquirer.Confirm(
            "install",
            message="Deseja instalar o Deno agora?",
        )
    ]
    return _prompt(questions)["install"]


def print_success(message: str) -> None:
    """Exibe uma mensagem de sucesso com estilização verde e regras."""
    console.print()
    console.print(Rule(style="green"))
    console.print(f"[bold green]✓ {message}[/bold green]")
    console.print(Rule(style="green"))


def print_error(message: str) -> None:
    """Exibe uma mensagem de erro com estilização vermelha e regras."""
    console.print()
    console.print(Rule(style="red"))
    console.print(f"[bold red]✗ Erro: {message}[/bold red]")
    console.print(Rule(style="red"))


def print_info(message: str) -> None:
    """Exibe uma mensagem informativa em ciano."""
    console.print()
    console.print(f"[bold cyan]→ {message}[/bold cyan]")


def print_warning(message: str) -> None:
    """Exibe uma mensagem de aviso dentro de um painel com borda amarela."""
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
    """Cria uma instância de Progress do Rich para downloads de vídeo único.

    Inclui: spinner, descrição, barra, bytes baixados/total,
    velocidade de transferência e tempo estimado restante.

    Returns:
        Instância de Progress configurada e vinculada ao console.
    """
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
    """Cria uma instância de Progress do Rich para downloads de playlist.

    Inclui: spinner, descrição, barra, porcentagem, bytes baixados/total,
    velocidade de transferência e tempo estimado restante. Suporta exibição
    de duas tarefas simultâneas (playlist geral + vídeo atual).

    Returns:
        Instância de Progress configurada com modo expand ativado.
    """
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
