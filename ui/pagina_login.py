import os
import sys
import tkinter as tk
from tkinter import messagebox
import core.autenticação as authentic
from ui.pagina_senha_mestre import TelaCriarSenhaMestre

class TelaLogin:
    def __init__(self, master):
        self.master = master
        self.master.title("PassGen - Login")
        self.master.geometry("300x200")
        self.master.resizable(False, False)


        # Rótulo e Campo de Senha
        self.lbl_senha = tk.Label(master, text="Insira a Senha Mestre:")
        self.lbl_senha.pack(pady=5)
        
        self.txt_senha = tk.Entry(master, show="*", width=25)
        self.txt_senha.pack(pady=5)

        # Botão de Login
        self.btn_entrar = tk.Button(master, text="Entrar", command=self.verificar_login)
        self.btn_entrar.pack(pady=15)
        
        
        # Botão de Criar senha
        self.btn_CriarSenha = tk.Button(master, text="Criar senha", command=self.CriarSenha)
        self.btn_CriarSenha.pack(pady=15)
        
    def CriarSenha(self):
        TelaCriarSenhaMestre(self.master)
        

    def verificar_login(self, *args):
        senha = self.txt_senha.get()
        
        try:
          if authentic.verificar_senha(senha) == True:
            tk.Label(text="Senha correta")
        except Exception as e:
            print("A senha mestre não coincide") 


if __name__ == "__main__":
    root = tk.Tk()
    app = TelaLogin(root)
    root.mainloop()