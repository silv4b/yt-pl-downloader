"""Testes unitários para o módulo de detecção de qualidade de vídeo."""

from unittest.mock import patch

from app.cli.quality import (
    _extract_first_video_formats,
    _get_available_qualities,
    prompt_quality,
)


def test_get_available_qualities_from_info():
    """Verifica que resoluções são extraídas corretamente dos metadados."""
    info = {
        "formats": [
            {"height": 1080},
            {"height": 720},
            {"height": 480},
            {"height": 360},
            {"height": None},
        ]
    }
    choices = _get_available_qualities(info, "https://example.com")
    labels = [c[0] for c in choices]
    assert "Melhor disponível" in labels
    assert "1080p" in labels
    assert "720p" in labels
    assert "480p" in labels
    assert "360p" in labels


def test_get_available_qualities_sorted_descending():
    """Verifica que resoluções são ordenadas do maior para o menor."""
    info = {
        "formats": [
            {"height": 360},
            {"height": 1080},
            {"height": 720},
        ]
    }
    choices = _get_available_qualities(info, "https://example.com")
    labels = [c[0] for c in choices]
    expected = ["Melhor disponível", "1080p", "720p", "360p"]
    assert labels == expected


def test_get_available_qualities_with_empty_formats():
    """Verifica que apenas 'Melhor disponível' aparece sem formatos."""
    mock_formats = []
    with patch("yt_dlp.YoutubeDL") as mock_ydl:
        mock_ydl.return_value.__enter__ = lambda self: self
        mock_ydl.return_value.__exit__ = lambda self, *a: None
        mock_ydl.return_value.extract_info.return_value = {"formats": mock_formats, "entries": []}
        choices = _get_available_qualities({"formats": []}, "https://example.com")
        assert len(choices) == 1
        assert choices[0][0] == "Melhor disponível"


def test_get_available_qualities_filter_contains_h264():
    """Verifica que o filtro de qualidade inclui o codec H.264."""
    info = {"formats": [{"height": 1080}]}
    choices = _get_available_qualities(info, "https://example.com")
    mapping = {c[0]: c[1] for c in choices}
    assert "vcodec^=avc1" in mapping["1080p"]


def test_extract_first_video_formats_returns_formats():
    """Verifica que formatos são extraídos quando info contém 'formats'."""
    mock_info = {"formats": [{"height": 1080}]}
    with patch("yt_dlp.YoutubeDL") as mock_ydl:
        mock_ydl.return_value.__enter__ = lambda self: self
        mock_ydl.return_value.__exit__ = lambda self, *a: None
        mock_ydl.return_value.extract_info.return_value = mock_info
        formats = _extract_first_video_formats("https://example.com")
        assert formats == [{"height": 1080}]


def test_extract_first_video_formats_from_playlist():
    """Verifica que formatos são extraídos do primeiro vídeo em playlists."""
    playlist_info = {
        "formats": None,
        "entries": [
            {"webpage_url": "https://example.com/video1"},
            {"webpage_url": "https://example.com/video2"},
        ],
    }
    video_info = {"formats": [{"height": 720}]}
    with patch("yt_dlp.YoutubeDL") as mock_ydl:
        mock_ydl.return_value.__enter__ = lambda self: self
        mock_ydl.return_value.__exit__ = lambda self, *a: None
        mock_ydl.return_value.extract_info.side_effect = [
            playlist_info,
            video_info,
        ]
        formats = _extract_first_video_formats("https://example.com/playlist")
        assert formats == [{"height": 720}]


def test_extract_first_video_formats_empty_playlist():
    """Verifica que lista vazia é retornada para playlist sem vídeos."""
    playlist_info = {"formats": None, "entries": []}
    with patch("yt_dlp.YoutubeDL") as mock_ydl:
        mock_ydl.return_value.__enter__ = lambda self: self
        mock_ydl.return_value.__exit__ = lambda self, *a: None
        mock_ydl.return_value.extract_info.return_value = playlist_info
        formats = _extract_first_video_formats("https://example.com/playlist")
        assert formats == []


def test_prompt_quality_returns_selected_filter():
    """Verifica que prompt_quality retorna o filtro da qualidade selecionada."""
    info = {"formats": [{"height": 1080}, {"height": 720}]}
    with patch("app.cli.quality._prompt", return_value={"quality": "720p"}):
        result = prompt_quality(info, "https://example.com")
        assert "720" in result


def test_prompt_quality_defaults_to_1080p():
    """Verifica que prompt_quality usa 1080p como padrão quando disponível."""
    info = {"formats": [{"height": 1080}]}
    with patch("app.cli.quality._prompt", return_value={"quality": "1080p"}):
        result = prompt_quality(info, "https://example.com")
        assert "1080" in result


def test_prompt_quality_fallback_when_1080p_unavailable():
    """Verifica que prompt_quality usa primeira opção quando 1080p não está disponível."""
    info = {"formats": [{"height": 720}]}
    with patch("app.cli.quality._prompt", return_value={"quality": "720p"}):
        result = prompt_quality(info, "https://example.com")
        assert "720" in result
