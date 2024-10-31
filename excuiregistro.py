import mysql.connector


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789",
    database="pastaDB"
)
cursor = conn.cursor()


cursor.execute("DELETE FROM subpastas")
conn.commit()

print("Todos os registros foram deletados com sucesso!")


cursor.close()
conn.close()
