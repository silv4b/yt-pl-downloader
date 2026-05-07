"""Testes unitários para funções de interface do menu CLI."""

from unittest.mock import patch

import pytest

from app.cli.menu import (
    _prompt,
    display_playlist_entries,
    open_folder,
    print_error,
    print_header,
    print_info,
    print_menu,
    print_success,
    print_warning,
    prompt_deno_install,
    prompt_ffmpeg_install,
    prompt_format,
    prompt_open_folder,
    prompt_url,
    update_playlist_status,
)


def test_prompt_raises_keyboard_interrupt_on_none():
    """Verifica que _prompt levanta KeyboardInterrupt quando resultado é None."""
    with patch("app.cli.menu.inquirer.prompt", return_value=None):
        with pytest.raises(KeyboardInterrupt):
            _prompt([])


def test_prompt_returns_result():
    """Verifica que _prompt retorna o resultado do inquirer."""
    expected = {"key": "value"}
    with patch("app.cli.menu.inquirer.prompt", return_value=expected):
        result = _prompt([])
        assert result == expected


def test_print_header_renders_panel(capsys):
    """Verifica que print_header exibe um painel estilizado."""
    print_header("Test Title")
    captured = capsys.readouterr()
    assert "Test Title" in captured.out


def test_print_menu_without_deno_option():
    """Verifica que print_menu funciona sem opção Deno."""
    with patch("app.cli.menu._prompt", return_value={"action": "v"}):
        result = print_menu(show_deno_option=False)
        assert result == "v"


def test_print_menu_with_deno_option():
    """Verifica que print_menu funciona com opção Deno."""
    with patch("app.cli.menu._prompt", return_value={"action": "d"}):
        result = print_menu(show_deno_option=True)
        assert result == "d"


def test_prompt_url_with_custom_message():
    """Verifica que prompt_url usa mensagem customizada."""
    with patch("app.cli.menu._prompt", return_value={"url": "https://example.com"}):
        result = prompt_url("Custom message")
        assert result == "https://example.com"


def test_prompt_url_strips_whitespace():
    """Verifica que prompt_url remove espaços extras."""
    with patch("app.cli.menu._prompt", return_value={"url": "  https://example.com  "}):
        result = prompt_url()
        assert result == "https://example.com"


def test_prompt_format_returns_true_for_audio():
    """Verifica que prompt_format retorna True quando áudio é selecionado."""
    with patch("app.cli.menu._prompt", return_value={"format": "audio"}):
        assert prompt_format() is True


def test_prompt_format_returns_false_for_video():
    """Verifica que prompt_format retorna False quando vídeo é selecionado."""
    with patch("app.cli.menu._prompt", return_value={"format": "video"}):
        assert prompt_format() is False


def test_prompt_ffmpeg_install_returns_true():
    """Verifica que prompt_ffmpeg_install retorna True quando confirmado."""
    with patch("app.cli.menu._prompt", return_value={"install": True}):
        assert prompt_ffmpeg_install() is True


def test_prompt_ffmpeg_install_returns_false():
    """Verifica que prompt_ffmpeg_install retorna False quando negado."""
    with patch("app.cli.menu._prompt", return_value={"install": False}):
        assert prompt_ffmpeg_install() is False


def test_prompt_deno_install_returns_true():
    """Verifica que prompt_deno_install retorna True quando confirmado."""
    with patch("app.cli.menu._prompt", return_value={"install": True}):
        assert prompt_deno_install() is True


def test_prompt_deno_install_returns_false():
    """Verifica que prompt_deno_install retorna False quando negado."""
    with patch("app.cli.menu._prompt", return_value={"install": False}):
        assert prompt_deno_install() is False


def test_print_success_renders(capsys):
    """Verifica que print_success exibe mensagem."""
    print_success("Done!")
    captured = capsys.readouterr()
    assert "Done!" in captured.out


def test_print_error_renders(capsys):
    """Verifica que print_error exibe mensagem."""
    print_error("Failed!")
    captured = capsys.readouterr()
    assert "Failed!" in captured.out


def test_print_info_renders(capsys):
    """Verifica que print_info exibe mensagem."""
    print_info("Info message")
    captured = capsys.readouterr()
    assert "Info message" in captured.out


def test_print_warning_renders(capsys):
    """Verifica que print_warning exibe mensagem."""
    print_warning("Warning message")
    captured = capsys.readouterr()
    assert "Warning message" in captured.out


def test_display_playlist_entries_renders_table(capsys):
    """Verifica que a tabela de vídeos da playlist é exibida corretamente."""
    entries = [
        {"title": "Video One"},
        {"title": "Video Two"},
        None,
    ]
    display_playlist_entries(entries)
    captured = capsys.readouterr()
    assert "Video One" in captured.out
    assert "Video Two" in captured.out
    assert "Pendente" in captured.out
    assert "Indisponível" in captured.out


def test_update_playlist_status_shows_completed(capsys):
    """Verifica que vídeos concluídos são marcados com ✓."""
    entries = [
        {"title": "Video One"},
        {"title": "Video Two"},
    ]
    update_playlist_status(entries, {1}, set(), None)
    captured = capsys.readouterr()
    assert "Concluído" in captured.out


def test_update_playlist_status_shows_failed(capsys):
    """Verifica que vídeos com falha são marcados com ✗."""
    entries = [
        {"title": "Video One"},
        {"title": "Video Two"},
    ]
    update_playlist_status(entries, set(), {1}, None)
    captured = capsys.readouterr()
    assert "Falhou" in captured.out


def test_update_playlist_status_shows_downloading(capsys):
    """Verifica que o vídeo sendo baixado é destacado."""
    entries = [
        {"title": "Video One"},
        {"title": "Video Two"},
    ]
    update_playlist_status(entries, set(), set(), 1)
    captured = capsys.readouterr()
    assert "Baixando" in captured.out


def test_update_playlist_status_shows_pending(capsys):
    """Verifica que vídeos não iniciados aparecem como pendentes."""
    entries = [
        {"title": "Video One"},
        {"title": "Video Two"},
        {"title": "Video Three"},
    ]
    update_playlist_status(entries, {1}, set(), None)
    captured = capsys.readouterr()
    assert "Pendente" in captured.out


def test_prompt_open_folder_returns_true():
    """Verifica que prompt_open_folder retorna True quando confirmado."""
    with patch("app.cli.menu._prompt", return_value={"open": True}):
        assert prompt_open_folder("/some/path") is True


def test_prompt_open_folder_returns_false():
    """Verifica que prompt_open_folder retorna False quando negado."""
    with patch("app.cli.menu._prompt", return_value={"open": False}):
        assert prompt_open_folder("/some/path") is False


def test_open_folder_linux(monkeypatch):
    """Verifica que open_folder usa xdg-open no Linux."""
    import platform
    import subprocess

    calls = []

    class MockPopen:
        def __init__(self, args):
            calls.append(args)

    with monkeypatch.context() as m:
        m.setattr(platform, "system", lambda: "Linux")
        m.setattr(subprocess, "Popen", MockPopen)
        open_folder("/test/path")
        assert ["xdg-open", "/test/path"] in calls


def test_open_folder_windows(monkeypatch):
    """Verifica que open_folder usa os.startfile no Windows."""
    import platform

    call_args = []

    def mock_startfile(path):
        call_args.append(path)

    with monkeypatch.context() as m:
        m.setattr(platform, "system", lambda: "Windows")
        m.setattr("os.startfile", mock_startfile)
        open_folder("C:\\test\\path")
        assert call_args == ["C:\\test\\path"]


def test_open_folder_macos(monkeypatch):
    """Verifica que open_folder usa 'open' no macOS."""
    import platform
    import subprocess

    calls = []

    class MockPopen:
        def __init__(self, args):
            calls.append(args)

    with monkeypatch.context() as m:
        m.setattr(platform, "system", lambda: "Darwin")
        m.setattr(subprocess, "Popen", MockPopen)
        open_folder("/Applications")
        assert ["open", "/Applications"] in calls
