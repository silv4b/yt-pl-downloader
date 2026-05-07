<!-- markdownlint-disable MD060 MD040-->
# AGENTS.md — Guia para Agentes de Código

Este documento define as convenções, arquitetura e práticas de desenvolvimento do projeto **yt-pl-downloader**.

## Stack

| Categoria | Tecnologia |
|---|---|
| **Python** | 3.12+ |
| **Gerenciador de pacotes** | [uv](https://github.com/astral-sh/uv) |
| **Linter/Formatter** | [Ruff](https://github.com/astral-sh/ruff) |
| **TUI** | [Rich](https://github.com/Textualize/rich) + [inquirer](https://github.com/magmax/python-inquirer) |
| **Download** | [yt-dlp](https://github.com/yt-dlp/yt-dlp) |
| **Configuração** | `config.yaml` + `pyyaml` |
| **Testes** | pytest |
| **Build** | PyInstaller via `build.py` |

## Arquitetura

```
yt-pl-downloader/
├── main.py                        # Entry point (CLI loop)
├── build.py                       # Script de build com PyInstaller
├── config.yaml                    # Configurações de paths e defaults
│
├── app/
│   ├── cli/                       # Interface de usuário
│   │   ├── __init__.py            # Reexporta funções públicas
│   │   ├── menu.py                # Prompts, output visual, barras de progresso
│   │   └── quality.py             # Detecção e seleção de qualidade de vídeo
│   │
│   ├── core/                      # Infraestrutura
│   │   ├── __init__.py            # Reexporta funções públicas
│   │   ├── config.py              # DownloadConfig — carrega config.yaml
│   │   ├── ffmpeg_utils.py        # Detecção e instalação do FFmpeg
│   │   ├── deno_utils.py          # Detecção e instalação do Deno
│   │   ├── logger.py              # Logger estruturado
│   │   └── utils.py               # Utilitários puros (sanitize_filename, clear_terminal)
│   │
│   ├── models/                    # Modelos de dados (dataclasses)
│   │   ├── __init__.py
│   │   ├── video.py               # VideoInfo
│   │   └── playlist.py            # PlaylistInfo
│   │
│   ├── services/                  # Lógica de download (sem UI)
│   │   ├── __init__.py
│   │   ├── downloader.py          # BaseDownloader — classe abstrata
│   │   ├── video_downloader.py    # VideoDownloader
│   │   └── playlist_downloader.py # PlaylistDownloader
│   │
│   └── exceptions.py              # Exceções customizadas
│
└── tests/                         # Testes com pytest
    ├── test_core/                 # Testes unitários do core
    ├── test_models/               # Testes unitários dos modelos
    └── test_integration/          # Testes de integração (downloads reais)
```

## Princípios de Design

### 1. Separação UI / Lógica de Negócio

- **`app/cli/`** — Tudo que interage com o usuário (prompts, output, cores)
- **`app/services/`** — Lógica pura, sem `input()`, `print()` ou `exit()`
- Services retornam objetos (`VideoInfo`, `PlaylistInfo`) ou levantam exceções
- `main.py` orquestra: CLI → Service → CLI

### 2. Sem `exit()` nos Services

- Nunca use `exit()`, `sys.exit()` ou `quit()` em services
- Use exceções customizadas (`DownloadError`, `InvalidURLError`, etc.)
- O `main.py` captura as exceções e exibe mensagens apropriadas

### 3. Sem Caminhos Hardcoded

- Todos os paths vêm de `DownloadConfig` em `app/core/config.py`
- O `config.yaml` é a fonte de verdade para valores padrão
- Use `config.get_video_output_dir()` e `config.get_playlist_output_dir()`

### 4. yt-dlp Silencioso + Rich Progress

- Sempre use `quiet: True`, `no_warnings: True`, `logger: SilentLogger()`
- Nunca use `quiet: False` — polui o terminal com logs do yt-dlp
- Use hooks de progresso para alimentar as barras do Rich
- Use `total_bytes` e `total_bytes_estimate` (não `total`) nos hooks
- O contexto do `Progress()` deve envolver todo o download (tempo calculado corretamente)

### 5. Codec de Vídeo: H.264 (AVC)

- Sempre force `[vcodec^=avc1]` nos filtros de formato
- AV1 causa problemas de compatibilidade com MPC-HC e players antigos
- Fallback para `best` se H.264 não estiver disponível

### 6. Cancelamento Seguro com inquirer

- `inquirer.prompt()` pode retornar `None` se o usuário pressionar `Ctrl+C`
- Use `_prompt()` (wrapper em `app/cli/menu.py`) que levanta `KeyboardInterrupt`
- Nunca acesse diretamente `inquirer.prompt(questions)["key"]`

## Convenções de Código

### Imports

- Sempre use `from __future__ import annotations` no topo
- Ordene imports: stdlib → third-party → local
- Use `ruff` para formatar: `uv run ruff check . --fix`

### Docstrings

- **Todas** as funções, classes e métodos devem ter docstring em **português**
- Siga o formato Google: descrição, Args, Returns, Raises
- Módulos também devem ter docstring

### Type Hints

- Use type hints em todas as assinaturas de função
- Use `|` para união de tipos (Python 3.10+)
- Use `Protocol` para callbacks (ex: `ProgressHook`)

### Testes para Novas Funcionalidades

- **Toda nova funcionalidade deve ter testes unitários correspondentes**
- Testes devem cobrir o caso principal e pelo menos um caso de erro
- Funções de UI (que usam `inquirer` ou `Console`) devem usar mocks para não depender de input do usuário
- Funções que fazem chamadas de rede (yt-dlp) devem mockar `yt_dlp.YoutubeDL`
- Organize os testes em `tests/test_<modulo>/` seguindo a mesma estrutura do `app/`

### Linha Máxima

- 120 caracteres (configurado no `pyproject.toml`)

## Exceções Customizadas

Todas em `app/exceptions.py`:

| Exceção | Quando usar |
|---|---|
| `DownloadError` | Base para todos os erros de download |
| `FFmpegNotFoundError` | FFmpeg não encontrado no PATH |
| `FFmpegInstallError` | Falha na instalação automática do FFmpeg/Deno |
| `InvalidURLError` | URL inválida ou inacessível |
| `PlaylistExtractionError` | Playlist sem vídeos |

## Testes

### Executar

```bash
# Apenas testes unitários
uv run pytest -m "not integration"

# Todos os testes
uv run pytest tests/ -v

# Apenas integração
uv run pytest -m integration

# Pular integração (CI rápido)
SKIP_INTEGRATION=1 uv run pytest tests/ -v
```

### Convenções

- Testes unitários **não** fazem downloads reais
- Testes de integração usam `tempfile.mkdtemp()` e limpam após execução
- Use fixtures para configuração isolada
- Docstrings em português descrevendo o que o teste valida
- Marque testes de integração com `@pytest.mark.integration`

## Build

Use sempre `build.py` — nunca rode PyInstaller manualmente:

```bash
uv run python build.py
```

O script automaticamente:

- Limpa builds anteriores
- Detecta a plataforma (`-win` / `-linux`)
- Inclui `--collect-all yt_dlp`, `--collect-all rich`
- Inclui `--copy-metadata readchar`, `--copy-metadata inquirer`
- O executável vai para `dist/`

## GitHub Actions

Workflows em `.github/workflows/`:

- Disparados por tags no formato `v*`
- Mesmo comando do `build.py` (com as flags de metadata)
- Upload para GitHub Releases

## Dependências

### Produção (`pyproject.toml > dependencies`)

- `yt-dlp` — Download de vídeos
- `rich` — Output visual e barras de progresso
- `inquirer` — Prompts interativos com setas
- `pyyaml` — Carregamento de config.yaml

### Desenvolvimento (`dependency-groups > dev`)

- `ruff` — Linter/formatter
- `pytest` — Testes
- `pyinstaller` — Build de executável
- `coverage` — Cobertura de testes

## Comandos Úteis

```bash
uv sync                    # Instalar dependências
uv run python main.py      # Executar o app
uv run python build.py     # Gerar executável
uv run ruff check .        # Verificar linting
uv run ruff check . --fix  # Corrigir linting
uv run ruff format .       # Formatar código
uv run pytest              # Rodar todos os testes
uv add <pacote>            # Adicionar dependência
uv add --dev <pacote>      # Adicionar dev dependency
```
