#Importa comunicação com o sistema operacional
import os
#Importa a biblioteca para carregar variáveis no .env
import dotenv
#Importa a comunicação com SQL
import mysql.connector

class conexao_sql:

    #Contrutor da conexão
    def __init__(self):
        dotenv.load_dotenv()

        DB_HOST = os.getenv("DB_HOST")
        DB_USER = os.getenv("DB_USER")
        DB_PORT = os.getenv("DB_PORT")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        DB_NAME = os.getenv("DB_NAME")

        self.conexao = None
        self.cursor = None
        
        try:
            #Estabelece a conexão com o banco de dados
            self.conexao = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                port=DB_PORT,
                password=DB_PASSWORD,
                database=DB_NAME
            )

            #Cria um cursor para dar comandos no banco de dados
            self.cursor = self.conexao.cursor()

            

        #Se não conectar gera exessão
        except mysql.connector.Error as erro:
            print(f"Erro ao conectar ao banco de dados: {erro}")
    
    
    #Função para gerar cursor/comando
    def get_cursor(self):
         return self.cursor
    
    #Função para fechar a conexão
    def close_conexao(self):
        if self.cursor:
            self.cursor.close()
        if self.conexao:
            self.conexao.close()
    
    #Função para executar comandos SQL
    def comando_sql(self, comando, params=None):
        try:
            if params:
                self.cursor.execute(comando, params)
            else:
                self.cursor.execute(comando)
            self.conexao.commit()
        except mysql.connector.Error as erro:
            print(f"Erro ao executar comando SQL: {erro}")
    
