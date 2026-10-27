import tkinter as tk
from ui.pagina_login import TelaLogin  # Certifique-se de que o nome do arquivo/classe corresponde ao seu projeto
# Opcional: importar inicialização do banco de dados, caso queira garantir que ele existe ao iniciar
# from banco.conexao import criar_conexao

def main():
    # 1. (Opcional) Inicializações prévias, como banco de dados ou configurações
    # criar_conexao()

    # 2. Inicializa a janela principal do Tkinter
    root = tk.Tk()

    # 3. Chama a primeira tela do sistema (Tela de Login)
    app = TelaLogin(root)

    # 4. Inicia o loop principal da interface gráfica (mantém a janela aberta)
    root.mainloop()

if __name__ == "__main__":
    main()