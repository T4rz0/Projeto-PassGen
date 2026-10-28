#Importa o tkinter para a GUI
import tkinter as tk
from tkinter import messagebox

#Importa cada classe minha
from core import criptografia as cripto
from banco import conexao

#Classe da tela para cadastrar uma senha mestre
class TelaCriarSenhaMestre:
    def __init__(self, master_window):
        if self.verificar_existencia_senha():
            messagebox.showwarning("Atenção","Já existe uma Senha Mestre")
            return
        
        self.top = tk.Toplevel(master_window)
        self.top.title("PassGen - Criar Senha Mestre")
        self.top.geometry("350x250")
        self.top.resizable(False, False)
        
        # Foca na tela
        self.top.grab_set()

        # Título
        self.lbl_titulo = tk.Label(
            self.top, 
            text="Cadastrar Senha Mestre", 
            font=("Arial", 12, "bold")
        )
        self.lbl_titulo.pack(pady=10)

        # Campo da senha mestre
        self.lbl_senha = tk.Label(self.top, text="Nova Senha Mestre:")
        self.lbl_senha.pack(pady=2)
        self.txt_senha = tk.Entry(self.top, show="*", width=30)
        self.txt_senha.pack(pady=5)

        # Campo de confirmação
        self.lbl_confirmar = tk.Label(self.top, text="Confirme a Senha Mestre:")
        self.lbl_confirmar.pack(pady=2)
        self.txt_confirmar = tk.Entry(self.top, show="*", width=30)
        self.txt_confirmar.pack(pady=5)

        # Botão Salvar
        self.btn_salvar = tk.Button(
            self.top, 
            text="Salvar Senha Mestre", 
            command=self.salvar_senha_mestre
        )
        self.btn_salvar.pack(pady=15)
     
    #Funcao para verificar se já existe alguma senha mestre   
    def verificar_existencia_senha(self):
            try:
                sql = conexao.conexao_sql()
                cursor = sql.get_cursor()
                cursor.execute("USE passgen")
                cursor.execute("SELECT COUNT(*) FROM configuracao")
                resultado = cursor.fetchone()
                sql.close_conexao()
                
                if resultado and resultado[0] > 0:
                    return True
            except Exception as e:
                print(f"Erro ao verificar senha mestre: {e}")
            return False

    #Função para armazenar a senha mestre
    def salvar_senha_mestre(self):
        senha = self.txt_senha.get()
        confirmacao = self.txt_confirmar.get()

        if not senha or not confirmacao:
            messagebox.showwarning("Atenção", "Preencha todos os campos!", parent=self.top)
            return

        if senha != confirmacao:
            messagebox.showerror("Erro", "As senhas não coincidem!", parent=self.top)
            return

        try:
            salt = cripto.gerar_salt()
            senha_mestre =cripto.hash_senha_mestre(senha, salt)
            cripto.armazenar_hash_senha(salt, senha_mestre)
            messagebox.showinfo("Sucesso", "Senha Mestre criada com sucesso!", parent=self.top)
            self.top.destroy()  # Fecha esta tela e retorna ao login
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar: {e}", parent=self.top)