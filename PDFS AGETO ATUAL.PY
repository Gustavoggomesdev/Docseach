import os
import mysql.connector
from datetime import datetime

# Configuração da conexão com o banco de dados
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789",
    database="pastaDB",
    autocommit=False
)
cursor = conn.cursor()

# Caminho raiz e profundidade máxima
caminho_raiz = r'B:\AGETO\BatchesPro\AGETO INDEX'
profundidade_maxima_desejada = 2

# Carrega todos os caminhos existentes para evitar SELECT por arquivo
cursor.execute("SELECT caminho FROM agetos")
caminhos_existentes = set(c[0] for c in cursor.fetchall())

contador = 0
COMMIT_EVERY = 200  # commit a cada 200 arquivos

def inserir_dados(nome, caminho, data_criacao):
    """Insere se não existir e marca como processado"""
    if caminho not in caminhos_existentes:
        try:
            cursor.execute(
                "INSERT INTO agetos (nome, caminho, data_criacao, processado) VALUES (%s,%s,%s,%s)",
                (nome, caminho, data_criacao, True)
            )
            caminhos_existentes.add(caminho)
            return True
        except mysql.connector.Error as e:
            print(f"Erro ao inserir {nome}: {e}")
    return False

# Função principal para listar PDFs
def listar_pdfs(caminho_raiz, profundidade_maxima):
    global contador
    for root, dirs, files in os.walk(caminho_raiz):
        profundidade_atual = root[len(caminho_raiz):].count(os.sep)
        if profundidade_atual < profundidade_maxima:
            for file_name in files:
                if file_name.lower().endswith('.pdf'):
                    caminho_completo = os.path.join(root, file_name).replace("\\", "/")
                    try:
                        data_criacao = datetime.fromtimestamp(os.path.getctime(caminho_completo))
                    except FileNotFoundError:
                        data_criacao = datetime.now()

                    inserido = inserir_dados(file_name, caminho_completo, data_criacao)
                    contador += 1

                    # Print de progresso a cada 50 arquivos
                    if contador % 50 == 0:
                        status = "inserido" if inserido else "já existente"
                        print(f"{contador} arquivos processados ({status}), último: {file_name}")

                    # Commit a cada COMMIT_EVERY arquivos
                    if contador % COMMIT_EVERY == 0:
                        conn.commit()
        else:
            dirs[:] = []

# Executa a função
listar_pdfs(caminho_raiz, profundidade_maxima_desejada)

# Commit final
conn.commit()
cursor.close()
conn.close()
print(f"Processo concluído! Total de arquivos processados: {contador}")
