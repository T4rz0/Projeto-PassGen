from banco import conexao
import bcrypt

#Função para verificar a senha
def verificar_senha(senha_escrita):

    sql = conexao.conexao_sql()
    cursor = sql.get_cursor()
    try:
        cursor.execute("USE passgen")
        cursor.execute("SELECT ver_senham FROM configuracao")
        senhas_mestre = cursor.fetchall()
    
       #Função para verificar a senha mestre usando o salt 
        if not senhas_mestre:
           sql.close_conexao()
           print("Não existe nenhuma senha mestre")
           return False
        for linha in senhas_mestre:
            hash_armazenado = bytes(linha[0])
            
            #Faz a checagem descriptografando com base no hash
            if bcrypt.checkpw(senha_escrita.encode('utf-8'), hash_armazenado):
                print("Senha mestre correta!")
                sql.close_conexao()
                return True
            else:
                print("Senha mestre incorreta!")
                sql.close_conexao()
                return False
    except Exception as e:
        print(f"Erro ao verificar a senha: {e}")   
        
#Função principal para testar a verificação
if __name__ == "__main__":
    senha = input("Digite sua senha:")
    verificar_senha(senha)
    