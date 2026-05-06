"""Configuração de logging estruturado para o aplicativo.

Fornece uma instância de logger pré-configurada que envia
saída para stdout com formatação de timestamp e nível de log.
"""

from __future__ import annotations

import logging
import sys


def setup_logger(name: str = "yt-pl-downloader") -> logging.Logger:
    """Cria ou retorna uma instância de logger configurada.

    Configura logging em nível INFO com formatação de timestamp no stdout.
    Configura os handlers apenas uma vez para evitar saída duplicada.

    Args:
        name: Nome do logger, padrão é o nome do aplicativo.

    Returns:
        Instância do Logger configurada.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


logger = setup_logger()
