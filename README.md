# YouTube Downloader

CLI para baixar vídeos individuais e playlists do YouTube em formato de vídeo (MP4) ou áudio (MP3).

## Recursos

- **Download de vídeos individuais** — Baixa qualquer vídeo do YouTube
- **Download de playlists completas** — Baixa todos os vídeos de uma playlist
- **Escolha de formato** — Vídeo (MP4) ou áudio (MP3)
- **Organização automática** — Downloads organizados em pastas por título
- **Deno integrado** — Verificação e instalação automática para melhorar extração do YouTube
- **FFmpeg integrado** — Verificação e instalação automática do FFmpeg
- **Interface interativa (TUI)** — Navegue com setas ↑↓ e Enter (`inquirer`), com output visual colorido (`Rich`)
- **Barras de progresso duplas** — Progresso da playlist + progresso individual do vídeo com %, velocidade, tamanho e tempo restante
- **Testes de integração** — Testes reais de download (MP4 e MP3) com isolamento em diretório temporário
- **Docstrings completas** — Todo o código documentado em português

## Requisitos

- **Python 3.12+**
- **uv** — Gerenciador de pacotes moderno
- **FFmpeg** — Instalado automaticamente pelo script se necessário
- **Deno** (opcional) — Instalado automaticamente; melhora extração de formatos do YouTube

### Instalando o uv

```bash
# Windows (via winget)
winget install --id=astral-sh.uv

# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Instalação

1. Clone o repositório:

    ```bash
    git clone https://github.com/silv4b/yt-pl-downloader.git
    cd yt-pl-downloader
    ```

2. Instale as dependências:

    ```bash
    uv sync
    ```

## Uso

### Executando o projeto

```bash
uv run python main.py
```

### Interface interativa (TUI)

O projeto combina **inquirer** para navegação com setas e **Rich** para output visual.

```text
╭──────────────────────────────────────╮
│          YouTube Downloader          │
╰──────────────────────────────────────╯

? O que deseja fazer?: (Use ↑↓ e Enter)
    Baixar vídeo individual
  > Baixar playlist completa
    Sair
```

Durante o download, uma barra de progresso é exibida:

```text
⠋ vídeo: Meu Vídeo Legal  ████████░░░░░░░░░░░░░  35%  15.2/43.7MB  5.3MB/s  0:00:05
```

### Baixando um vídeo individual

1. Selecione **"Baixar vídeo individual"** com ↑↓ e `Enter`
2. Cole a URL do vídeo e `Enter`
3. Selecione **Vídeo (MP4)** ou **Áudio (MP3)** com ↑↓ e `Enter`
4. Barra de progresso aparece durante o download
5. Salvo em `downloads/downloaded_videos/<titulo>/<video|audio>/`

### Baixando uma playlist

1. Selecione **"Baixar playlist completa"** com ↑↓ e `Enter`
2. Cole a URL da playlist e `Enter`
3. Selecione **Vídeo (MP4)** ou **Áudio (MP3)** com ↑↓ e `Enter`
4. Barra de progresso mostra avanço vídeo a vídeo
5. Salvo em `downloads/downloaded_playlists/<titulo>/<video|audio>/`

## Estrutura do Projeto

```text
yt-pl-downloader/
├── main.py                        # Entry point (CLI)
├── pyproject.toml                 # Configuração do projeto
├── config.yaml                    # Configurações de paths e defaults
│
├── app/
│   ├── cli/                       # Interface de linha de comando
│   │   └── menu.py                # Prompts interativos e output visual
│   │
│   ├── core/                      # Infraestrutura
│   │   ├── config.py              # DownloadConfig centralizado (YAML)
│   │   ├── ffmpeg_utils.py        # Verificação e instalação do FFmpeg
│   │   ├── deno_utils.py          # Verificação e instalação do Deno
│   │   ├── logger.py              # Logging estruturado
│   │   └── utils.py               # Utilitários (sanitize, etc)
│   │
│   ├── models/                    # Modelos de dados
│   │   ├── video.py               # VideoInfo
│   │   └── playlist.py            # PlaylistInfo
│   │
│   ├── services/                  # Lógica de download
│   │   ├── downloader.py          # Classe base abstrata + hooks
│   │   ├── video_downloader.py    # Download de vídeo único
│   │   └── playlist_downloader.py # Download de playlist
│   │
│   └── exceptions.py              # Exceções customizadas
│
└── tests/                         # Testes com pytest
    ├── test_core/
    │   ├── test_config.py         # Config e carregamento YAML
    │   └── test_utils.py          # Sanitização de nomes
    ├── test_models/
    │   └── test_models.py         # VideoInfo e PlaylistInfo
    └── test_integration/
        └── test_downloads.py      # Downloads reais (MP4/MP3)
```

## Comandos úteis

```bash
# Instalar dependências
uv sync

# Executar o projeto
uv run python main.py

# Rodar testes unitários
uv run pytest -m "not integration"

# Rodar todos os testes (inclui integração com downloads reais)
uv run pytest tests/ -v

# Rodar apenas testes de integração
uv run pytest -m integration

# Pular testes de integração (útil para CI rápido)
SKIP_INTEGRATION=1 uv run pytest tests/ -v

# Executar linter
uv run ruff check .

# Formatar código
uv run ruff format .

# Adicionar nova dependência
uv add <pacote>

# Adicionar dependência de desenvolvimento
uv add --dev <pacote>
```

## Build (Executável)

### Usando PyInstaller

```bash
# Instalar PyInstaller (já incluído nas dev dependencies)
uv sync

# Build
uv run pyinstaller --onefile --name yt-pl-downloader main.py
```

O executável será criado na pasta `dist/`.

### No Linux

```bash
# Dar permissão de execução
chmod +x dist/yt-pl-downloader
```

## CI/CD

O projeto possui GitHub Actions para build automático em Windows e Linux. Ao criar uma tag com o formato `v*`, o build é disparado automaticamente:

```bash
git tag v0.2.0
git push origin v0.2.0
```

## Notas

- O FFmpeg é necessário para conversão de formatos. O projeto verifica e oferece instalação automática
- O Deno é opcional mas recomendado: melhora a extração de formatos do YouTube, permitindo acesso a mais resoluções
- Sem o Deno, alguns vídeos podem não estar disponíveis na melhor qualidade; a opção de instalar aparece no menu
- Os downloads são organizados automaticamente em `downloads/`
- Títulos de vídeos e playlists são sanitizados para nomes de pasta válidos
- Em playlists, vídeos falhos são pulados e o download continua
- Os testes de integração realizam downloads reais; use `SKIP_INTEGRATION=1` para ignorá-los

## Licença

MIT

## Créditos

- Baseado em [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- Design inspirado em [Dhananjay Porwal](https://github.com/DhananjayPorwal/youtube-playlist-downloader)
