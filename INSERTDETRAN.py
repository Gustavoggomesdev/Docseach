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


def pasta_existe(caminho):
    cursor.execute("SELECT COUNT(*) FROM subpastas WHERE caminho = %s", (caminho,))
    return cursor.fetchone()[0] > 0


def pasta_processada(caminho):
    cursor.execute("SELECT processado FROM subpastas WHERE caminho = %s", (caminho,))
    result = cursor.fetchone()
    if result is not None:
        return result[0] 
    return False


def marcar_como_processada(caminho):
    cursor.execute("UPDATE subpastas SET processado = TRUE WHERE caminho = %s", (caminho,))
    conn.commit()


def inserir_dados(nome, caminho, data_criacao):
    if not pasta_existe(caminho):
        query = "INSERT INTO subpastas (nome, caminho, data_criacao, processado) VALUES (%s, %s, %s, %s)"
        values = (nome, caminho, data_criacao, False)
        cursor.execute(query, values)
        conn.commit()
        print(f"Subpasta {nome} registrada no banco de dados")
    elif not pasta_processada(caminho):
        print(f"Subpasta {nome} em {caminho} já existe no banco de dados, mas ainda não foi processada")
    else:
        print(f"Subpasta {nome} em {caminho} já foi processada anteriormente")


caminho_raiz = r'Z:/DETRAN - TO 03/ScanPro/VEÍCULO'


def listar_subpastas(caminho_raiz, profundidade_maxima):
    for root, dirs, files in os.walk(caminho_raiz):
        profundidade_atual = root[len(caminho_raiz):].count(os.sep)
        if profundidade_atual < profundidade_maxima:
            for dir_name in dirs:
                caminho_completo = os.path.join(root, dir_name).replace("\\", "/")  
                data_criacao = datetime.fromtimestamp(os.path.getctime(caminho_completo))
                if not pasta_processada(caminho_completo):
                    inserir_dados(dir_name, caminho_completo, data_criacao)
                    marcar_como_processada(caminho_completo)
                else:
                    print(f"Subpasta {dir_name} em {caminho_completo} já foi processada")
        else:
            dirs[:] = []


profundidade_maxima_desejada = 2

listar_subpastas(caminho_raiz, profundidade_maxima_desejada)

cursor.close()
conn.close()

print("Processo concluído com sucesso!")
