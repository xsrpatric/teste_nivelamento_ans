import pdfplumber
import pandas as pd
import zipfile
import os

# Nome do PDF e do CSV
pdf_path = "anexo1.pdf"  # Substitua pelo caminho do seu arquivo PDF
csv_path = "dados_extraidos.csv"
zip_path = "Teste_seu_nome.zip"

# Lista para armazenar as tabelas extraídas
dataframes = []

# Abrindo o PDF e extraindo tabela
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        tables = page.extract_table()
        if tables:
            df = pd.DataFrame(tables[1:], columns=tables[0])  # Ajusta cabeçalho
            dataframes.append(df)

# Concatenando todas as tabelas extraídas
df_final = pd.concat(dataframes, ignore_index=True)

# Substituindo abreviações das colunas OD e AMB
substituicoes = {
    "OD": "Odontologia",
    "AMB": "Ambulatorial"
}
df_final.replace(substituicoes, inplace=True)

# Salvando os dados em um CSV
df_final.to_csv(csv_path, index=False, encoding="utf-8")

# Compactando o CSV em um arquivo ZIP
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(csv_path)

# Removendo o CSV após compactação
os.remove(csv_path)

print(f"[+] Processo concluído! Arquivo ZIP salvo como: {zip_path}")
