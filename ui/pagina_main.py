import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox

# Adiciona a raiz do projeto ao caminho de busca do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from banco import conexao
from core import criptografia as cripto
from core.gerador import gerar_senha

class TelaMain:
    def __init__(self, master):
        self.master = master
        self.master.title("PassGen - Gerenciador de Senhas")
        self.master.geometry("700x450")
        self.master.resizable(False, False)

        # Título
        self.lbl_titulo = tk.Label(master, text="Suas Senhas Armazenadas", font=("Arial", 14, "bold"))
        self.lbl_titulo.pack(pady=10)

        # Frame da Tabela (Treeview)
        self.frame_tabela = tk.Frame(master)
        self.frame_tabela.pack(pady=5)

        # Criando a Treeview alinhada com as colunas da tabela CREDENCIAIS do seu SQL
        self.colunas = ("ID", "Site", "E-mail", "Senha")
        self.tabela = ttk.Treeview(self.frame_tabela, columns=self.colunas, show="headings", height=10)
        
        for coluna in self.colunas:
            self.tabela.heading(coluna, text=coluna)
            self.tabela.column(coluna, width=150, anchor="center")
        
        self.tabela.column("ID", width=50)
        self.tabela.pack(side=tk.LEFT, fill=tk.BOTH)

        # Scrollbar para a tabela
        self.scrollbar = ttk.Scrollbar(self.frame_tabela, orient="vertical", command=self.tabela.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tabela.configure(yscrollcommand=self.scrollbar.set)

        # Frame de Ações / Botões
        self.frame_botoes = tk.Frame(master)
        self.frame_botoes.pack(pady=15)

        self.btn_adicionar = tk.Button(self.frame_botoes, text="Adicionar Nova Senha", width=20, bg="#4CAF50", fg="white", command=self.abrir_janela_adicionar)
        self.btn_adicionar.grid(row=0, column=0, padx=5)

        self.btn_copiar = tk.Button(self.frame_botoes, text="Copiar Senha", width=15, command=self.copiar_senha)
        self.btn_copiar.grid(row=0, column=1, padx=5)

        self.btn_excluir = tk.Button(self.frame_botoes, text="Excluir Selecionado", width=18, bg="#f44336", fg="white", command=self.excluir_credencial)
        self.btn_excluir.grid(row=0, column=2, padx=5)

        self.btn_atualizar = tk.Button(self.frame_botoes, text="Atualizar Lista", width=15, command=self.carregar_credenciais)
        self.btn_atualizar.grid(row=0, column=3, padx=5)

        # Carrega os dados do banco ao iniciar a tela usando a classe conexao_sql
        self.carregar_credenciais()

    def carregar_credenciais(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        sql = None
        try:
            # Utilizando a sua classe de conexão padrão
            sql = conexao.conexao_sql()
            cursor = sql.get_cursor()
            cursor.execute("USE passgen")
            cursor.execute("SELECT ID, SITE, EMAIL, SENHA FROM credenciais")
            resultados = cursor.fetchall()
            
            for linha in resultados:
                id_cred, site, email, senha_cripto = linha
                try:
                    # Descriptografa utilizando a função do seu módulo criptografia.py
                    senha_limpa = cripto.descriptografar_senha(senha_cripto)
                except Exception:
                    senha_limpa = "[Erro ao descriptografar]"
                
                self.tabela.insert("", "end", values=(id_cred, site, email, senha_limpa))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar credenciais: {e}")
        finally:
            if sql:
                sql.close_conexao()

    def abrir_janela_adicionar(self):
        self.top_add = tk.Toplevel(self.master)
        self.top_add.title("PassGen - Adicionar Senha")
        self.top_add.geometry("300x300")
        self.top_add.resizable(False, False)
        self.top_add.grab_set()

        tk.Label(self.top_add, text="Site/Serviço:").pack(pady=2)
        self.txt_site = tk.Entry(self.top_add, width=30)
        self.txt_site.pack(pady=2)

        tk.Label(self.top_add, text="E-mail/Usuário:").pack(pady=2)
        self.txt_email = tk.Entry(self.top_add, width=30)
        self.txt_email.pack(pady=2)

        tk.Label(self.top_add, text="Senha:").pack(pady=2)
        self.txt_senha_nova = tk.Entry(self.top_add, width=30)
        self.txt_senha_nova.pack(pady=2)

        self.btn_gerar = tk.Button(self.top_add, text="Gerar Senha Automática", command=self.preencher_senha_gerada)
        self.btn_gerar.pack(pady=5)

        self.btn_salvar = tk.Button(self.top_add, text="Salvar", bg="#2196F3", fg="white", command=self.salvar_nova_credencial)
        self.btn_salvar.pack(pady=10)

    def preencher_senha_gerada(self):
        # Chamando a função diretamente do seu gerador.py (ex: comprimento 12, números=True, especiais=True)
        senha_aleatoria = gerar_senha(12, True, True)
        self.txt_senha_nova.delete(0, tk.END)
        self.txt_senha_nova.insert(0, senha_aleatoria)

    def salvar_nova_credencial(self):
        site = self.txt_site.get()
        email = self.txt_email.get()
        senha_limpa = self.txt_senha_nova.get()

        if not site or not email or not senha_limpa:
            messagebox.showwarning("Atenção", "Preencha todos os campos!", parent=self.top_add)
            return

        sql = None
        try:
            # Criptografa a senha usando a função Fernet de criptografia.py
            senha_criptografada = cripto.criptografar_senha(senha_limpa)

            # Usando os métodos da sua classe conexao_sql para persistência
            sql = conexao.conexao_sql()
            cursor = sql.get_cursor()
            cursor.execute("USE passgen")
            
            comando = "INSERT INTO credenciais (SITE, EMAIL, SENHA) VALUES (%s, %s, %s)"
            sql.comando_sql(comando, (site, email, senha_criptografada))

            messagebox.showinfo("Sucesso", "Credencial salva com sucesso!", parent=self.top_add)
            self.top_add.destroy()
            self.carregar_credenciais()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar credencial: {e}", parent=self.top_add)
        finally:
            if sql:
                sql.close_conexao()

    def copiar_senha(self):
        selected_item = self.tabela.selection()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione uma credencial na tabela.")
            return
        
        item_data = self.tabela.item(selected_item)
        senha = item_data['values'][3] # Coluna da senha
        
        self.master.clipboard_clear()
        self.master.clipboard_append(senha)
        messagebox.showinfo("Sucesso", "Senha copiada para a área de transferência!")

    def excluir_credencial(self):
        selected_item = self.tabela.selection()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione uma credencial para excluir.")
            return
        
        item_data = self.tabela.item(selected_item)
        id_cred = item_data['values'][0]

        confirmacao = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir esta credencial?")
        if confirmacao:
            sql = None
            try:
                sql = conexao.conexao_sql()
                cursor = sql.get_cursor()
                cursor.execute("USE passgen")
                
                comando = "DELETE FROM credenciais WHERE ID = %s"
                sql.comando_sql(comando, (id_cred,))

                messagebox.showinfo("Sucesso", "Credencial excluída com sucesso!")
                self.carregar_credenciais()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir: {e}")
            finally:
                if sql:
                    sql.close_conexao()

if __name__ == "__main__":
    root = tk.Tk()
    app = TelaMain(root)
    root.mainloop()