from __future__ import annotations

import os
import platform
import re
import unicodedata


def sanitize_filename(filename: str) -> str:
    sanitized = unicodedata.normalize("NFKD", filename)
    sanitized = "".join(c for c in sanitized if not unicodedata.combining(c))
    sanitized = re.sub(r"[^\w\s-]", "", sanitized)
    sanitized = re.sub(r"[\s]+", "_", sanitized)
    return sanitized.strip("_")


def clear_terminal() -> None:
    os.system("cls" if platform.system() == "Windows" else "clear")
