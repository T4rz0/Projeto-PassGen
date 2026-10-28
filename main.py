#Importa o tkinter e a pagina de login
import tkinter as tk
from ui.pagina_login import TelaLogin

def main():
    #inicia uma tela do tkinter
    root = tk.Tk()

    #Chama a tela de login
    app = TelaLogin(root)

    #inicia o looping de tela
    root.mainloop()

#Função para executar
if __name__ == "__main__":
    main()