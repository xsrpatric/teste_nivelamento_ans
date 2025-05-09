import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# URL da página onde estão os PDFs
URL = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
pasta_downloads = "web_scraping/pdfs"
nome_zip = "web_scraping/anexos.zip"

# Criar a pasta de downloads se não existir
os.makedirs(pasta_downloads, exist_ok=True)

#Baixa um arquivo da URL e salva localmente.
def baixar_arquivo(url, nome_arquivo):

# Verifica se a resposta foi bem-sucedida 
    resposta = requests.get(url, stream=True)
    tamanho_total = int(resposta.headers.get('content-length', 0))

        with open(nome_arquivo, "wb") as arquivo, tqdm(
           total=tamanho_total, unit="B", unit_scale=True, desc=nome_arquivo
            ) as barra:
                 for chunk in resposta.iter_content(chunk_size=1024):
                 if chunk:
                    arquivo.write(chunk)
                    barra.update(len(chunk))

        print(f"[+] Download concluído: {nome_arquivo}")
    else:
        print(f"[-] Erro ao baixar {url} (Status {resposta.status_code})")

# Exemplo de chamada
baixar_arquivo(URL, nome_zip)
