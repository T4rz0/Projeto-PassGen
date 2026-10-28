#Importa o TKinter para a GUI
import tkinter as tk
from tkinter import ttk, messagebox

#Importa classes e metodos meus
from banco import conexao
from core import criptografia as cripto
from core.gerador import gerar_senha

# Largura da tabela e de cada coluna: ID, Site, E-mail, Senha
LARGURAS = (50, 150, 210, 210)
FONTE = ("Consolas", 10)
FONTE_CAB = ("Consolas", 10, "bold")
COR_NORMAL = "#ffffff"
COR_SELECIONADA = "#cfe8ff"

#Classe da tela
class TelaMain:
    def __init__(self, master):
        self.master = master
        self.master.title("PassGen - Gerenciador de Senhas")
        self.master.geometry("720x450")
        self.master.resizable(False, False)

        self.id_selecionado = None
        self.linhas = {}

        # Título
        self.lbl_titulo = tk.Label(master, text="Suas Senhas Armazenadas", font=("Arial", 14, "bold"))
        self.lbl_titulo.pack(pady=10)

        # Subtexto para dica de uso
        tk.Label(
            master,
            text="Clique em uma linha para selecioná-la. Selecione o texto (duplo clique = campo todo) e use copie",
            fg="gray",
        ).pack()

        # Cabeçalho
        self.frame_cabecalho = tk.Frame(master)
        self.frame_cabecalho.pack(padx=10, pady=(8, 0), anchor="w")
        for col, (nome, larg) in enumerate(zip(("ID", "Site", "E-mail", "Senha"), LARGURAS)):
            self.frame_cabecalho.columnconfigure(col, minsize=larg)
            tk.Label(
                self.frame_cabecalho, text=nome, font=FONTE_CAB,
                bg="#e0e0e0", relief="groove", pady=3
            ).grid(row=0, column=col, sticky="ew", padx=1)

        # Área rolável com as linhas
        self.frame_tabela = tk.Frame(master)
        self.frame_tabela.pack(padx=10, pady=2, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.frame_tabela, height=240, width=sum(LARGURAS) + 10, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.frame_tabela, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.inner = tk.Frame(self.canvas)
        for col, larg in enumerate(LARGURAS):
            self.inner.columnconfigure(col, minsize=larg)
        self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self._rolar_mouse)

        # Botões
        self.frame_botoes = tk.Frame(master)
        self.frame_botoes.pack(pady=15)

        self.btn_adicionar = tk.Button(self.frame_botoes, text="Adicionar Nova Senha", width=20, bg="#4CAF50", fg="white", command=self.abrir_janela_adicionar)
        self.btn_adicionar.grid(row=0, column=0, padx=5)

        self.btn_excluir = tk.Button(self.frame_botoes, text="Excluir Selecionado", width=18, bg="#f44336", fg="white", command=self.excluir_credencial)
        self.btn_excluir.grid(row=0, column=1, padx=5)

        self.btn_atualizar = tk.Button(self.frame_botoes, text="Atualizar Lista", width=15, command=self.carregar_credenciais)
        self.btn_atualizar.grid(row=0, column=2, padx=5)

        self.carregar_credenciais()

    #Função de rolar o mouse na tabela
    def _rolar_mouse(self, event):
        self.canvas.yview_scroll(int(-event.delta / 120), "units")

    #função de selecionar cada credêncial com o duplo clique
    def _selecionar_tudo(self, event):
        event.widget.select_range(0, tk.END)
        event.widget.icursor(tk.END)
        return "break"

    #Cria cada campo da tabela com as credênciais
    def _criar_campo(self, linha, coluna, texto, largura, id_cred):
        ent = tk.Entry(
            self.inner, width=1, justify="center", font=FONTE,
            relief="solid", borderwidth=1,
            readonlybackground=COR_NORMAL,
            disabledforeground="black",
        )
        ent.insert(0, str(texto))
        ent.configure(state="readonly")  # selecionável e copiável, mas não editável
        ent.grid(row=linha, column=coluna, sticky="ew", padx=1, pady=0, ipady=3)

        ent.bind("<Button-1>", lambda e, i=id_cred: self.selecionar_linha(i), add="+")
        ent.bind("<Double-Button-1>", self._selecionar_tudo)
        ent.bind("<Control-a>", self._selecionar_tudo)
        return ent

    #Destaca a linha selecionada
    def selecionar_linha(self, id_cred):
        if self.id_selecionado in self.linhas:
            for ent in self.linhas[self.id_selecionado]:
                ent.configure(readonlybackground=COR_NORMAL)
        self.id_selecionado = id_cred
        for ent in self.linhas.get(id_cred, []):
            ent.configure(readonlybackground=COR_SELECIONADA)

    #Carrega nos campos da tabela as credênciasis
    def carregar_credenciais(self):
        for widget in self.inner.winfo_children():
            widget.destroy()
        self.linhas = {}
        self.id_selecionado = None

        sql = None
        try:
            sql = conexao.conexao_sql()
            cursor = sql.get_cursor()
            cursor.execute("USE passgen")
            cursor.execute("SELECT ID, SITE, EMAIL, SENHA FROM credenciais")
            resultados = cursor.fetchall()

            for i, (id_cred, site, email, senha_cripto) in enumerate(resultados):
                try:
                    senha_limpa = cripto.descriptografar_senha(senha_cripto)
                except Exception:
                    senha_limpa = "[Erro ao descriptografar]"

                valores = (id_cred, site, email, senha_limpa)
                self.linhas[id_cred] = [
                    self._criar_campo(i, col, val, LARGURAS[col], id_cred)
                    for col, val in enumerate(valores)
                ]
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar credenciais: {e}")
        finally:
            if sql:
                sql.close_conexao()

    #Tela adicionar credêncial
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

    #Preenche o campo da senha com a senha gerada
    def preencher_senha_gerada(self):
        senha_aleatoria = gerar_senha(12, True, True)
        self.txt_senha_nova.delete(0, tk.END)
        self.txt_senha_nova.insert(0, senha_aleatoria)

    #Funcão para salvar a credêncial
    def salvar_nova_credencial(self):
        site = self.txt_site.get()
        email = self.txt_email.get()
        senha_limpa = self.txt_senha_nova.get()

        if not site or not email or not senha_limpa:
            messagebox.showwarning("Atenção", "Preencha todos os campos!", parent=self.top_add)
            return

        sql = None
        try:
            senha_criptografada = cripto.criptografar_senha(senha_limpa)

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

    #Função para excluir a credêncial
    def excluir_credencial(self):
        if self.id_selecionado is None:
            messagebox.showwarning("Atenção", "Clique em uma linha para selecioná-la antes de excluir.")
            return

        id_cred = self.id_selecionado

        if messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir esta credencial?"):
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