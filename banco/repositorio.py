import os
import sys
from tabulate import tabulate
from cryptography.fernet import Fernet

#Marca o diretório principal para encontrar os arquivos locais necessários para o uso
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from banco import conexao
from core import criptografia as cripto
from core import gerador

#Add opção de selecionar se quer com senha digitada ou senha gerada
def create(site, email, senha):
    try:
        sql = conexao.conexao_sql()
        cursor = sql.get_cursor()
        cursor.execute("USE passgen")
        
        senha_cripto = cripto.criptografar_senha(senha)
        
        cursor.execute("INSERT INTO credenciais (site, email, senha) VALUES (%s, %s, %s)", (site, email, senha_cripto))
        sql.conexao.commit()
        sql.close_conexao()
        print("Credênciais salvas com sucesso!")
    except Exception as e:
        print(f"Não foi possivel adicionar ao banco {e}")
    
def create_gerada(site, email):
    try:
        sql = conexao.conexao_sql()
        cursor = sql.get_cursor()
        cursor.execute("USE passgen")
        
        comprimento = int(input("Qual o tamanho da senha? "))
        numeros = input("Terá números e letras? (s/n): ").strip().lower()
        especiais = input("Terá caracteres especiais? (s/n): ").strip().lower()
        
        senha_gerada = gerador.gerar_senha(comprimento, numeros, especiais)
        
        senha_cripto = cripto.criptografar_senha(senha_gerada)
        
        cursor.execute("INSERT INTO credenciais (site, email, senha) VALUES (%s, %s, %s)", (site, email, senha_cripto))
        sql.conexao.commit()
        sql.close_conexao()
        print("Credênciais salvas com sucesso!")
    except Exception as e:
        print(f"Não foi possivel adicionar ao banco {e}")

#Lista todas as credenciais
def read():
    try:
        sql = conexao.conexao_sql()
        cursor = sql.get_cursor()
        cursor.execute("USE passgen")
        cursor.execute("SELECT site, email, senha, criado FROM credenciais")
        results = cursor.fetchall()
        sql.close_conexao()
        
        #lista feita para armazenar dados para exibir
        lista_limpa = []
        for linha in results:
            site, email, senha, criado = linha
            
            try:
                senha_limpa = cripto.descriptografar_senha(senha)
            except Exception as e:
                print("Não foi possivel descriptografar a senha")
            lista_limpa.append([site,email,senha_limpa,criado])
        
        #cabeçalhos da tabela para exibição
        cabecalhos = ["Site", "E-mail", "Senha", "Criado em"]
        
        # Retorna a tabela formatada utilizando o tabulate
        return tabulate(lista_limpa, headers=cabecalhos, tablefmt="fancy_grid")
    except Exception as e:
        print(f"Não foi possivel obter as credênciais {e}")
        return []
          
#Modifica toda a credencial ou apenas partes        
def update(tipo):
    sql = conexao.conexao_sql()
    cursor = sql.get_cursor()
    cursor.execute("USE passgen")
    match tipo:
        case "site":
            try:
                email = input("Qual o email cadastrado no site que você deseja alterar? ")
                novo_site = input("Qual o novo site? ")
                cursor.execute("UPDATE credenciais SET site = %s WHERE email = %s", (novo_site, email))
                print(f"O nome do site foi alterado")
            except Exception as e:
                print(f"Não foi possivel alterar o nome do site {e}")
                
        case "email":
            try:
                email = input("Qual o email cadastrado no site que você deseja alterar? ")
                novo_email = input("Qual o novo email? ")
                cursor.execute("UPDATE credenciais SET email = %s WHERE email = %s", (novo_email, email))
                print(f"O email do site foi alterado")
            except Exception as e:
                    print(f"Não foi possivel alterar o email no site {e}")
                    
        case "senha":
            try:
                email = input("Qual o email cadastrado no site que você deseja alterar? ")
                opt = input("Você deseja gerar uma senha?").strip().lower()
                if opt == "sim":
                    comprimento = int(input("Qual o tamanho da senha? "))
                    numeros = input("Terá números e letras? (s/n): ").strip().lower()
                    especiais = input("Terá caracteres especiais? (s/n): ").strip().lower()
                            
                    senha_gerada = gerador.gerar_senha(comprimento, numeros, especiais)
                            
                    senha = cripto.criptografar_senha(senha_gerada)
                else:
                    senha_limpa = input("Qual a nova senha?")
                    senha = cripto.criptografar_senha(senha_limpa)
                cursor.execute("UPDATE credenciais SET senha = %s WHERE email = %s", (senha, email))
                print(f"A senha do site foi alterada")
            except Exception as e:
                print(f"Não foi possivel alterar a senha no site {e}")
            
        case "tudo":
            try:
                email = input("Qual o email cadastrado no site que você deseja alterar? ")
                novo_site = input("Qual o novo nome do site?")
                novo_email = input("Qual o novo email?")
                opt = input("Você deseja gerar uma senha?").strip().lower()
                if opt == "sim":
                    comprimento = int(input("Qual o tamanho da senha? "))
                    numeros = input("Terá números e letras? (s/n): ").strip().lower()
                    especiais = input("Terá caracteres especiais? (s/n): ").strip().lower()
                            
                    senha_gerada = gerador.gerar_senha(comprimento, numeros, especiais)
                            
                    senha = cripto.criptografar_senha(senha_gerada)
                else:
                    senha_limpa = input("Qual a nova senha?")
                    senha = cripto.criptografar_senha(senha_limpa)
                
                cursor.execute("UPDATE credenciais SET site = %s, email = %s, senha = %s WHERE email = %s", (novo_site, novo_email, senha, email))
                print(f"O conteúdo todo do site foi alterado com sucesso")
            except Exception as e:
                print(f"Não foi possivel alterar as credenciais {e}")
    sql.conexao.commit()
    sql.close_conexao()
   
#Deleta as credenciais        
def delete(email):
    try:
        sql = conexao.conexao_sql()
        cursor = sql.get_cursor()
        cursor.execute("USE passgen")
        cursor.execute("DELETE FROM credenciais WHERE email = %s", (email,))
        sql.conexao.commit()
        sql.close_conexao()
        print(f"Credenciais do site excluido com sucesso")
    except Exception as e:
        print(f"Não foi possivel deletar as credênciais do site {e}")

#Procura a credêncial com base no site    
def procura_por_site(site):
    try:
        sql = conexao.conexao_sql()
        cursor = sql.get_cursor()
        cursor.execute("USE passgen")
        cursor.execute("SELECT site, email, senha, criado FROM credenciais WHERE site = %s", (site,))
        results = cursor.fetchall()
        sql.close_conexao()
            
            #lista feita para armazenar dados para exibir
        lista_limpa = []
        for linha in results:
            site, email, senha, criado = linha
                
            try:
                senha_limpa = cripto.descriptografar_senha(senha)
            except Exception as e:
                print("Não foi possivel descriptografar a senha")
            lista_limpa.append([site,email,senha_limpa,criado])
            
            #cabeçalhos da tabela para exibição
            cabecalhos = ["Site", "E-mail", "Senha", "Criado em"]
            
            # Retorna a tabela formatada utilizando o tabulate
            return tabulate(lista_limpa, headers=cabecalhos, tablefmt="fancy_grid")
    except Exception as e:
        print(f"Não foi possivel obter as credênciais {e}")
        return []
        
#Menu simples para teste no terminal
def menu_teste():
    while True:
        print("\n=== Menu de teste ===")
        print("1 - Cadastrar credencial")
        print("2 - Listar credenciais")
        print("3 - Modificar credencial")
        print("4 - Excluir credencial")
        print("5 - Procurar credencial")
        print("0 - Sair")

        match input("Escolha uma opção: ").strip():
            case "1":
                site = input("Qual o site? ").strip()
                email = input("Qual o email? ").strip()
                print("\n1 - Digitar uma senha")
                print("2 - Gerar uma senha")

                match input("Como deseja definir a senha? ").strip():
                    case "1":
                        senha = input("Qual a senha? ")
                        create(site, email, senha)
                    case "2":
                        create_gerada(site, email)
                    case _:
                        print("Opção inválida. Cadastro cancelado.")
            case "2":
                print(read())
            case "3":
                print("\nQual informação deseja modificar?")
                print("1 - Site")
                print("2 - Email")
                print("3 - Senha")
                print("4 - Todas as informações")

                match input("Escolha uma opção: ").strip():
                    case "1":
                        update("site")
                    case "2":
                        update("email")
                    case "3":
                        update("senha")
                    case "4":
                        update("tudo")
                    case _:
                        print("Opção inválida. Nenhuma alteração realizada.")
            case "4":
                email = input("Qual o email que deseja excluir? ")
                delete(email)
            case "5":
                site = input("Qual o site da credencial que deseja procurar? ").strip()
                resultado = procura_por_site(site)
                print(resultado if resultado else "Nenhuma credencial encontrada.")
            case "0":
                print("Saindo do menu de teste.")
                break
            case _:
                print("Opção inválida. Escolha uma opção do menu.")

#Main para a execução
if __name__ == "__main__":
    menu_teste()
     