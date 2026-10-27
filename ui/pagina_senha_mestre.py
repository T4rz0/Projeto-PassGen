import tkinter as tk
from tkinter import messagebox
from core import criptografia as cripto

class TelaCriarSenhaMestre:
    def __init__(self, master_window):
        self.top = tk.Toplevel(master_window)
        self.top.title("PassGen - Criar Senha Mestre")
        self.top.geometry("350x250")
        self.top.resizable(False, False)
        
        # Torna a janela modal (prende o foco nela)
        self.top.grab_set()

        # Título
        self.lbl_titulo = tk.Label(
            self.top, 
            text="Cadastrar Senha Mestre", 
            font=("Arial", 12, "bold")
        )
        self.lbl_titulo.pack(pady=10)

        # Campo: Senha Mestre
        self.lbl_senha = tk.Label(self.top, text="Nova Senha Mestre:")
        self.lbl_senha.pack(pady=2)
        self.txt_senha = tk.Entry(self.top, show="*", width=30)
        self.txt_senha.pack(pady=5)

        # Campo: Confirmar Senha Mestre
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