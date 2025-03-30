import os
import unicodedata


def normalizar_texto(texto):
    """
    Normaliza o texto para facilitar a comparação:
    - Remove acentos e caracteres especiais.
    - Converte para minúsculas.
    - Remove espaços extras.
    - Substitui caracteres inválidos por '_'.
    """
    # Remove acentos e caracteres especiais
    texto = (
        unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode("ASCII")
    )
    texto = texto.lower()
    # Remove espaços extras no início e no fim
    texto = texto.strip()
    # Substitui caracteres inválidos do windows por '_'
    caracteres_invalidos = ["<", ">", ":", '"', "/", "\\", "|", "?", "*", "｜"]
    for char in caracteres_invalidos:
        texto = texto.replace(char, "_")
    return texto


def ler_titulos(caminho_pasta):
    """
    Lê o arquivo titulos.txt na pasta especificada e retorna um dicionário onde a chave é o nome do vídeo
    e o valor é o nome formatado (com o número).
    """
    caminho_arquivo = os.path.join(caminho_pasta, "titulos.txt")
    titulos = {}
    try:
        print(f"Lendo o arquivo {caminho_arquivo}...")
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()  # Remove espaços em branco e quebras de linha
                if linha:
                    # Divide a linha no primeiro ponto e espaço (N. Título do Vídeo)
                    numero, nome = linha.split(". ", 1)
                    nome_normalizado = normalizar_texto(nome)
                    titulos[nome_normalizado] = (
                        f"{numero}. {nome}"  # Formata o novo nome
                    )
        print(f"Total de títulos lidos: {len(titulos)}")
        return titulos
    except Exception as e:
        print(f"Erro ao ler o arquivo {caminho_arquivo}: {e}")
        return None


def renomear_videos(caminho_pasta, titulos):
    """
    Renomeia os vídeos na pasta com base nos títulos do arquivo.
    """
    try:
        print(f"Renomeando vídeos na pasta {caminho_pasta}...")
        # Lista todos os arquivos na pasta
        for nome_arquivo in os.listdir(caminho_pasta):
            caminho_completo = os.path.join(caminho_pasta, nome_arquivo)

            # Verifica se é um arquivo (ignora pastas)
            if os.path.isfile(caminho_completo) and nome_arquivo != "titulos.txt":
                # Remove a extensão do arquivo para comparar com os títulos
                nome_sem_extensao, extensao = os.path.splitext(nome_arquivo)
                nome_sem_extensao_normalizado = normalizar_texto(nome_sem_extensao)
                print(
                    f"Verificando arquivo: {nome_arquivo} -> Nome normalizado: {nome_sem_extensao_normalizado}"
                )

                # Verifica se o nome do arquivo (sem extensão e normalizado) está no dicionário de títulos
                if nome_sem_extensao_normalizado in titulos:
                    novo_nome = titulos[nome_sem_extensao_normalizado] + extensao
                    novo_nome = normalizar_texto(novo_nome)
                    novo_caminho = os.path.join(caminho_pasta, novo_nome)

                    # Renomeia o arquivo
                    os.rename(caminho_completo, novo_caminho)
                    print(f"Renomeado: {nome_arquivo} -> {novo_nome}")
                else:
                    print(f"Arquivo '{nome_arquivo}' não encontrado em titulos.txt.")
    except Exception as e:
        print(f"Erro ao renomear os vídeos: {e}")


if __name__ == "__main__":
    caminho_pasta = input(
        "Digite o caminho da pasta onde estão os vídeos e o arquivo titulos.txt: "
    )

    if not os.path.isdir(caminho_pasta):
        print(f"Erro: A pasta '{caminho_pasta}' não existe.")
    else:
        titulos = ler_titulos(caminho_pasta)
        if titulos:
            renomear_videos(caminho_pasta, titulos)
        else:
            print("Nenhum título foi lido do arquivo titulos.txt.")
