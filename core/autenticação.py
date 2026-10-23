import sys
import os

# Adiciona a raiz do projeto (um nível acima) ao caminho de busca do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from banco import conexao
import bcrypt

def verificar_senha(senha):

    sql = conexao.conexao_sql()
    cursor = sql.get_cursor()
    cursor.execute("USE passgen")
    cursor.execute("SELECT salt FROM configuracao WHERE id = 1")
    stored_salt = cursor.fetchone()
    cursor.execute("SELECT ver_senham FROM configuracao WHERE id = 1")
    stored_hash = cursor.fetchone()
    
    try:
       #Função para verificar a senha mestre usando o salt armazenado no banco de dados
        if stored_salt and stored_hash:
            stored_salt = stored_salt[0]
            stored_hash = stored_hash[0]
            if bcrypt.checkpw(senha.encode('utf-8'), stored_hash):
                print("Senha mestre correta!")
                return True
            else:
                print("Senha mestre incorreta!")
                return False
    except Exception as e:
        print(f"Erro ao verificar a senha: {e}")   
        
#Função principal
if __name__ == "__main__":
    senha = input("Digite sua senha:")
    verificar_senha(senha)
    