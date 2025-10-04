from flask import Flask, render_template, request, send_file, abort
import mysql.connector
import os

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="pastaDB"
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    resultados = []
    mensagem_erro = None
    tabela = 'subpastas' 

    if request.method == 'POST':
        nome_subpasta = request.form.get('nome_subpasta', '').strip()
        tabela = request.form.get('tabela', 'subpastas') 

        if not nome_subpasta:
            mensagem_erro = "Por favor, insira o nome do processo para pesquisar."
        else:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                like_pattern = f"%{nome_subpasta}%"
                query = f"""
                SELECT id, nome, caminho, data_criacao 
                FROM {tabela}
                WHERE nome LIKE %s
                """
                cursor.execute(query, (like_pattern,))
                resultados = cursor.fetchall()
                cursor.close()
                conn.close()
                if not resultados:
                    mensagem_erro = "Nenhum resultado encontrado para a pesquisa."
            except mysql.connector.Error as err:
                mensagem_erro = f"Erro ao acessar o banco de dados: {err}"

    return render_template(
        'index.html',
        resultados=resultados,
        tabela=tabela,
        mensagem_erro=mensagem_erro
    )

@app.route('/abrir_arquivo/<int:resultado_id>')
def abrir_arquivo(resultado_id):
    tabela = request.args.get('tabela', 'arquivos_pdf')
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT caminho FROM {tabela} WHERE id = %s", (resultado_id,))
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        return abort(500, description=f"Erro ao acessar o banco de dados: {err}")

    if resultado:
        caminho_arquivo = resultado[0]
        # Detecta a letra do drive e monta o UNC path corretamente
        if caminho_arquivo[1:3] == ':\\' or caminho_arquivo[1:3] == ':/':
            letra = caminho_arquivo[0].upper()
            resto = caminho_arquivo[3:]  # Remove "X:\" ou "X:/"
            resto = resto.replace('/', '\\')
            if letra == 'Z':
                caminho_arquivo = f"\\\\192.168.52.252\\Detran\\{resto}"
            elif letra == 'X':
                caminho_arquivo = f"\\\\192.168.52.252\\ageto\\{resto}"
            elif letra == 'N':
                caminho_arquivo = f"\\\\192.168.52.253\\detran\\{resto}"
            elif letra == 'B':
                caminho_arquivo = f"\\\\192.168.52.253\\ageto\\{resto}"
        # Tenta servir o arquivo
        if os.path.exists(caminho_arquivo):
            return send_file(caminho_arquivo)
        else:
            return abort(404, description=f"Arquivo não encontrado: {caminho_arquivo}")
    else:
        return abort(404, description="Registro não encontrado.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

    
#python -m pip install --upgrade mysql-connector-python
