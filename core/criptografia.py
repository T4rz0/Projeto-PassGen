from banco import conexao

#funcao para gerar o salt
def gerar_salt():
    import secrets
    salt = secrets.token_bytes(16)
    armazenar_salt(salt)
    return salt
    

#funcao para criptografar a senha mestre com o salt gerado
def hash_senha(senha, salt):
    import bcrypt
    # Gera o hash da senha usando bcrypt com o salt fornecido
    hashed = bcrypt.hashpw(senha.encode('utf-8'), salt)
    return hashed

def armazenar_salt(salt):
    # Armazena o salt no banco de dados
    try:
        sql = conexao.conexao_sql()
        cursor = sql.get_cursor()
        comando = "INSERT INTO salt (salt) VALUES (%s)"+salt
        cursor.execute(comando)
        sql.comando_sql("COMMIT")
    except Exception as e:
        print(f"Erro ao armazenar salt: {e}")


def armazenar_hash_senha(hashed):
    # Armazena o hash da senha no banco de dados
    try:
        sql = conexao.conexao_sql()
        cursor = sql.get_cursor()
        cursor.execute("INSERT INTO senha_mestre (hash) VALUES (%s)", (hashed,))
        sql.comando_sql("COMMIT")
        sql.close_conexao()
    except Exception as e:
        print(f"Erro ao armazenar hash da senha: {e}")
        
#Funcão principal
senha = input("Digite a senha mestre: ")
comprimento = len(senha)
salt = gerar_salt()
try:
    senha_hash = hash_senha(senha, salt)
except Exception as e:
    print(f"Erro ao gerar hash da senha: {e}")
try:
    armazenar_hash_senha(senha_hash)
except Exception as e:
    print(f"Erro ao armazenar a senha: {e}")
try:
    armazenar_salt(salt)
except Exception as e:
    print(f"Erro ao armazenar o salt: {e}")
    

    
    
     


