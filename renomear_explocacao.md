# Documentação do Script de Renomeação de Vídeos

Este script em Python renomeia arquivos de vídeo em uma pasta com base nos títulos enumerados em um arquivo `titulos.txt`. Ele foi projetado para funcionar em sistemas Windows e lida com caracteres especiais, acentos e espaços em branco.

---

## Funcionalidades

1. **Leitura do Arquivo `titulos.txt`**:
   - O script lê um arquivo chamado `titulos.txt` que contém os nomes dos vídeos enumerados.
   - Exemplo de formato do arquivo:

     ```bash
     1. Nome do Vídeo 1
     2. Nome do Vídeo 2
     3. Nome do Vídeo 3
     ```

2. **Normalização de Texto**:
   - Remove acentos e caracteres especiais.
   - Converte o texto para minúsculas.
   - Remove espaços extras no início e no fim.
   - Substitui caracteres inválidos para nomes de arquivos no Windows (como `｜`, `/`, `\`, `:`, etc.) por `_`.

3. **Renomeação de Vídeos**:
   - Compara os nomes dos arquivos de vídeo na pasta com os títulos no arquivo `titulos.txt`.
   - Renomeia os arquivos de vídeo para o formato `N. Nome do Vídeo.extensão`, onde `N` é o número do título.

4. **Tratamento de Erros**:
   - Exibe mensagens de erro caso o arquivo `titulos.txt` não seja encontrado ou ocorra algum problema durante a renomeação.

---

## Como Usar

### Pré-requisitos

1. **Python**:
   - Certifique-se de ter o Python instalado. Você pode baixá-lo em [python.org](https://www.python.org/).

2. **Arquivo `titulos.txt`**:
   - Crie um arquivo chamado `titulos.txt` na mesma pasta onde estão os vídeos.
   - O arquivo deve conter os nomes dos vídeos enumerados, um por linha, no formato:

     ```bash
     1. Nome do Vídeo 1
     2. Nome do Vídeo 2
     3. Nome do Vídeo 3
     ```

3. **Vídeos na Pasta**:
   - Coloque os vídeos na mesma pasta onde está o arquivo `titulos.txt`.

---

### Passo a Passo

1. **Salve o Script**:
   - Copie o código do script para um arquivo chamado `renomear_videos.py`.

2. **Execute o Script**:
   - Abra o terminal (Prompt de Comando ou PowerShell) e navegue até a pasta onde o script está salvo.
   - Execute o script com o comando:

     ```bash
     python renomear_videos.py
     ```

3. **Informe o Caminho da Pasta**:
   - Quando solicitado, insira o caminho da pasta onde estão os vídeos e o arquivo `titulos.txt`. Por exemplo:

     ```bash
     Digite o caminho da pasta onde estão os vídeos e o arquivo titulos.txt: C:\Users\bruno\Documentos\Ferramentas\youtube-playlist-downloader\downloads\CursoCompletoPreparatórioparaaCertificaçãoPMPeCAPM
     ```

4. **Acompanhe a Execução**:
   - O script exibirá mensagens no terminal enquanto lê o arquivo `titulos.txt` e renomeia os vídeos.

5. **Resultado**:
   - Após a execução, os vídeos serão renomeados conforme os títulos no arquivo `titulos.txt`.

---

## Exemplo de Funcionamento

### Estrutura da Pasta Antes da Execução

```bash
C:\Users\bruno\Documentos\Ferramentas\youtube-playlist-downloader\downloads\CursoCompletoPreparatórioparaaCertificaçãoPMPeCAPM\
    titulos.txt
    A importância do Contexto dos Projetos ｜ Capítulo 2 - Aula 1.mp4
    video_aula_02.mkv
    video_aula_03.avi
```

### Conteúdo de `titulos.txt`

```bash
11. A importância do Contexto dos Projetos | Capítulo 2 - Aula 1
12. video_aula_02
13. video_aula_03
```

### Saída do Script

```bash
Digite o caminho da pasta onde estão os vídeos e o arquivo titulos.txt: C:\Users\bruno\Documentos\Ferramentas\youtube-playlist-downloader\downloads\CursoCompletoPreparatórioparaaCertificaçãoPMPeCAPM
Lendo o arquivo C:\Users\bruno\Documentos\Ferramentas\youtube-playlist-downloader\downloads\CursoCompletoPreparatórioparaaCertificaçãoPMPeCAPM\titulos.txt...
Total de títulos lidos: 3
Renomeando vídeos na pasta C:\Users\bruno\Documentos\Ferramentas\youtube-playlist-downloader\downloads\CursoCompletoPreparatórioparaaCertificaçãoPMPeCAPM...
Verificando arquivo: A importância do Contexto dos Projetos ｜ Capítulo 2 - Aula 1.mp4 -> Nome normalizado: a_importancia_do_contexto_dos_projetos_|_capitulo_2_-_aula_1
Renomeado: A importância do Contexto dos Projetos ｜ Capítulo 2 - Aula 1.mp4 -> 11. A importância do Contexto dos Projetos | Capítulo 2 - Aula 1.mp4
Verificando arquivo: video_aula_02.mkv -> Nome normalizado: video_aula_02
Renomeado: video_aula_02.mkv -> 12. video_aula_02.mkv
Verificando arquivo: video_aula_03.avi -> Nome normalizado: video_aula_03
Renomeado: video_aula_03.avi -> 13. video_aula_03.avi
```

### Estrutura da Pasta Após Execução

```bash
C:\Users\bruno\Documentos\Ferramentas\youtube-playlist-downloader\downloads\CursoCompletoPreparatórioparaaCertificaçãoPMPeCAPM\
    titulos.txt
    11. A importância do Contexto dos Projetos | Capítulo 2 - Aula 1.mp4
    12. video_aula_02.mkv
    13. video_aula_03.avi
```

---

## Código Completo

```python
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
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    # Converte para minúsculas
    texto = texto.lower()
    # Remove espaços extras no início e no fim
    texto = texto.strip()
    # Substitui caracteres inválidos por '_'
    caracteres_invalidos = ['<', '>', ':', '"', '/', '\\', '|', '?', '*', '｜']
    for char in caracteres_invalidos:
        texto = texto.replace(char, '_')
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
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                linha = linha.strip()  # Remove espaços em branco e quebras de linha
                if linha:
                    # Divide a linha no primeiro ponto e espaço (N. Título do Vídeo)
                    numero, nome = linha.split('. ', 1)
                    # Normaliza o nome do vídeo para facilitar a comparação
                    nome_normalizado = normalizar_texto(nome)
                    titulos[nome_normalizado] = f"{numero}. {nome}"  # Formata o novo nome
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
                # Normaliza o nome do arquivo para facilitar a comparação
                nome_sem_extensao_normalizado = normalizar_texto(nome_sem_extensao)
                print(f"Verificando arquivo: {nome_arquivo} -> Nome normalizado: {nome_sem_extensao_normalizado}")

                # Verifica se o nome do arquivo (sem extensão e normalizado) está no dicionário de títulos
                if nome_sem_extensao_normalizado in titulos:
                    novo_nome = titulos[nome_sem_extensao_normalizado] + extensao  # Mantém a extensão original
                    # Substitui caracteres inválidos no novo nome
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
    # Solicita o caminho da pasta ao usuário
    caminho_pasta = input("Digite o caminho da pasta onde estão os vídeos e o arquivo titulos.txt: ")

    # Verifica se o caminho da pasta existe
    if not os.path.isdir(caminho_pasta):
        print(f"Erro: A pasta '{caminho_pasta}' não existe.")
    else:
        # Lê os títulos do arquivo titulos.txt na pasta especificada
        titulos = ler_titulos(caminho_pasta)

        if titulos:
            # Renomeia os vídeos
            renomear_videos(caminho_pasta, titulos)
        else:
            print("Nenhum título foi lido do arquivo titulos.txt.")
```

---

## Considerações Finais

- O script é compatível com sistemas Windows.
- Certifique-se de que o arquivo `titulos.txt` esteja no formato correto.
- Se houver problemas, verifique as mensagens de erro exibidas no terminal.
