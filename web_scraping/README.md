# Web Scraping

~~~python
import os
import requests
import zipfile
from bs4 import BeautifulSoup
from tqdm import tqdm

# URL da página onde estão os PDFs
URL = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
pasta_download = "web_scraping/pdfs"
nomes_ZIP = "web_scraping/anexos.zip"

# Criar a pasta de downloads se não existir
os.makedirs(PASTA_DOWNLOADS, exist_ok=True)

def baixar_arquivo(url, nome_arquivo):
    """Baixa um arquivo da URL e salva localmente."""
    resposta = requests.get(url, stream=True)
    tamanho_total = int(resposta.headers.get('content-length', 0))
    
    with open(nome_arquivo, 'wb') as arquivo, tqdm(
        desc=nome_arquivo,
        total=tamanho_total,
        unit='B',
        unit_scale=True,
        unit_divisor=1024
    ) as barra:
        for chunk in resposta.iter_content(chunk_size=1024):
            arquivo.write(chunk)
            barra.update(len(chunk))

def encontrar_pdfs():
    """Encontra os links dos PDFs na página da ANS."""
    resposta = requests.get(URL)
    soup = BeautifulSoup(resposta.text, 'html.parser')
    
    # Filtra os links para encontrar PDFs
    links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]
    
    # Filtra os Anexos I e II
    anexos = [link for link in links if "anexo-i" in link.lower() or "anexo-ii" in link.lower()]
    return anexos

def compactar_pdfs():
    """Compacta todos os PDFs baixados em um arquivo ZIP."""
    with zipfile.ZipFile(NOME_ZIP, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for arquivo in os.listdir(PASTA_DOWNLOADS):
            caminho_completo = os.path.join(PASTA_DOWNLOADS, arquivo)
            zipf.write(caminho_completo, os.path.basename(caminho_completo))

def main():
    print("[+] Buscando links dos PDFs...")
    links_pdfs = encontrar_pdfs()
    
    if not links_pdfs:
        print("[-] Nenhum PDF encontrado.")
        return
    
    print(f"[+] Encontrados {len(links_pdfs)} PDFs. Iniciando download...")
    
    for link in links_pdfs:
        nome_arquivo = os.path.join(PASTA_DOWNLOADS, link.split("/")[-1])
        baixar_arquivo(link, nome_arquivo)
    
    print("[+] Compactando arquivos...")
    compactar_pdfs()
    
    print(f"[✅] Processo concluído! Arquivos salvos em {NOME_ZIP}")

if __name__ == "__main__":
    main()
