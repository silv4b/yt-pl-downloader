"""Configuração centralizada para o downloader do YouTube.

Carrega configurações do config.yaml com valores padrão de fallback
e fornece acesso tipado aos caminhos de download e opções de formato.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

_DEFAULTS = {
    "downloads_dir": "downloads",
    "video_subdir": "downloaded_videos",
    "playlist_subdir": "downloaded_playlists",
    "default_video_format": "mp4",
    "default_audio_format": "mp3",
    "audio_quality": "192",
}


def _find_config_path() -> Path:
    """Localiza o arquivo config.yaml buscando nos diretórios do projeto.

    Busca primeiro na raiz do pacote e depois no diretório de trabalho atual.

    Returns:
        Caminho para o config.yaml (mesmo que não exista).
    """
    for base in [Path(__file__).parent.parent.parent, Path.cwd()]:
        path = base / "config.yaml"
        if path.exists():
            return path
    return Path.cwd() / "config.yaml"


def _load_config() -> dict:
    """Carrega a configuração do config.yaml, mesclando com valores padrão.

    Se o config.yaml não existir, retorna apenas os valores padrão.

    Returns:
        Dicionário contendo todas as chaves de configuração.
    """
    config_path = _find_config_path()
    if not config_path.exists():
        return dict(_DEFAULTS)
    with open(config_path, encoding="utf-8") as f:
        loaded = yaml.safe_load(f) or {}
    return {**_DEFAULTS, **loaded}


@dataclass(frozen=True)
class DownloadConfig:
    """Configuração imutável para caminhos de download e opções de formato.

    Attributes:
        base_dir: Diretório raiz para todos os downloads.
        video_subdir: Nome do subdiretório para downloads de vídeo individual.
        playlist_subdir: Nome do subdiretório para downloads de playlist.
        default_video_ext: Extensão padrão para vídeo (mp4).
        default_audio_ext: Extensão padrão para áudio (mp3).
        audio_quality: Taxa de bits para conversão MP3 (padrão: 192).
    """

    base_dir: Path = Path(_DEFAULTS["downloads_dir"])
    video_subdir: str = _DEFAULTS["video_subdir"]
    playlist_subdir: str = _DEFAULTS["playlist_subdir"]
    default_video_ext: str = _DEFAULTS["default_video_format"]
    default_audio_ext: str = _DEFAULTS["default_audio_format"]
    audio_quality: str = _DEFAULTS["audio_quality"]

    @property
    def video_base_path(self) -> Path:
        """Retorna o caminho completo para o diretório de downloads de vídeo."""
        return self.base_dir / self.video_subdir

    @property
    def playlist_base_path(self) -> Path:
        """Retorna o caminho completo para o diretório de downloads de playlist."""
        return self.base_dir / self.playlist_subdir

    def get_video_output_dir(self, title: str, is_audio: bool = False) -> Path:
        """Monta o caminho do diretório de saída para download de um vídeo.

        Args:
            title: Título sanitizado do vídeo usado como nome da pasta.
            is_audio: Se True, coloca arquivos na subpasta 'audio'; senão 'video'.

        Returns:
            Caminho do diretório de saída para este vídeo.
        """
        subdir = "audio" if is_audio else "video"
        return self.video_base_path / title / subdir

    def get_playlist_output_dir(self, title: str, is_audio: bool = False) -> Path:
        """Monta o caminho do diretório de saída para download de uma playlist.

        Args:
            title: Título sanitizado da playlist usado como nome da pasta.
            is_audio: Se True, coloca arquivos na subpasta 'audio'; senão 'video'.

        Returns:
            Caminho do diretório de saída para esta playlist.
        """
        subdir = "audio" if is_audio else "video"
        return self.playlist_base_path / title / subdir

    def ensure_dirs(self) -> None:
        """Cria todos os diretórios de download se não existirem."""
        self.video_base_path.mkdir(parents=True, exist_ok=True)
        self.playlist_base_path.mkdir(parents=True, exist_ok=True)


_raw = _load_config()
config = DownloadConfig(
    base_dir=Path(_raw["downloads_dir"]),
    video_subdir=_raw["video_subdir"],
    playlist_subdir=_raw["playlist_subdir"],
    default_video_ext=_raw["default_video_format"],
    default_audio_ext=_raw["default_audio_format"],
    audio_quality=_raw["audio_quality"],
)
