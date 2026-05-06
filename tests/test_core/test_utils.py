"""Testes unitários para os utilitários de sanitização de nomes de arquivo."""

from app.core.utils import sanitize_filename


def test_sanitize_filename_removes_accents():
    """Verifica se acentos são removidos corretamente."""
    assert sanitize_filename("café") == "cafe"


def test_sanitize_filename_removes_special_chars():
    """Verifica se caracteres especiais são removidos."""
    assert sanitize_filename("video<name>.txt") == "videonametxt"


def test_sanitize_filename_replaces_spaces():
    """Verifica se espaços são substituídos por underscores."""
    assert sanitize_filename("my video title") == "my_video_title"


def test_sanitize_filename_strips_underscores():
    """Verifica se underscores no início e fim são removidos."""
    assert sanitize_filename("__video__") == "video"


def test_sanitize_filename_preserves_alphanumeric():
    """Verifica se caracteres alfanuméricos são preservados."""
    assert sanitize_filename("Video123") == "Video123"
