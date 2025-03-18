import subprocess

def extrair_titulos_da_playlist(url_playlist):
    try:
        # Comando yt-dlp para obter os títulos da playlist
        comando = [
            'yt-dlp',
            '--get-title',          # Extrai apenas os títulos
            '--flat-playlist',       # Não detalha cada vídeo (mais rápido)
            url_playlist             # URL da playlist
        ]

        # Executa o comando e captura a saída
        resultado = subprocess.run(comando, stdout=subprocess.PIPE, text=True)

        # Verifica se o comando foi executado com sucesso
        if resultado.returncode == 0:
            # Divide a saída em linhas (cada linha é um título)
            titulos = resultado.stdout.strip().split('\n')
            return titulos
        else:
            print("Erro ao executar o yt-dlp.")
            return None

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return None

def salvar_titulos_em_arquivo(titulos, nome_arquivo):
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            for indice, titulo in enumerate(titulos, start=1):
                # Formata o título com o número
                linha = f"{indice}. {titulo}"
                print(linha)  # Exibe o título no console
                arquivo.write(linha + '\n')  # Escreve o título no arquivo
        print(f"\nTítulos salvos em {nome_arquivo}")
    except Exception as e:
        print(f"Erro ao salvar os títulos: {e}")

if __name__ == "__main__":
    # Solicita a URL da playlist ao usuário
    url_playlist = input("Cole a URL da playlist do YouTube: ")

    # Extrai os títulos
    titulos = extrair_titulos_da_playlist(url_playlist)

    if titulos:
        # Salva os títulos em um arquivo
        salvar_titulos_em_arquivo(titulos, "titulos.txt")