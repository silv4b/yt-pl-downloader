# YouTube Playlist Downloader ✨

> Projeto baseado no design de [Dhananjay Porwal](https://github.com/DhananjayPorwal/youtube-playlist-downloader).

Este repositório contém um projeto em Python para baixar todos os vídeos de uma playlist
 do YouTube. O projeto agora inclui apenas a Interface de Linha de Comando (CLI).

## Recursos

- **Downloads de Playlist:** Baixa todos os vídeos de uma URL de playlist do YouTube.
- **Nomeação de Pastas:** Converte o título da playlist em um nome de pasta alfanumérico para armazenar os vídeos baixados.
- **Alta Resolução:** Baixa cada vídeo na mais alta resolução disponível.
- **Atualizações em Tempo Real:** A GUI fornece progresso do download e relatórios de erro em tempo real.

## Instalação

1. Instale o ffmpeg no seu sistema operacional
   - No Windows:

        ```bash
        scoop install ffmpeg
        ```

   - No Linux (Ubuntu):

        ```bash
        sudo apt install ffmpeg
        ```

2. Clone o repositório:

    ```bash
    git clone https://github.com/silv4b/yt-pl-downloader.git
    ```

3. Acesse o diretório do projeto:

    ```bash
    cd yt-pl-downloader
    ```

4. Configure um ambiente **virtual** (recomendado):

    ```bash
    python -m venv venv
    ```

    e ative o ambiente virtual

    - No Windows:

        ```bash
        .\venv\Scripts\Activate.ps1
        ```

    - No Linux:

        ```bash
        source venv/bin/activate
        ```

5. Instale as dependências necessárias:

    ```bash
    pip install -r requirements.txt
    ```

## Uso

### Interface de Linha de Comando (CLI)

1. Execute o script CLI:

    ```bash
    python playlist_downloader.py
    ```

2. Siga as instruções:

   - Insira a URL da playlist do YouTube quando solicitado.
   - O script criará uma pasta (nomeada com o título da playlist sanitizado) dentro de uma outra pasta chamada `downloads` e baixará todos os vídeos nela.
   - Atualizações de progresso e detalhes do tamanho dos vídeos são exibidos no terminal.

## Notas Adicionais

- O projeto agora utiliza `yt_dlp` para melhor compatibilidade e desempenho em comparação com a biblioteca `pytube`.

- Para compilações multiplataforma, lembre-se de que os executáveis são específicos para cada sistema operacional. Atualmente, apenas o executável para Ubuntu é fornecido (compilado com PyInstaller no Ubuntu).

- Para o funcionamento correto, o FFMPEG deve estar instalado.

## Fontes

[Documentação do yt_dlp](https://github.com/yt-dlp/yt-dlp)
