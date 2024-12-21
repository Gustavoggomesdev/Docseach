import os
import mysql.connector
from datetime import datetime


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789",
    database="pastaDB"
)
cursor = conn.cursor()


def arquivo_existe(caminho):
    cursor.execute("SELECT COUNT(*) FROM arquivos_pdf WHERE caminho = %s", (caminho,))
    return cursor.fetchone()[0] > 0

def arquivo_processado(caminho):
    cursor.execute("SELECT processado FROM arquivos_pdf WHERE caminho = %s", (caminho,))
    result = cursor.fetchone()
    if result is not None:
        return result[0]
    return False

def marcar_como_processado(caminho):
    cursor.execute("UPDATE arquivos_pdf SET processado = TRUE WHERE caminho = %s", (caminho,))
    conn.commit()


def inserir_dados(nome, caminho, data_criacao):
    if not arquivo_existe(caminho):
        query = "INSERT INTO arquivos_pdf (nome, caminho, data_criacao, processado) VALUES (%s, %s, %s, %s)"
        values = (nome, caminho, data_criacao, False)
        cursor.execute(query, values)
        conn.commit()
        print(f"Arquivo PDF {nome} registrado no banco de dados")
    elif not arquivo_processado(caminho):
        print(f"Arquivo PDF {nome} em {caminho} já existe no banco de dados, mas ainda não foi processado")
    else:
        print(f"Arquivo PDF {nome} em {caminho} já foi processado anteriormente")


caminho_raiz = r'X:/AGETO/BatchesPro/AGETO PASSIVO'


def listar_pdfs(caminho_raiz, profundidade_maxima):
    for root, dirs, files in os.walk(caminho_raiz):
        profundidade_atual = root[len(caminho_raiz):].count(os.sep)
        if profundidade_atual < profundidade_maxima:
            for file_name in files:
                if file_name.lower().endswith('.pdf'):
                    caminho_completo = os.path.join(root, file_name).replace("\\", "/")
                    data_criacao = datetime.fromtimestamp(os.path.getctime(caminho_completo))
                    if not arquivo_processado(caminho_completo):
                        inserir_dados(file_name, caminho_completo, data_criacao)
                        marcar_como_processado(caminho_completo)
                    else:
                        print(f"Arquivo PDF {file_name} em {caminho_completo} já foi processado")
        else:
            dirs[:] = []  


profundidade_maxima_desejada = 2


listar_pdfs(caminho_raiz, profundidade_maxima_desejada)


cursor.close()
conn.close()

print("Processo concluído com sucesso!")
