import os
import sys
from tabulate import tabulate

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from banco import conexao
from core import criptografia as cripto

#Add opção de selecionar se quer com senha digitada ou senha gerada
def create(site, email, senha):
    try:
        sql = conexao.conexao_sql()
        cursor = sql.get_cursor()
        cursor.execute("USE passgen")
        
        salt = cripto.gerar_salt()
        senha_hash = cripto.hash_senha(senha, salt)
        cursor.execute("INSERT INTO credenciais (site, email, senha) VALUES (%s, %s, %s)", (site, email, senha_hash))
        sql.conexao.commit()
        sql.close_conexao()
    except Exception as e:
        print(f"Não foi possivel adicionar ao banco {e}")

def read():
    try:
        sql = conexao.conexao_sql()
        cursor = sql.get_cursor()
        cursor.execute("USE passgen")
        cursor.execute("SELECT * FROM credenciais")
        results = cursor.fetchall()
        sql.close_conexao()
        return results
    except Exception as e:
        print(f"Não foi possivel obter as credênciais {e}")
        
def update(tipo):
    sql = conexao.conexao_sql()
    cursor = sql.get_cursor()
    cursor.execute("USE passgen")
    nome_site = input("Qual o nome do site que você deseja alterar? ")
    match tipo:
        case "site":
            try:
                novo_site = input("Qual o novo site? ")
                cursor.execute("UPDATE credenciais SET site = %s WHERE site = %s", (novo_site, nome_site))
                print("O conteúdo foi alterado com sucesso")
            except Exception as e:
                print(f"Não foi possivel alterar o nome do site {e}")
                
        case "email":
            try:
                novo_email = input("Qual o novo email? ")
                cursor.execute("UPDATE credenciais SET email = %s WHERE site = %s", (novo_email, nome_site))
                print("O conteúdo foi alterado com sucesso")
            except Exception as e:
                    print(f"Não foi possivel alterar o email no site {e}")
                    
        case "senha":
            try:
                nova_senha = input("Qual a nova senha? ")
                salt = cripto.gerar_salt()
                senha_hash = cripto.hash_senha(nova_senha, salt)
                cursor.execute("UPDATE credenciais SET senha = %s WHERE site = %s", (senha_hash, nome_site))
                print("O conteúdo foi alterado com sucesso")
            except Exception as e:
                    print(f"Não foi possivel alterar a senha no site {e}")
            
        case "tudo":
            try:
                salt = cripto.gerar_salt()
                senha_hash = cripto.hash_senha(senha, salt)
                cursor.execute("UPDATE credenciais SET site = %s email = %s, senha = %s WHERE site = %s", (novo_site,novo_email, senha_hash, nome_site))
                print("O conteúdo foi alterado com sucesso")
            except Exception as e:
                print(f"Não foi possivel alterar as credenciais{e}")
    sql.conexao.commit()
    sql.close_conexao()
   
        
def delete(site):
    try:
        sql = conexao.conexao_sql()
        cursor = sql.get_cursor()
        cursor.execute("USE passgen")
        cursor.execute("DELETE FROM credenciais WHERE site = %s", (site,))
        sql.conexao.commit()
        sql.close_conexao()
    except Exception as e:
        print(f"Não foi possivel deletar a credêncial {e}")
    
def procura_por_site(site):
    sql = conexao.conexao_sql()
    cursor = sql.get_cursor()
    cursor.execute("USE passgen")
    cursor.execute("SELECT * FROM credenciais WHERE site = %s", (site,))
    result = cursor.fetchone()
    sql.close_conexao()
    return result

#faça um crud em match para testar as funçoes
print("Menu de Teste")
resp=input("O que deseja testar?")
match resp.lower():
    case "create":
        site = input("Qual o site? ")
        email = input("Qual o email? ")
        senha = input("Qual a senha? ")
        create(site, email, senha)
    case "delete":
        opt = input("De qual site é a credencial você deseja excluir?")
        delete(opt)
    case "listar":
        print(tabulate(read()))
    case "modificar":
        opt = input("O que você deseja mudar? ")
        update(opt)
     