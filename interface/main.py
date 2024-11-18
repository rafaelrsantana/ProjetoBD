import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from datetime import datetime

# Função para conectar ao banco de dados
def conectar():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="biblioteca",
            user="postgres",
            password="1381",
            client_encoding="utf-8"
        )
        conn.set_client_encoding('UTF8')
        return conn
    except Exception as e:
        print("Erro na conexão:", e)
        return None

# Funções para usuários

# Listar usuários
def listar_usuarios():
    janela_listar = tk.Toplevel()
    janela_listar.title("Listagem de Usuários")
    
    tree = ttk.Treeview(janela_listar, columns=("ID", "Nome", "Email", "Telefone"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("Email", text="Email")
    tree.heading("Telefone", text="Telefone")
    tree.pack(fill=tk.BOTH, expand=True)

    conn = conectar()
    if conn is None:
        messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, email, telefone FROM Usuario")
        usuarios = cursor.fetchall()
        for usuario in usuarios:
            tree.insert("", tk.END, values=usuario)
        conn.close()
    except Exception as e:
        print("Erro ao listar usuários:", e)
        messagebox.showerror("Erro", "Erro ao listar usuários.")

# Cadastrar usuário
def cadastrar_usuario():
    def salvar():
        nome = entry_nome.get()
        email = entry_email.get()
        telefone = entry_telefone.get()


        if not nome or not email:
            messagebox.showerror("Erro", "Nome e e-mail são obrigatórios.")
            return

        conn = conectar()
        if conn is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Usuario (nome, email, telefone) VALUES (%s, %s, %s)",
                (nome, email, telefone)
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            janela_cadastrar.destroy()
        except Exception as e:
            print("Erro ao cadastrar usuário:", e)
            messagebox.showerror("Erro", "Erro ao cadastrar usuário.")

    janela_cadastrar = tk.Toplevel()
    janela_cadastrar.title("Cadastrar Usuário")

    tk.Label(janela_cadastrar, text="Nome:").grid(row=0, column=0, padx=10, pady=10)
    entry_nome = tk.Entry(janela_cadastrar)
    entry_nome.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(janela_cadastrar, text="Email:").grid(row=1, column=0, padx=10, pady=10)
    entry_email = tk.Entry(janela_cadastrar)
    entry_email.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(janela_cadastrar, text="Telefone:").grid(row=2, column=0, padx=10, pady=10)
    entry_telefone = tk.Entry(janela_cadastrar)
    entry_telefone.grid(row=2, column=1, padx=10, pady=10)

    tk.Button(janela_cadastrar, text="Salvar", command=salvar).grid(row=3, column=0, columnspan=2, pady=10)

# Edição de usuário
def editar_usuario():
    def carregar_dados():
        usuario_id = entry_id.get()
        conn = conectar()
        if conn is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            return
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT nome, email, telefone FROM Usuario WHERE id = %s", (usuario_id,))
            usuario = cursor.fetchone()
            if usuario:
                entry_nome.insert(0, usuario[0])
                entry_email.insert(0, usuario[1])
                entry_telefone.insert(0, usuario[2])
            else:
                messagebox.showerror("Erro", "Usuário não encontrado.")
            conn.close()
        except Exception as e:
            print("Erro ao carregar dados:", e)
            messagebox.showerror("Erro", "Erro ao carregar dados do usuário.")

    def salvar_edicao():
        usuario_id = entry_id.get()
        nome = entry_nome.get()
        email = entry_email.get()
        telefone = entry_telefone.get()

        conn = conectar()
        if conn is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            return
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Usuario SET nome = %s, email = %s, telefone = %s WHERE id = %s",
                (nome, email, telefone, usuario_id)
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!")
            janela_editar.destroy()
        except Exception as e:
            print("Erro ao salvar edição:", e)
            messagebox.showerror("Erro", "Erro ao salvar edição do usuário.")

    janela_editar = tk.Toplevel()
    janela_editar.title("Editar Usuário")

    tk.Label(janela_editar, text="ID do Usuário:").grid(row=0, column=0, padx=10, pady=10)
    entry_id = tk.Entry(janela_editar)
    entry_id.grid(row=0, column=1, padx=10, pady=10)

    tk.Button(janela_editar, text="Carregar Dados", command=carregar_dados).grid(row=0, column=2, padx=10, pady=10)

    tk.Label(janela_editar, text="Nome:").grid(row=1, column=0, padx=10, pady=10)
    entry_nome = tk.Entry(janela_editar)
    entry_nome.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(janela_editar, text="Email:").grid(row=2, column=0, padx=10, pady=10)
    entry_email = tk.Entry(janela_editar)
    entry_email.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(janela_editar, text="Telefone:").grid(row=3, column=0, padx=10, pady=10)
    entry_telefone = tk.Entry(janela_editar)
    entry_telefone.grid(row=3, column=1, padx=10, pady=10)

    tk.Button(janela_editar, text="Salvar", command=salvar_edicao).grid(row=4, column=0, columnspan=3, pady=10)

# Excluir usuário
def excluir_usuario():
    def excluir():
        usuario_id = entry_id.get()
        senha_admin = entry_senha.get()

        if not usuario_id.isdigit():
            messagebox.showerror("Erro", "ID inválido.")
            return

        conn = conectar()
        if conn is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            return

        try:
            cursor = conn.cursor()

            # Verificar a senha do administrador no banco de dados
            cursor.execute("SELECT senha FROM Administradores LIMIT 1")
            resultado = cursor.fetchone()
            if resultado is None:
                messagebox.showerror("Erro", "Administrador não encontrado.")
                return

            senha_correta = resultado[0]

            if senha_admin != senha_correta:
                messagebox.showerror("Erro", "Senha de administrador incorreta.")
                return

            # Excluir registros relacionados na tabela Aluguel
            cursor.execute("DELETE FROM Aluguel WHERE usuario_id = %s", (usuario_id,))

            # Excluir o usuário
            cursor.execute("DELETE FROM Usuario WHERE id = %s", (usuario_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
            janela_excluir.destroy()
        except Exception as e:
            print("Erro ao excluir usuário:", e)
            messagebox.showerror("Erro", "Erro ao excluir usuário.")

    janela_excluir = tk.Toplevel()
    janela_excluir.title("Excluir Usuário")

    tk.Label(janela_excluir, text="ID do Usuário:").grid(row=0, column=0, padx=10, pady=10)
    entry_id = tk.Entry(janela_excluir)
    entry_id.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(janela_excluir, text="Senha de Administrador:").grid(row=1, column=0, padx=10, pady=10)
    entry_senha = tk.Entry(janela_excluir, show="*")
    entry_senha.grid(row=1, column=1, padx=10, pady=10)

    tk.Button(janela_excluir, text="Excluir", command=excluir).grid(row=2, column=0, columnspan=2, pady=10)

# Funções para livros
# Listar livros
def listar_livros():
    janela_listar = tk.Toplevel()
    janela_listar.title("Listagem de Livros")

    tk.Label(janela_listar, text="Buscar:").pack(pady=5)
    entry_busca = tk.Entry(janela_listar)
    entry_busca.pack(pady=5)


    def atualizar_lista(*args):
        termo = entry_busca.get()
        conn = conectar()
        if conn is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            return
        try:
            cursor = conn.cursor()
            consulta = "SELECT id, titulo, autor, ano, disponibilidade FROM Livro WHERE titulo ILIKE %s OR autor ILIKE %s"
            cursor.execute(consulta, ('%' + termo + '%', '%' + termo + '%'))
            livros = cursor.fetchall()
            tree.delete(*tree.get_children())
            for livro in livros:
                disponibilidade = "Sim" if livro[4] else "Não"
                tree.insert("", tk.END, values=(livro[0], livro[1], livro[2], livro[3], disponibilidade))
            conn.close()
        except Exception as e:
            print("Erro ao listar livros:", e)
            messagebox.showerror("Erro", "Erro ao listar livros.")

    entry_busca.bind("<KeyRelease>", atualizar_lista)
    
    tree = ttk.Treeview(janela_listar, columns=("ID", "Título", "Autor", "Ano", "Disponibilidade"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Título", text="Título")
    tree.heading("Autor", text="Autor")
    tree.heading("Ano", text="Ano")
    tree.heading("Disponibilidade", text="Disponível")
    tree.pack(fill=tk.BOTH, expand=True)

    conn = conectar()
    if conn is None:
        messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, titulo, autor, ano, disponibilidade FROM Livro")
        livros = cursor.fetchall()
        for livro in livros:
            disponibilidade = "Sim" if livro[4] else "Não"
            tree.insert("", tk.END, values=(livro[0], livro[1], livro[2], livro[3], disponibilidade))
        conn.close()
    except Exception as e:
        print("Erro ao listar livros:", e)
        messagebox.showerror("Erro", "Erro ao listar livros.")

# Cadastrar livro
def cadastrar_livro():
    def salvar():
        titulo = entry_titulo.get()
        autor = entry_autor.get()
        ano = entry_ano.get()
        disponibilidade = var_disponibilidade.get() == "Sim"

        conn = conectar()
        if conn is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Livro (titulo, autor, ano, disponibilidade) VALUES (%s, %s, %s, %s)",
                (titulo, autor, ano, disponibilidade)
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Livro cadastrado com sucesso!")
            janela_cadastrar.destroy()
        except Exception as e:
            print("Erro ao cadastrar livro:", e)
            messagebox.showerror("Erro", "Erro ao cadastrar livro.")

    janela_cadastrar = tk.Toplevel()
    janela_cadastrar.title("Cadastrar Livro")

    tk.Label(janela_cadastrar, text="Título:").grid(row=0, column=0, padx=10, pady=10)
    entry_titulo = tk.Entry(janela_cadastrar)
    entry_titulo.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(janela_cadastrar, text="Autor:").grid(row=1, column=0, padx=10, pady=10)
    entry_autor = tk.Entry(janela_cadastrar)
    entry_autor.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(janela_cadastrar, text="Ano:").grid(row=2, column=0, padx=10, pady=10)
    entry_ano = tk.Entry(janela_cadastrar)
    entry_ano.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(janela_cadastrar, text="Disponibilidade:").grid(row=3, column=0, padx=10, pady=10)
    var_disponibilidade = tk.StringVar(value="Sim")
    tk.Radiobutton(janela_cadastrar, text="Sim", variable=var_disponibilidade, value="Sim").grid(row=3, column=1, padx=10, pady=10)
    tk.Radiobutton(janela_cadastrar, text="Não", variable=var_disponibilidade, value="Não").grid(row=3, column=2, padx=10, pady=10)

    tk.Button(janela_cadastrar, text="Salvar", command=salvar).grid(row=4, column=0, columnspan=3, pady=10)

# Editar livro
def editar_livro():
    def carregar_dados():
        livro_id = entry_id.get()
        conn = conectar()
        if conn is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            return
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT titulo, autor, ano FROM Livro WHERE id = %s", (livro_id,))
            livro = cursor.fetchone()
            if livro:
                entry_titulo.insert(0, livro[0])
                entry_autor.insert(0, livro[1])
                entry_ano.insert(0, livro[2])
            else:
                messagebox.showerror("Erro", "Livro não encontrado.")
            conn.close()
        except Exception as e:
            print("Erro ao carregar dados:", e)
            messagebox.showerror("Erro", "Erro ao carregar dados do livro.")

    def salvar_edicao():
        livro_id = entry_id.get()
        titulo = entry_titulo.get()
        autor = entry_autor.get()
        ano = entry_ano.get()

        conn = conectar()
        if conn is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            return
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Livro SET titulo = %s, autor = %s, ano = %s WHERE id = %s",
                (titulo, autor, ano, livro_id)
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Livro atualizado com sucesso!")
            janela_editar.destroy()
        except Exception as e:
            print("Erro ao salvar edição:", e)
            messagebox.showerror("Erro", "Erro ao salvar edição do livro.")

    janela_editar = tk.Toplevel()
    janela_editar.title("Editar Livro")

    tk.Label(janela_editar, text="ID do Livro:").grid(row=0, column=0, padx=10, pady=10)
    entry_id = tk.Entry(janela_editar)
    entry_id.grid(row=0, column=1, padx=10, pady=10)

    tk.Button(janela_editar, text="Carregar Dados", command=carregar_dados).grid(row=0, column=2, padx=10, pady=10)

    tk.Label(janela_editar, text="Título:").grid(row=1, column=0, padx=10, pady=10)
    entry_titulo = tk.Entry(janela_editar)
    entry_titulo.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(janela_editar, text="Autor:").grid(row=2, column=0, padx=10, pady=10)
    entry_autor = tk.Entry(janela_editar)
    entry_autor.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(janela_editar, text="Ano:").grid(row=3, column=0, padx=10, pady=10)
    entry_ano = tk.Entry(janela_editar)
    entry_ano.grid(row=3, column=1, padx=10, pady=10)

    tk.Button(janela_editar, text="Salvar", command=salvar_edicao).grid(row=4, column=0, columnspan=3, pady=10)

# Excluir livro
def excluir_livro():
    def excluir():
        livro_id = entry_id.get()
        senha_admin = entry_senha.get()

        if not livro_id.isdigit():
            messagebox.showerror("Erro", "ID inválido.")
            return

        conn = conectar()
        if conn is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            return

        try:
            cursor = conn.cursor()

            # Verificar a senha do administrador no banco de dados
            cursor.execute("SELECT senha FROM Administradores LIMIT 1")
            resultado = cursor.fetchone()
            if resultado is None:
                messagebox.showerror("Erro", "Administrador não encontrado.")
                return

            senha_correta = resultado[0]

            if senha_admin != senha_correta:
                messagebox.showerror("Erro", "Senha de administrador incorreta.")
                return

            # Excluir registros relacionados na tabela Aluguel
            cursor.execute("DELETE FROM Aluguel WHERE livro_id = %s", (livro_id,))

            # Excluir o livro
            cursor.execute("DELETE FROM Livro WHERE id = %s", (livro_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Livro excluído com sucesso!")
            janela_excluir.destroy()
        except Exception as e:
            print("Erro ao excluir livro:", e)
            messagebox.showerror("Erro", "Erro ao excluir livro.")

    janela_excluir = tk.Toplevel()
    janela_excluir.title("Excluir Livro")

    tk.Label(janela_excluir, text="ID do Livro:").grid(row=0, column=0, padx=10, pady=10)
    entry_id = tk.Entry(janela_excluir)
    entry_id.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(janela_excluir, text="Senha de Administrador:").grid(row=1, column=0, padx=10, pady=10)
    entry_senha = tk.Entry(janela_excluir, show="*")
    entry_senha.grid(row=1, column=1, padx=10, pady=10)

    tk.Button(janela_excluir, text="Excluir", command=excluir).grid(row=2, column=0, columnspan=2, pady=10)

def alugar_livro():
    def alugar():
        livro_id = entry_id.get()
        usuario_id = entry_usuario_id.get()

        conn = conectar()
        if conn is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE Livro SET disponibilidade = %s WHERE id = %s AND disponibilidade = %s", (False, livro_id, True))
            if cursor.rowcount == 0:
                messagebox.showerror("Erro", "Livro não disponível para aluguel.")
                return
            cursor.execute("INSERT INTO Aluguel (livro_id, usuario_id, data_aluguel) VALUES (%s, %s, %s)", (livro_id, usuario_id, datetime.now()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Livro alugado com sucesso!")
            janela_alugar.destroy()
        except Exception as e:
            print("Erro ao alugar livro:", e)
            messagebox.showerror("Erro", "Erro ao alugar livro.")

    janela_alugar = tk.Toplevel()
    janela_alugar.title("Alugar Livro")

    tk.Label(janela_alugar, text="ID do Livro:").grid(row=0, column=0, padx=10, pady=10)
    entry_id = tk.Entry(janela_alugar)
    entry_id.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(janela_alugar, text="ID do Usuário:").grid(row=1, column=0, padx=10, pady=10)
    entry_usuario_id = tk.Entry(janela_alugar)
    entry_usuario_id.grid(row=1, column=1, padx=10, pady=10)

    tk.Button(janela_alugar, text="Alugar", command=alugar).grid(row=2, column=0, columnspan=2, pady=10)


def devolver_livro():
    def devolver():
        livro_id = entry_id.get()

        conn = conectar()
        if conn is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE Livro SET disponibilidade = %s WHERE id = %s AND disponibilidade = %s", (True, livro_id, False))
            if cursor.rowcount == 0:
                messagebox.showerror("Erro", "Livro não está alugado.")
                return
            cursor.execute("UPDATE Aluguel SET data_devolucao = %s WHERE livro_id = %s AND data_devolucao IS NULL", (datetime.now(), livro_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Livro devolvido com sucesso!")
            janela_devolver.destroy()
        except Exception as e:
            print("Erro ao devolver livro:", e)
            messagebox.showerror("Erro", "Erro ao devolver livro.")

    janela_devolver = tk.Toplevel()
    janela_devolver.title("Devolver Livro")

    tk.Label(janela_devolver, text="ID do Livro:").grid(row=0, column=0, padx=10, pady=10)
    entry_id = tk.Entry(janela_devolver)
    entry_id.grid(row=0, column=1, padx=10, pady=10)

    tk.Button(janela_devolver, text="Devolver", command=devolver).grid(row=1, column=0, columnspan=2, pady=10)

# Interface principal
app = tk.Tk()
app.title("Sistema de Biblioteca")

notebook = ttk.Notebook(app)
notebook.pack(expand=True, fill='both')

aba_usuarios = ttk.Frame(notebook)
aba_livros = ttk.Frame(notebook)
aba_aluguel = ttk.Frame(notebook)

notebook.add(aba_usuarios, text="Usuários")
notebook.add(aba_livros, text="Livros")
notebook.add(aba_aluguel, text="Aluguel")


btn_listar_usuarios = tk.Button(aba_usuarios, text="Listar Usuários", command=listar_usuarios)
btn_listar_usuarios.pack(pady=10)

btn_cadastrar_usuario = tk.Button(aba_usuarios, text="Cadastrar Usuário", command=cadastrar_usuario)
btn_cadastrar_usuario.pack(pady=10)

btn_editar_usuario = tk.Button(aba_usuarios, text="Editar Usuário", command=editar_usuario)
btn_editar_usuario.pack(pady=10)

btn_excluir_usuario = tk.Button(aba_usuarios, text="Excluir Usuário", command=excluir_usuario)
btn_excluir_usuario.pack(pady=10)


btn_listar_livros = tk.Button(aba_livros, text="Listar Livros", command=listar_livros)
btn_listar_livros.pack(pady=10)

btn_cadastrar_livro = tk.Button(aba_livros, text="Cadastrar Livro", command=cadastrar_livro)
btn_cadastrar_livro.pack(pady=10)

btn_editar_livro = tk.Button(aba_livros, text="Editar Livro", command=editar_livro)
btn_editar_livro.pack(pady=10)

btn_excluir_livro = tk.Button(aba_livros, text="Excluir Livro", command=excluir_livro)
btn_excluir_livro.pack(pady=10)

btn_alugar_livro = tk.Button(aba_aluguel, text="Alugar Livro", command=alugar_livro)
btn_alugar_livro.pack(pady=10)
btn_devolver_livro = tk.Button(aba_aluguel, text="Devolver Livro", command=devolver_livro)
btn_devolver_livro.pack(pady=10)

app.mainloop()
