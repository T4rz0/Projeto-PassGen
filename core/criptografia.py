import sys
import os

# Adiciona a raiz do projeto (um nível acima) ao caminho de busca do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from banco import conexao
import bcrypt

#funcao para gerar o salt
def gerar_salt():
    return bcrypt.gensalt()
    

#funcao para criptografar a senha mestre com o salt gerado
def hash_senha(senha, salt):
    # Gera o hash da senha usando bcrypt com o salt fornecido
    hashed = bcrypt.hashpw(senha.encode('utf-8'), salt)
    return hashed



def armazenar_hash_senha(salt,hashed):
    # Armazena o hash da senha no banco de dados
    try:
        sql = conexao.conexao_sql()
        cursor = sql.get_cursor()
        cursor.execute("USE passgen")
        cursor.execute("INSERT INTO configuracao (salt, ver_senham) VALUES (%s, %s)", (salt, hashed))
        sql.conexao.commit()
        sql.close_conexao()
    except Exception as e:
        print(f"Erro ao armazenar hash da senha: {e}")
        
     
        
#Funcão principal
if __name__ == "__main__":
    senha = input("Digite a senha mestre: ")
    comprimento = len(senha)
    salt = gerar_salt()
    senha_hash = None
    
    try:
        senha_hash = hash_senha(senha, salt)
    except Exception as e:
        print(f"Erro ao gerar hash da senha: {e}")
    try:
        armazenar_hash_senha(salt, senha_hash)
        print("Senha mestre criptografada e armazenada com sucesso!")
    except Exception as e:
        print(f"Erro ao armazenar a senha: {e}")
   
        

    
    
     


