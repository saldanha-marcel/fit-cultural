from django.test import TestCase

# Create your tests here.
import sqlite3

def test_database_connection():
    try:
        # Tenta conectar ao banco de dados SQLite padrão do Django
        conn = sqlite3.connect('db.sqlite3')
        conn.close()
        print("Conexão com o banco de dados bem-sucedida.")
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()
conn.execute("UPDATE core_testprogress SET behavioral_test_completed = 1, typing_test_completed = 1 WHERE user_id = 1")
conn.commit()
conn.close()
