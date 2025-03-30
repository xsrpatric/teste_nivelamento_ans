import pdfplumber
import pandas as pd
import zipfile
import os

# Configurações iniciais
pdf_path = "anexo1.pdf"  
csv_path = "dados_extraidos.csv"
zip_path = "Teste_seu_nome.zip"  
# Verifica se o arquivo PDF existe
if not os.path.exists(pdf_path):
    print(f"[ERRO] O arquivo {pdf_path} não foi encontrado.")
    exit(1)

# Lista para armazenar as tabelas extraídas
dataframes = []

try:
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                df = pd.DataFrame(table[1:], columns=table[0])  # Define cabeçalho corretamente
                dataframes.append(df)
except Exception as e:
    print(f"[ERRO] Falha ao processar o PDF: {e}")
    exit(1)

# Verifica se alguma tabela foi extraída
if not dataframes:
    print("[ERRO] Nenhuma tabela foi encontrada no PDF.")
    exit(1)

# Concatenando todas as tabelas extraídas
df_final = pd.concat(dataframes, ignore_index=True)

# Substituição das abreviações (somente se as colunas existirem)
if "OD" in df_final.columns:
    df_final["OD"] = df_final["OD"].replace({"OD": "Odontologia"})
if "AMB" in df_final.columns:
    df_final["AMB"] = df_final["AMB"].replace({"AMB": "Ambulatorial"})

# Salvando os dados em CSV
df_final.to_csv(csv_path, index=False, encoding="utf-8")

# Compactando o CSV em um arquivo ZIP
try:
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(csv_path)
    os.remove(csv_path)  # Remove o CSV após compactação
    print(f"[+] Processo concluído! Arquivo ZIP salvo como: {zip_path}")
except Exception as e:
    print(f"[ERRO] Falha ao criar o ZIP: {e}")
