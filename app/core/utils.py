"""Utilitários para sanitização de nomes de arquivo e controle do terminal."""

from __future__ import annotations

import os
import platform
import re
import unicodedata


def sanitize_filename(filename: str) -> str:
    """Converte uma string em um nome de arquivo válido para o sistema.

    Remove acentos, caracteres especiais e substitui espaços por
    underscores. Remove underscores no início e no final do resultado.

    Args:
        filename: A string original a ser sanitizada.

    Returns:
        Um nome de arquivo limpo e seguro para uso em qualquer sistema.
    """
    sanitized = unicodedata.normalize("NFKD", filename)
    sanitized = "".join(c for c in sanitized if not unicodedata.combining(c))
    sanitized = re.sub(r"[^\w\s-]", "", sanitized)
    sanitized = re.sub(r"[\s]+", "_", sanitized)
    return sanitized.strip("_")


def clear_terminal() -> None:
    """Limpa a tela do terminal usando o comando apropriado do sistema."""
    os.system("cls" if platform.system() == "Windows" else "clear")
