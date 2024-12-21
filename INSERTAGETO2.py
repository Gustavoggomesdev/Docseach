import os
import mysql.connector
from datetime import datetime

# Configuração da conexão com o MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789",
    database="pastaDB"
)
cursor = conn.cursor()

# Função para verificar se o diretório já existe na tabela
def pasta_existe(caminho):
    cursor.execute("SELECT COUNT(*) FROM agetos WHERE caminho = %s", (caminho,))
    return cursor.fetchone()[0] > 0

# Função para verificar se a subpasta já foi processada
def pasta_processada(caminho):
    cursor.execute("SELECT processado FROM agetos WHERE caminho = %s", (caminho,))
    result = cursor.fetchone()
    if result is not None:
        return result[0]  # Retorna True se processado, False se não processado
    return False

# Função para marcar uma subpasta como processada
def marcar_como_processada(caminho):
    cursor.execute("UPDATE agetos SET processado = TRUE WHERE caminho = %s", (caminho,))
    conn.commit()

# Função para inserir dados na tabela agetos
def inserir_dados(nome, caminho, data_criacao):
    if not pasta_existe(caminho):
        query = "INSERT INTO agetos (nome, caminho, data_criacao, processado) VALUES (%s, %s, %s, %s)"
        values = (nome, caminho, data_criacao, False)
        cursor.execute(query, values)
        conn.commit()
        print(f"Subpasta {nome} registrada no banco de dados")
    elif not pasta_processada(caminho):
        print(f"Subpasta {nome} em {caminho} já existe no banco de dados, mas ainda não foi processada")
    else:
        print(f"Subpasta {nome} em {caminho} já foi processada anteriormente")

# Caminho da pasta raiz para a tabela agetos
caminho_raiz = r'X:/AGETO/ScanPro/ADMINISTRATIVO'

# Função para listar e adicionar subpastas
def listar_subpastas(caminho_raiz, profundidade_maxima):
    for root, dirs, files in os.walk(caminho_raiz):
        profundidade_atual = root[len(caminho_raiz):].count(os.sep)
        if profundidade_atual < profundidade_maxima:
            for dir_name in dirs:
                caminho_completo = os.path.join(root, dir_name).replace("\\", "/")  # Corrige as barras invertidas
                data_criacao = datetime.fromtimestamp(os.path.getctime(caminho_completo))
                if not pasta_processada(caminho_completo):
                    inserir_dados(dir_name, caminho_completo, data_criacao)
                    marcar_como_processada(caminho_completo)
                else:
                    print(f"Subpasta {dir_name} em {caminho_completo} já foi processada")
        else:
            dirs[:] = []

# Definir profundidade máxima
profundidade_maxima_desejada = 2

# Listar subpastas e adicionar ao banco de dados
listar_subpastas(caminho_raiz, profundidade_maxima_desejada)

# Fechar a conexão
cursor.close()
conn.close()

print("Processo concluído com sucesso!")