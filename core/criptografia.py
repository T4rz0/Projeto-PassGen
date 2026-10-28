import os
from cryptography.fernet import Fernet

from banco import conexao
import bcrypt

#funcao para gerar o salt
def gerar_salt():
    return bcrypt.gensalt()
    

#funcao para criptografar a senha mestre com o salt gerado
def hash_senha_mestre(senha, salt):
    # Gera o hash da senha usando bcrypt com o salt fornecido
    hashed = bcrypt.hashpw(senha.encode('utf-8'), salt)
    return hashed


#Função para armazenar o código de criptografia da senha mestre
def armazenar_hash_senha(salt,hashed):
    # Armazena o hash da senha no banco de dados
    try:
        sql = conexao.conexao_sql()
        cursor = sql.get_cursor()
        cursor.execute("USE passgen")
        
        cursor.execute("SELECT ver_senham FROM configuracao LIMIT 1")
        resul = cursor.fetchone()
        if resul is not None and resul[0] is not None:
            sql.close_conexao()
            raise Exception ("Já existe uma Senha Mestre cadastrada!")
        cursor.execute("INSERT INTO configuracao (salt, ver_senham) VALUES (%s, %s)", (salt, hashed))
        sql.conexao.commit()
        sql.close_conexao()
    except Exception as e:
        print(f"Erro ao armazenar hash da senha: {e}")
        
#Cria a chave para criptografar a senha com base no código FERNET no .env
def obter_chave():
    try:
        chave = os.getenv("CHAVE_FERNET") 
        return chave.encode()
    except Exception as e:
        print(f"Não foi possivel obter a chave {e}")

#Criptografia para senha do usuário
def criptografar_senha(senha_limpa):
    f = Fernet(obter_chave())
    token = f.encrypt(senha_limpa.encode('utf-8'))
    return token.decode('utf-8')       

#Verificação da senha do usuário
def descriptografar_senha(senha_cripto):
    f = Fernet(obter_chave())
    senha_descripto = f.decrypt(senha_cripto.encode('utf-8'))
    return senha_descripto.decode('utf-8')

#Funcão principal para teste da senha mestre
if __name__ == "__main__":
    senha = input("Digite a senha mestre: ")
    comprimento = len(senha)
    salt = gerar_salt()
    senha_hash = None
    
    try:
        senha_hash = hash_senha_mestre(senha, salt)
    except Exception as e:
        print(f"Erro ao gerar hash da senha: {e}")
    try:
        armazenar_hash_senha(salt, senha_hash)
        print("Senha mestre criptografada e armazenada com sucesso!")
    except Exception as e:
        print(f"Erro ao armazenar a senha: {e}")
   
        

    
    
     


