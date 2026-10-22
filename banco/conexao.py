#Importa comunicação com o sistema operacional
import os
#Importa a biblioteca para carregar variáveis no .env
import dotenv
#Importa a comunicação com SQL
import mysql.connector

dotenv.load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PORT = os.getenv("DB_PORT")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

try:
    #Estabelece a conexão com o banco de dados
    conexao = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        port=DB_PORT,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    #Caso funcione exibe mensagem de sucesso
    print("Conexão com o banco de dados estabelecida com sucesso!")

    #Cria um cursor para dar comandos no banco de dados
    cursor = conexao.cursor()
    cursor.execute("SELECT version()")
    versao = cursor.fetchone()
    print(f"Versão do banco de dados: {versao[0]}")

    #fecha a conexão com o banco de dados
    cursor.close()
    conexao.close()

#Se não conectar gera exessão
except mysql.connector.Error as erro:
    print(f"Erro ao conectar ao banco de dados: {erro}")
