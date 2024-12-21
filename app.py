from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789",
    database="pastaDB"
)
cursor = conn.cursor()

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
                like_pattern = f"%{nome_subpasta}%"
                
              
                query = f"""
                SELECT id, nome, caminho, data_criacao 
                FROM {tabela} 
                WHERE nome LIKE %s
                """
                cursor.execute(query, (like_pattern,))
                resultados = cursor.fetchall()

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
