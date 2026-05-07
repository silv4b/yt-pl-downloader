"""Detecção e seleção de qualidade de vídeo.

Detecta as resoluções disponíveis nos metadados do yt-dlp
e permite ao usuário escolher com menu interativo (setas + Enter).
"""

from __future__ import annotations

import inquirer
import yt_dlp

from app.cli.menu import _prompt


def _extract_first_video_formats(url: str) -> list[dict]:
    """Extrai formatos do primeiro vídeo disponível na URL.

    Para vídeos individuais, retorna os formatos diretamente.
    Para playlists, pega o primeiro vídeo da lista e extrai seus formatos.

    Args:
        url: URL do vídeo ou playlist do YouTube.

    Returns:
        Lista de dicionários de formatos do yt-dlp.
    """
    opts = {"quiet": True, "no_warnings": True}
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)

    # Se é um vídeo individual
    formats = info.get("formats")
    if formats:
        return formats

    # Se é uma playlist, pega o primeiro vídeo válido
    entries = info.get("entries") or []
    for entry in entries:
        if entry is None:
            continue
        entry_url = entry.get("webpage_url") or entry.get("url")
        if not entry_url:
            continue
        with yt_dlp.YoutubeDL(opts) as ydl:
            video_info = ydl.extract_info(entry_url, download=False)
        return video_info.get("formats") or []

    return []


def _get_available_qualities(info: dict, url: str) -> list[tuple[str, str]]:
    """Detecta as resoluções de vídeo disponíveis nos metadados do yt-dlp.

    Retorna uma lista de tuplas (label, yt-dlp_format) ordenadas por resolução.

    Args:
        info: Dicionário de metadados retornado por _extract_info().
        url: URL original (usada para extrair formatos do primeiro vídeo).

    Returns:
        Lista de tuplas com (descrição amigável, filtro yt-dlp).
        Inclui sempre uma opção "Melhor disponível".
    """
    formats = info.get("formats") or _extract_first_video_formats(url)
    resolutions = set()

    for fmt in formats:
        h = fmt.get("height")
        if h:
            resolutions.add(h)

    ordered = sorted(resolutions, reverse=True)
    choices = [("Melhor disponível", "best")]
    for res in ordered:
        label = f"{res}p"
        yt_filter = (
            f"bestvideo[height<={res}][vcodec^=avc1]+bestaudio/"
            f"bestvideo[height<={res}]+bestaudio/best[height<={res}]/best"
        )
        choices.append((label, yt_filter))

    return choices


def prompt_quality(info: dict, url: str) -> str:
    """Exibe as qualidades de vídeo disponíveis e permite ao usuário escolher.

    Usa inquirer.List para navegação com setas. A opção 1080p é
    selecionada por padrão se disponível.

    Args:
        info: Dicionário de metadados do yt-dlp com informações do vídeo.
        url: URL original (usada para extrair formatos do primeiro vídeo).

    Returns:
        Filtro de formato do yt-dlp correspondente à qualidade escolhida.
    """
    choices = _get_available_qualities(info, url)
    labels = [c[0] for c in choices]
    mapping = {c[0]: c[1] for c in choices}

    default = "1080p"
    if default not in labels:
        default = labels[1] if len(labels) > 1 else labels[0]

    questions = [
        inquirer.List(
            "quality",
            message="Qualidade do vídeo",
            choices=labels,
            default=default,
        )
    ]
    selected = _prompt(questions)["quality"]
    return mapping[selected]
