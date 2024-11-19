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

# Funções para Usuários

def listar_usuarios():
    janela_listar = tk.Toplevel()
    janela_listar.title("Listagem de Usuários")
    
    tree = ttk.Treeview(janela_listar, columns=("CPF", "Nome", "Sobrenome", "Email", "Telefone"), show="headings")
    tree.heading("CPF", text="CPF")
    tree.heading("Nome", text="Nome")
    tree.heading("Sobrenome", text="Sobrenome")
    tree.heading("Email", text="Email")
    tree.heading("Telefone", text="Telefone")
    tree.pack(fill=tk.BOTH, expand=True)

    conn = conectar()
    if conn is None:
        messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT CPF, Nome, Sobrenome, Email, Telefone FROM Usuario")
        usuarios = cursor.fetchall()
        for usuario in usuarios:
            tree.insert("", tk.END, values=usuario)
        conn.close()
    except Exception as e:
        print("Erro ao listar usuários:", e)
        messagebox.showerror("Erro", "Erro ao listar usuários.")

def cadastrar_usuario():
    def salvar():
        cpf = entry_cpf.get()
        nome = entry_nome.get()
        sobrenome = entry_sobrenome.get()
        email = entry_email.get()
        telefone = entry_telefone.get()
        endereco_id = entry_endereco_id.get()

        if not cpf or not nome or not sobrenome or not email:
            messagebox.showerror("Erro", "CPF, Nome, Sobrenome e E-mail são obrigatórios.")
            return

        conn = conectar()
        if conn is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Usuario (CPF, Nome, Sobrenome, Email, Telefone, ID_Endereco) VALUES (%s, %s, %s, %s, %s, %s)",
                (cpf, nome, sobrenome, email, telefone, endereco_id)
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

    tk.Label(janela_cadastrar, text="CPF:").grid(row=0, column=0, padx=10, pady=10)
    entry_cpf = tk.Entry(janela_cadastrar)
    entry_cpf.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(janela_cadastrar, text="Nome:").grid(row=1, column=0, padx=10, pady=10)
    entry_nome = tk.Entry(janela_cadastrar)
    entry_nome.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(janela_cadastrar, text="Sobrenome:").grid(row=2, column=0, padx=10, pady=10)
    entry_sobrenome = tk.Entry(janela_cadastrar)
    entry_sobrenome.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(janela_cadastrar, text="Email:").grid(row=3, column=0, padx=10, pady=10)
    entry_email = tk.Entry(janela_cadastrar)
    entry_email.grid(row=3, column=1, padx=10, pady=10)

    tk.Label(janela_cadastrar, text="Telefone:").grid(row=4, column=0, padx=10, pady=10)
    entry_telefone = tk.Entry(janela_cadastrar)
    entry_telefone.grid(row=4, column=1, padx=10, pady=10)

    tk.Label(janela_cadastrar, text="ID do Endereço:").grid(row=5, column=0, padx=10, pady=10)
    entry_endereco_id = tk.Entry(janela_cadastrar)
    entry_endereco_id.grid(row=5, column=1, padx=10, pady=10)

    tk.Button(janela_cadastrar, text="Salvar", command=salvar).grid(row=6, column=0, columnspan=2, pady=10)

def editar_usuario():
    def carregar_dados():
        cpf = entry_cpf.get()
        conn = conectar()
        if conn is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            return
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT Nome, Sobrenome, Email, Telefone FROM Usuario WHERE CPF = %s", (cpf,))
            usuario = cursor.fetchone()
            if usuario:
                entry_nome.insert(0, usuario[0])
                entry_sobrenome.insert(0, usuario[1])
                entry_email.insert(0, usuario[2])
                entry_telefone.insert(0, usuario[3])
            else:
                messagebox.showerror("Erro", "Usuário não encontrado.")
            conn.close()
        except Exception as e:
            print("Erro ao carregar dados:", e)
            messagebox.showerror("Erro", "Erro ao carregar dados do usuário.")

    def salvar_edicao():
        cpf = entry_cpf.get()
        nome = entry_nome.get()
        sobrenome = entry_sobrenome.get()
        email = entry_email.get()
        telefone = entry_telefone.get()

        conn = conectar()
        if conn is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            return
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Usuario SET Nome = %s, Sobrenome = %s, Email = %s, Telefone = %s WHERE CPF = %s",
                (nome, sobrenome, email, telefone, cpf)
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

    tk.Label(janela_editar, text="CPF do Usuário:").grid(row=0, column=0, padx=10, pady=10)
    entry_cpf = tk.Entry(janela_editar)
    entry_cpf.grid(row=0, column=1, padx=10, pady=10)
    tk.Button(janela_editar, text="Carregar Dados", command=carregar_dados).grid(row=0, column=2, padx=10, pady=10)

    tk.Label(janela_editar, text="Nome:").grid(row=1, column=0, padx=10, pady=10)
    entry_nome = tk.Entry(janela_editar)
    entry_nome.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(janela_editar, text="Sobrenome:").grid(row=2, column=0, padx=10, pady=10)
    entry_sobrenome = tk.Entry(janela_editar)
    entry_sobrenome.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(janela_editar, text="Email:").grid(row=3, column=0, padx=10, pady=10)
    entry_email = tk.Entry(janela_editar)
    entry_email.grid(row=3, column=1, padx=10, pady=10)

    tk.Label(janela_editar, text="Telefone:").grid(row=4, column=0, padx=10, pady=10)
    entry_telefone = tk.Entry(janela_editar)
    entry_telefone.grid(row=4, column=1, padx=10, pady=10)

    tk.Button(janela_editar, text="Salvar Edição", command=salvar_edicao).grid(row=5, column=0, columnspan=2, pady=10)

def excluir_usuario():
    def excluir():
        cpf = entry_cpf.get()
        senha_admin = entry_senha.get()

        if not cpf:
            messagebox.showerror("Erro", "CPF é obrigatório.")
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
            cursor.execute("DELETE FROM Aluguel WHERE usuario_id = %s", (cpf,))

            # Excluir o usuário
            cursor.execute("DELETE FROM Usuario WHERE CPF = %s", (cpf,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
            janela_excluir.destroy()
        except Exception as e:
            print("Erro ao excluir usuário:", e)
            messagebox.showerror("Erro", "Erro ao excluir usuário.")

    janela_excluir = tk.Toplevel()
    janela_excluir.title("Excluir Usuário")

    tk.Label(janela_excluir, text="CPF do Usuário:").grid(row=0, column=0, padx=10, pady=10)
    entry_cpf = tk.Entry(janela_excluir)
    entry_cpf.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(janela_excluir, text="Senha de Administrador:").grid(row=1, column=0, padx=10, pady=10)
    entry_senha = tk.Entry(janela_excluir, show="*")
    entry_senha.grid(row=1, column=1, padx=10, pady=10)

    tk.Button(janela_excluir, text="Excluir", command=excluir).grid(row=2, column=0, columnspan=2, pady=10)

# Funções para Livros

def listar_livros():
    janela_listar = tk.Toplevel()
    janela_listar.title("Listagem de Livros")

    tk.Label(janela_listar, text="Buscar:").pack(pady=5)
    entry_busca = tk.Entry(janela_listar)
    entry_busca.pack(pady=5)

    tree = ttk.Treeview(janela_listar, columns=("ISBN", "Edição", "Quantidade Total", "Quantidade Disponível", "ID Título"), show="headings")
    tree.heading("ISBN", text="ISBN")
    tree.heading("Edição", text="Edição")
    tree.heading("Quantidade Total", text="Quantidade Total")
    tree.heading("Quantidade Disponível", text="Quantidade Disponível")
    tree.heading("ID Título", text="ID Título")
    tree.pack(fill=tk.BOTH, expand=True)

    def atualizar_lista(*args):
        termo = entry_busca.get()
        conn = conectar()
        if conn is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            return
        try:
            cursor = conn.cursor()
            consulta = "SELECT ISBN, Edição, Qntd_total, Qntd_disponivel, ID_titulo FROM Livro WHERE ISBN ILIKE %s OR Edição ILIKE %s"
            cursor.execute(consulta, ('%' + termo + '%', '%' + termo + '%'))
            livros = cursor.fetchall()
            tree.delete(*tree.get_children())
            for livro in livros:
                tree.insert("", tk.END, values=livro)
            conn.close()
        except Exception as e:
            print("Erro ao listar livros:", e)
            messagebox.showerror("Erro", "Erro ao listar livros.")

    entry_busca.bind("<KeyRelease>", atualizar_lista)

    atualizar_lista()

def cadastrar_livro():
    def salvar():
        isbn = entry_isbn.get()
        edicao = entry_edicao.get()
        qntd_total = entry_qntd_total.get()
        qntd_disponivel = entry_qntd_disponivel.get()
        id_titulo = entry_id_titulo.get()

        if not isbn or not edicao or not qntd_total or not qntd_disponivel or not id_titulo:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
            return

        conn = conectar()
        if conn is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Livro (ISBN, Edição, Qntd_total, Qntd_disponivel, ID_titulo) VALUES (%s, %s, %s, %s, %s)",
                (isbn, edicao, qntd_total, qntd_disponivel, id_titulo)
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

    tk.Label(janela_cadastrar, text="ISBN:").grid(row=0, column=0, padx=10, pady=10)
    entry_isbn = tk.Entry(janela_cadastrar)
    entry_isbn.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(janela_cadastrar, text="Edição:").grid(row=1, column=0, padx=10, pady=10)
    entry_edicao = tk.Entry(janela_cadastrar)
    entry_edicao.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(janela_cadastrar, text="Quantidade Total:").grid(row=2, column=0, padx=10, pady=10)
    entry_qntd_total = tk.Entry(janela_cadastrar)
    entry_qntd_total.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(janela_cadastrar, text="Quantidade Disponível:").grid(row=3, column=0, padx=10, pady=10)
    entry_qntd_disponivel = tk.Entry(janela_cadastrar)
    entry_qntd_disponivel.grid(row=3, column=1, padx=10, pady=10)

    tk.Label(janela_cadastrar, text="ID do Título:").grid(row=4, column=0, padx=10, pady=10)
    entry_id_titulo = tk.Entry(janela_cadastrar)
    entry_id_titulo.grid(row=4, column=1, padx=10, pady=10)

    tk.Button(janela_cadastrar, text="Salvar", command=salvar).grid(row=5, column=0, columnspan=2, pady=10)

def editar_livro():
    def carregar_dados():
        isbn = entry_isbn.get()
        conn = conectar()
        if conn is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            return
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT Edição, Qntd_total, Qntd_disponivel, ID_titulo FROM Livro WHERE ISBN = %s", (isbn,))
            livro = cursor.fetchone()
            if livro:
                entry_edicao.insert(0, livro[0])
                entry_qntd_total.insert(0, livro[1])
                entry_qntd_disponivel.insert(0, livro[2])
                entry_id_titulo.insert(0, livro[3])
            else:
                messagebox.showerror("Erro", "Livro não encontrado.")
            conn.close()
        except Exception as e:
            print("Erro ao carregar dados:", e)
            messagebox.showerror("Erro", "Erro ao carregar dados do livro.")

    def salvar_edicao():
        isbn = entry_isbn.get()
        edicao = entry_edicao.get()
        qntd_total = entry_qntd_total.get()
        qntd_disponivel = entry_qntd_disponivel.get()
        id_titulo = entry_id_titulo.get()

        conn = conectar()
        if conn is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            return
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Livro SET Edição = %s, Qntd_total = %s, Qntd_disponivel = %s, ID_titulo = %s WHERE ISBN = %s",
                (edicao, qntd_total, qntd_disponivel, id_titulo, isbn)
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

    tk.Label(janela_editar, text="ISBN do Livro:").grid(row=0, column=0, padx=10, pady=10)
    entry_isbn = tk.Entry(janela_editar)
    entry_isbn.grid(row=0, column=1, padx=10, pady=10)
    tk.Button(janela_editar, text="Carregar Dados", command=carregar_dados).grid(row=0, column=2, padx=10, pady=10)

    tk.Label(janela_editar, text="Edição:").grid(row=1, column=0, padx=10, pady=10)
    entry_edicao = tk.Entry(janela_editar)
    entry_edicao.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(janela_editar, text="Quantidade Total:").grid(row=2, column=0, padx=10, pady=10)
    entry_qntd_total = tk.Entry(janela_editar)
    entry_qntd_total.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(janela_editar, text="Quantidade Disponível:").grid(row=3, column=0, padx=10, pady=10)
    entry_qntd_disponivel = tk.Entry(janela_editar)
    entry_qntd_disponivel.grid(row=3, column=1, padx=10, pady=10)

    tk.Label(janela_editar, text="ID do Título:").grid(row=4, column=0, padx=10, pady=10)
    entry_id_titulo = tk.Entry(janela_editar)
    entry_id_titulo.grid(row=4, column=1, padx=10, pady=10)

    tk.Button(janela_editar, text="Salvar Edição", command=salvar_edicao).grid(row=5, column=0, columnspan=2, pady=10)

def excluir_livro():
    def excluir():
        isbn = entry_isbn.get()
        senha_admin = entry_senha.get()

        if not isbn:
            messagebox.showerror("Erro", "ISBN é obrigatório.")
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
            cursor.execute("DELETE FROM Aluguel WHERE livro_id = %s", (isbn,))

            # Excluir o livro
            cursor.execute("DELETE FROM Livro WHERE ISBN = %s", (isbn,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Livro excluído com sucesso!")
            janela_excluir.destroy()
        except Exception as e:
            print("Erro ao excluir livro:", e)
            messagebox.showerror("Erro", "Erro ao excluir livro.")

    janela_excluir = tk.Toplevel()
    janela_excluir.title("Excluir Livro")

    tk.Label(janela_excluir, text="ISBN do Livro:").grid(row=0, column=0, padx=10, pady=10)
    entry_isbn = tk.Entry(janela_excluir)
    entry_isbn.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(janela_excluir, text="Senha de Administrador:").grid(row=1, column=0, padx=10, pady=10)
    entry_senha = tk.Entry(janela_excluir, show="*")
    entry_senha.grid(row=1, column=1, padx=10, pady=10)

    tk.Button(janela_excluir, text="Excluir", command=excluir).grid(row=2, column=0, columnspan=2, pady=10)

def alugar_livro():
    def alugar():
        isbn = entry_isbn.get()
        cpf = entry_cpf.get()

        conn = conectar()
        if conn is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE Livro SET Qntd_disponivel = Qntd_disponivel - 1 WHERE ISBN = %s AND Qntd_disponivel > 0", (isbn,))
            if cursor.rowcount == 0:
                messagebox.showerror("Erro", "Livro não disponível para aluguel.")
                return
            cursor.execute("INSERT INTO Aluguel (Data_aluguel, CPF, ISBN) VALUES (%s, %s, %s)", (datetime.now(), cpf, isbn))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Livro alugado com sucesso!")
            janela_alugar.destroy()
        except Exception as e:
            print("Erro ao alugar livro:", e)
            messagebox.showerror("Erro", "Erro ao alugar livro.")

    janela_alugar = tk.Toplevel()
    janela_alugar.title("Alugar Livro")

    tk.Label(janela_alugar, text="ISBN do Livro:").grid(row=0, column=0, padx=10, pady=10)
    entry_isbn = tk.Entry(janela_alugar)
    entry_isbn.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(janela_alugar, text="CPF do Usuário:").grid(row=1, column=0, padx=10, pady=10)
    entry_cpf = tk.Entry(janela_alugar)
    entry_cpf.grid(row=1, column=1, padx=10, pady=10)

    tk.Button(janela_alugar, text="Alugar", command=alugar).grid(row=2, column=0, columnspan=2, pady=10)

def devolver_livro():
    def devolver():
        isbn = entry_isbn.get()

        conn = conectar()
        if conn is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE Livro SET Qntd_disponivel = Qntd_disponivel + 1 WHERE ISBN = %s AND Qntd_disponivel < Qntd_total", (isbn,))
            if cursor.rowcount == 0:
                messagebox.showerror("Erro", "Livro não está alugado.")
                return
            cursor.execute("UPDATE Aluguel SET Data_devolucao = %s WHERE ISBN = %s AND Data_devolucao IS NULL", (datetime.now(), isbn))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Livro devolvido com sucesso!")
            janela_devolver.destroy()
        except Exception as e:
            print("Erro ao devolver livro:", e)
            messagebox.showerror("Erro", "Erro ao devolver livro.")

    janela_devolver = tk.Toplevel()
    janela_devolver.title("Devolver Livro")

    tk.Label(janela_devolver, text="ISBN do Livro:").grid(row=0, column=0, padx=10, pady=10)
    entry_isbn = tk.Entry(janela_devolver)
    entry_isbn.grid(row=0, column=1, padx=10, pady=10)

    tk.Button(janela_devolver, text="Devolver", command=devolver).grid(row=1, column=0, columnspan=2, pady=10)

# Interface Principal
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

# Botões para Usuários
btn_listar_usuarios = tk.Button(aba_usuarios, text="Listar Usuários", command=listar_usuarios)
btn_listar_usuarios.pack(pady=10)

btn_cadastrar_usuario = tk.Button(aba_usuarios, text="Cadastrar Usuário", command=cadastrar_usuario)
btn_cadastrar_usuario.pack(pady=10)

btn_editar_usuario = tk.Button(aba_usuarios, text="Editar Usuário", command=editar_usuario)
btn_editar_usuario.pack(pady=10)

btn_excluir_usuario = tk.Button(aba_usuarios, text="Excluir Usuário", command=excluir_usuario)
btn_excluir_usuario.pack(pady=10)

# Botões para Livros
btn_listar_livros = tk.Button(aba_livros, text="Listar Livros", command=listar_livros)
btn_listar_livros.pack(pady=10)

btn_cadastrar_livro = tk.Button(aba_livros, text="Cadastrar Livro", command=cadastrar_livro)
btn_cadastrar_livro.pack(pady=10)

btn_editar_livro = tk.Button(aba_livros, text="Editar Livro", command=editar_livro)
btn_editar_livro.pack(pady=10)

btn_excluir_livro = tk.Button(aba_livros, text="Excluir Livro", command=excluir_livro)
btn_excluir_livro.pack(pady=10)

# Botões para Aluguel
btn_alugar_livro = tk.Button(aba_aluguel, text="Alugar Livro", command=alugar_livro)
btn_alugar_livro.pack(pady=10)

btn_devolver_livro = tk.Button(aba_aluguel, text="Devolver Livro", command=devolver_livro)
btn_devolver_livro.pack(pady=10)

app.mainloop()