import tkinter as tk
from tkinter import messagebox
import core.autenticação as authentic
from ui.pagina_main import TelaMain
from ui.pagina_senha_mestre import TelaCriarSenhaMestre
from banco import conexao

class TelaLogin:
    def __init__(self, master):
        self.master = master
        self.master.title("PassGen - Login")
        self.master.geometry("300x200")
        self.master.resizable(False, False)

        self.checar_primeiro_acesso()

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
        

    def verificar_login(self):
        senha = self.txt_senha.get()
        try:
            if authentic.verificar_senha(senha) == True:
                self.master.destroy() # Fecha a tela de login
                root_main = tk.Tk()
                TelaMain(root_main)
                root_main.mainloop()
            else:
                messagebox.showerror("Erro de login","A senha não coincide")
        except Exception as e:
            print("A senha mestre não coincide") 
            
    def verificar_existencia_senha(self):

        sql = None
        try:
            sql = conexao.conexao_sql()
            cursor = sql.get_cursor()
            cursor.execute("USE passgen")
            cursor.execute("SELECT COUNT(*) FROM configuracao")
            resultado = cursor.fetchone()
            
            if resultado and resultado[0] > 0:
                return True
        except Exception as e:
            print(f"Erro ao verificar senha mestre: {e}")
        finally:
            if sql:
                sql.close_conexao()
        return False

    def checar_primeiro_acesso(self):
        """Exibe um aviso automático caso o banco de dados esteja sem senha mestre."""
        if not self.verificar_existencia_senha():
            messagebox.showwarning(
                "Atenção - Primeiro Acesso", 
                "Nenhuma Senha Mestre encontrada no banco de dados!\nPor favor, cadastre uma nova senha.",
                parent=self.master
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = TelaLogin(root)
    
    root.mainloop()