# YouTube Playlist Downloader

Este repositório contém um projeto em Python para baixar todos os vídeos de uma playlist
 do YouTube. O projeto agora inclui apenas a Interface de Linha de Comando (CLI) e funciona tanto no windows, quanto no linux.

## Recursos

- **Downloads de Playlist:** Baixa todos os vídeos de uma URL de playlist do YouTube.
- **Downloads de Videos:** Baixa vídeos únicos de uma URL de vídeos do YouTube.
- **Nomeação de Pastas:** Converte o título da playlist em um nome de pasta alfanumérico para armazenar os vídeos e áudios baixados.
- **Alta Resolução:** Baixa cada vídeo/áudio na mais alta resolução disponível.
- **Atualizações em Tempo Real:** A CLI fornece progresso do download e relatórios de erro em tempo real.
- **Escolher Formato:** Escolhe se quer baixar a playlist ou vídeos em arquivos de vídeo (.mp4) ou áudios (.mp3).
- **Organização em Pastas:** Todos os downloads são organizados em pastas específicas `downloads\downloaded_playlists` e `downloads\downloaded_videos_only`.
- **GUI:** [Em desenvolvimento]

## **Instalação**

1. Instale o ffmpeg no seu sistema operacional
   - No Windows:

        ```bash
        scoop install ffmpeg
        ```

   - No Linux (Ubuntu):

        ```bash
        sudo apt install ffmpeg
        ```

    > O script irá verificar se o FFmpeg está instalado, solicitando ao usuário permissão para instalar, quando necessário.

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

6. Executar o Script via terminal:

    ```bash
    python main.py
    ```

## Build

### Para Windows e Linux

> O build pode ser feito via terminal, usando o pyinstaller, presente no `requirements.txt`.

Para usar o script como um executável, basta executar o comando a seguir:

```bash
pyinstaller --onefile --name playlist-downloader playlist_downloader.py
```

No Windows ou no Linux, serão criadas duas pastas, `build` e `dist`, dentro da segunda pasta estará o executável, podendo ser usado em qualquer pasta em que seja mantido. Porém no linux será necessário dar a permissão para execução. Com: `chmod u+x playlist-downloader`.

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

> Projeto baseado no design de [Dhananjay Porwal](https://github.com/DhananjayPorwal/youtube-playlist-downloader).
