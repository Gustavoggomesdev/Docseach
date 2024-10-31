import mysql.connector


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789",
    database="pastaDB"
)
cursor = conn.cursor()


query = """
    SELECT caminho, GROUP_CONCAT(id ORDER BY id) AS ids
    FROM subpastas
    GROUP BY caminho
    HAVING COUNT(*) > 1;
"""
cursor.execute(query)
duplicados = cursor.fetchall()


for caminho, ids in duplicados:
    ids_list = ids.split(',')
    id_to_keep = ids_list[0]  
    ids_to_delete = ids_list[1:]
    

    print(f"\nCaminho: {caminho}")
    print(f"IDs a serem excluídos: {', '.join(ids_to_delete)}")

    for id_to_delete in ids_to_delete:
        cursor.execute("DELETE FROM subpastas WHERE id = %s", (id_to_delete,))
    conn.commit()


cursor.close()
conn.close()

print("Duplicados removidos com sucesso!")
