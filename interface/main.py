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
            password="123456",
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
        cep = entry_cep.get()
        estado = entry_estado.get()
        cidade = entry_cidade.get()
        rua = entry_rua.get()
        numero = entry_numero.get()

        if not cpf or not nome or not sobrenome or not email or not cep or not estado or not cidade or not rua or not numero:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
            return

        conn = conectar()
        if conn is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            return

        try:
            cursor = conn.cursor()

            # Verificar se o endereço já existe
            cursor.execute("""
                SELECT ID_Endereco FROM Endereco
                WHERE CEP = %s AND Estado = %s AND Cidade = %s AND Rua = %s AND Numero = %s
            """, (cep, estado, cidade, rua, numero))
            endereco_existente = cursor.fetchone()

            if endereco_existente:
                id_endereco = endereco_existente[0]
            else:
                # Inserir novo endereço
                cursor.execute("""
                    INSERT INTO Endereco (CEP, Estado, Cidade, Rua, Numero)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING ID_Endereco
                """, (cep, estado, cidade, rua, numero))
                id_endereco = cursor.fetchone()[0]

            # Inserir novo usuário
            cursor.execute("""
                INSERT INTO Usuario (CPF, Nome, Sobrenome, Email, Telefone, ID_Endereco)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (cpf, nome, sobrenome, email, telefone, id_endereco))

            conn.commit()
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            janela_cadastrar.destroy()
        except Exception as e:
            print("Erro ao cadastrar usuário:", e)
            conn.rollback()
            messagebox.showerror("Erro", "Erro ao cadastrar usuário.")
        finally:
            cursor.close()
            conn.close()

    janela_cadastrar = tk.Toplevel()
    janela_cadastrar.title("Cadastrar Usuário")

    tk.Label(janela_cadastrar, text="CPF:").grid(row=0, column=0, padx=10, pady=5)
    entry_cpf = tk.Entry(janela_cadastrar)
    entry_cpf.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(janela_cadastrar, text="Nome:").grid(row=1, column=0, padx=10, pady=5)
    entry_nome = tk.Entry(janela_cadastrar)
    entry_nome.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(janela_cadastrar, text="Sobrenome:").grid(row=2, column=0, padx=10, pady=5)
    entry_sobrenome = tk.Entry(janela_cadastrar)
    entry_sobrenome.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(janela_cadastrar, text="Email:").grid(row=3, column=0, padx=10, pady=5)
    entry_email = tk.Entry(janela_cadastrar)
    entry_email.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(janela_cadastrar, text="Telefone:").grid(row=4, column=0, padx=10, pady=5)
    entry_telefone = tk.Entry(janela_cadastrar)
    entry_telefone.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(janela_cadastrar, text="CEP:").grid(row=5, column=0, padx=10, pady=5)
    entry_cep = tk.Entry(janela_cadastrar)
    entry_cep.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(janela_cadastrar, text="Estado:").grid(row=6, column=0, padx=10, pady=5)
    entry_estado = tk.Entry(janela_cadastrar)
    entry_estado.grid(row=6, column=1, padx=10, pady=5)

    tk.Label(janela_cadastrar, text="Cidade:").grid(row=7, column=0, padx=10, pady=5)
    entry_cidade = tk.Entry(janela_cadastrar)
    entry_cidade.grid(row=7, column=1, padx=10, pady=5)

    tk.Label(janela_cadastrar, text="Rua:").grid(row=8, column=0, padx=10, pady=5)
    entry_rua = tk.Entry(janela_cadastrar)
    entry_rua.grid(row=8, column=1, padx=10, pady=5)

    tk.Label(janela_cadastrar, text="Número:").grid(row=9, column=0, padx=10, pady=5)
    entry_numero = tk.Entry(janela_cadastrar)
    entry_numero.grid(row=9, column=1, padx=10, pady=5)

    tk.Button(janela_cadastrar, text="Salvar", command=salvar).grid(row=10, column=0, columnspan=2, pady=10)

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
        senha_banco = entry_senha.get()

        if not cpf or not senha_banco:
            messagebox.showerror("Erro", "CPF do usuário e senha do banco de dados são obrigatórios.")
            return

        # Tentar conexão com a senha fornecida
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="biblioteca",
                user="postgres",
                password="123456",
                client_encoding="utf-8"  
            )
        except Exception as e:
            print("Erro ao conectar ao banco de dados:", e)
            messagebox.showerror("Erro", "Senha do banco de dados incorreta ou falha na conexão.")
            return

        try:
            cursor = conn.cursor()

            # Verificar se o CPF existe no banco de dados
            cursor.execute("SELECT CPF FROM Usuario WHERE CPF = %s", (cpf,))
            if cursor.fetchone() is None:
                messagebox.showerror("Erro", "Usuário não encontrado com o CPF informado.")
                return

            # Excluir registros relacionados na tabela Aluguel
            cursor.execute("DELETE FROM Aluguel WHERE CPF = %s", (cpf,))

            # Excluir o usuário
            cursor.execute("DELETE FROM Usuario WHERE CPF = %s", (cpf,))
            conn.commit()
            messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
            janela_excluir.destroy()
        except Exception as e:
            print("Erro ao excluir usuário:", e)
            conn.rollback()
            messagebox.showerror("Erro", "Erro ao excluir usuário. Verifique se há dependências.")
        finally:
            cursor.close()
            conn.close()

    janela_excluir = tk.Toplevel()
    janela_excluir.title("Excluir Usuário")

    tk.Label(janela_excluir, text="CPF do Usuário:").grid(row=0, column=0, padx=10, pady=10)
    entry_cpf = tk.Entry(janela_excluir)
    entry_cpf.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(janela_excluir, text="Senha do Banco de Dados:").grid(row=1, column=0, padx=10, pady=10)
    entry_senha = tk.Entry(janela_excluir, show="*")
    entry_senha.grid(row=1, column=1, padx=10, pady=10)

    tk.Button(janela_excluir, text="Excluir", command=excluir).grid(row=2, column=0, columnspan=2, pady=10)

# Funções para Livros

def listar_livros():
    def carregar_livros(filtro=None):
        # Conectar ao banco de dados
        conn = conectar()
        if conn is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            return

        try:
            cursor = conn.cursor()

            # Consulta SQL para listar os livros com filtro opcional, combinando as tabelas Livro e Titulo
            if filtro:
                query = """
                SELECT l.ISBN, l.Edicao, l.Qntd_total, l.Qntd_disponivel, t.Titulo, t.Autor
                FROM Livro l
                INNER JOIN Titulo t ON l.ID_titulo = t.ID_titulo
                WHERE LOWER(l.ISBN) LIKE %s OR LOWER(t.Titulo) LIKE %s OR LOWER(t.Autor) LIKE %s
                """
                cursor.execute(query, (f"%{filtro.lower()}%", f"%{filtro.lower()}%", f"%{filtro.lower()}%"))
            else:
                query = """
                SELECT l.ISBN, l.Edicao, l.Qntd_total, l.Qntd_disponivel, t.Titulo, t.Autor
                FROM Livro l
                INNER JOIN Titulo t ON l.ID_titulo = t.ID_titulo
                """
                cursor.execute(query)

            # Limpar a Treeview antes de carregar novos dados
            for item in tree.get_children():
                tree.delete(item)

            # Inserir os dados na Treeview
            for row in cursor.fetchall():
                tree.insert("", tk.END, values=row)

        except Exception as e:
            print("Erro ao listar livros:", e)
            messagebox.showerror("Erro", "Erro ao listar livros.")
        finally:
            cursor.close()
            conn.close()

    def buscar_livros():
        filtro = entry_busca.get()
        carregar_livros(filtro)

    # Criar janela de listagem
    janela_listar = tk.Toplevel()
    janela_listar.title("Listagem de Livros")
    janela_listar.geometry("800x400")

    # Campo de busca
    tk.Label(janela_listar, text="Buscar (ISBN, Título ou Autor):").pack(pady=5)
    entry_busca = tk.Entry(janela_listar)
    entry_busca.pack(pady=5)

    tk.Button(janela_listar, text="Buscar", command=buscar_livros).pack(pady=5)

    # Configurar Treeview para exibir os dados
    tree = ttk.Treeview(janela_listar, columns=("ISBN", "Edição", "Quantidade Total", "Quantidade Disponível", "Título", "Autor"), show="headings")
    tree.heading("ISBN", text="ISBN")
    tree.heading("Edição", text="Edição")
    tree.heading("Quantidade Total", text="Quantidade Total")
    tree.heading("Quantidade Disponível", text="Quantidade Disponível")
    tree.heading("Título", text="Título")
    tree.heading("Autor", text="Autor")
    tree.pack(fill=tk.BOTH, expand=True)

    # Ajustar o tamanho das colunas para uma melhor visualização
    tree.column("ISBN", width=120)
    tree.column("Edição", width=100)
    tree.column("Quantidade Total", width=140)
    tree.column("Quantidade Disponível", width=140)
    tree.column("Título", width=200)
    tree.column("Autor", width=150)

    # Carregar todos os livros ao abrir
    carregar_livros()


def cadastrar_livro():
    def salvar():
        isbn = entry_isbn.get()
        edicao = entry_edicao.get()
        qntd_total = entry_qntd_total.get()
        qntd_disponivel = entry_qntd_disponivel.get()
        titulo = entry_titulo.get()
        autor = entry_autor.get()
        editora = entry_editora.get()
        ano = entry_ano.get()

        if not isbn or not edicao or not qntd_total or not qntd_disponivel or not titulo or not autor or not editora or not ano:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
            return

        conn = conectar()
        if conn is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            return

        try:
            cursor = conn.cursor()

            # Verificar se o título já existe
            cursor.execute("SELECT ID_titulo FROM Titulo WHERE Titulo = %s AND Autor = %s", (titulo, autor))
            resultado = cursor.fetchone()

            if resultado:
                id_titulo = resultado[0]
            else:
                # Inserir novo título na tabela Titulo
                cursor.execute(
                    "INSERT INTO Titulo (Titulo, Autor, Editora, Ano) VALUES (%s, %s, %s, %s) RETURNING ID_titulo",
                    (titulo, autor, editora, ano)
                )
                id_titulo = cursor.fetchone()[0]

            # Inserir o livro com o ID_titulo correspondente
            cursor.execute(
                "INSERT INTO Livro (ISBN, Edicao, Qntd_total, Qntd_disponivel, ID_titulo) VALUES (%s, %s, %s, %s, %s)",
                (isbn, edicao, int(qntd_total), int(qntd_disponivel), id_titulo)
            )
            conn.commit()
            messagebox.showinfo("Sucesso", f"Livro cadastrado com sucesso! ID do Título: {id_titulo}")
            janela_cadastrar.destroy()
        except Exception as e:
            print("Erro ao cadastrar livro:", e)
            messagebox.showerror("Erro", f"Erro ao cadastrar livro: {e}")
        finally:
            cursor.close()
            conn.close()

    # Janela de cadastro
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

    tk.Label(janela_cadastrar, text="Título:").grid(row=4, column=0, padx=10, pady=10)
    entry_titulo = tk.Entry(janela_cadastrar)
    entry_titulo.grid(row=4, column=1, padx=10, pady=10)

    tk.Label(janela_cadastrar, text="Autor:").grid(row=5, column=0, padx=10, pady=10)
    entry_autor = tk.Entry(janela_cadastrar)
    entry_autor.grid(row=5, column=1, padx=10, pady=10)

    tk.Label(janela_cadastrar, text="Editora:").grid(row=6, column=0, padx=10, pady=10)
    entry_editora = tk.Entry(janela_cadastrar)
    entry_editora.grid(row=6, column=1, padx=10, pady=10)

    tk.Label(janela_cadastrar, text="Ano:").grid(row=7, column=0, padx=10, pady=10)
    entry_ano = tk.Entry(janela_cadastrar)
    entry_ano.grid(row=7, column=1, padx=10, pady=10)

    tk.Button(janela_cadastrar, text="Salvar", command=salvar).grid(row=8, column=0, columnspan=2, pady=10)


def editar_livro():
    def carregar_dados():
        isbn = entry_isbn.get()
        conn = conectar()
        if conn is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT l.Edicao, l.Qntd_total, l.Qntd_disponivel, t.Titulo, t.Autor, t.Editora, t.Ano, l.ID_titulo
                FROM Livro l
                JOIN Titulo t ON l.ID_titulo = t.ID_titulo
                WHERE l.ISBN = %s
            """, (isbn,))
            livro = cursor.fetchone()
            if livro:
                entry_edicao.insert(0, livro[0])
                entry_qntd_total.insert(0, livro[1])
                entry_qntd_disponivel.insert(0, livro[2])
                entry_titulo.insert(0, livro[3])
                entry_autor.insert(0, livro[4])
                entry_editora.insert(0, livro[5])
                entry_ano.insert(0, livro[6])
                label_id_titulo['text'] = livro[7]
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
        titulo = entry_titulo.get()
        autor = entry_autor.get()
        editora = entry_editora.get()
        ano = entry_ano.get()
        id_titulo = label_id_titulo['text']  # Mantém o ID do título inalterado

        conn = conectar()
        if conn is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            return
        try:
            cursor = conn.cursor()
            # Atualizar os dados na tabela Livro
            cursor.execute("""
                UPDATE Livro
                SET Edicao = %s, Qntd_total = %s, Qntd_disponivel = %s
                WHERE ISBN = %s
            """, (edicao, qntd_total, qntd_disponivel, isbn))

            # Atualizar os dados na tabela Titulo
            cursor.execute("""
                UPDATE Titulo
                SET Titulo = %s, Autor = %s, Editora = %s, Ano = %s
                WHERE ID_titulo = %s
            """, (titulo, autor, editora, ano, id_titulo))

            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Livro e título atualizados com sucesso!")
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

    tk.Label(janela_editar, text="Título:").grid(row=4, column=0, padx=10, pady=10)
    entry_titulo = tk.Entry(janela_editar)
    entry_titulo.grid(row=4, column=1, padx=10, pady=10)

    tk.Label(janela_editar, text="Autor:").grid(row=5, column=0, padx=10, pady=10)
    entry_autor = tk.Entry(janela_editar)
    entry_autor.grid(row=5, column=1, padx=10, pady=10)

    tk.Label(janela_editar, text="Editora:").grid(row=6, column=0, padx=10, pady=10)
    entry_editora = tk.Entry(janela_editar)
    entry_editora.grid(row=6, column=1, padx=10, pady=10)

    tk.Label(janela_editar, text="Ano:").grid(row=7, column=0, padx=10, pady=10)
    entry_ano = tk.Entry(janela_editar)
    entry_ano.grid(row=7, column=1, padx=10, pady=10)

    tk.Label(janela_editar, text="ID do Título:").grid(row=8, column=0, padx=10, pady=10)
    label_id_titulo = tk.Label(janela_editar, text="")
    label_id_titulo.grid(row=8, column=1, padx=10, pady=10)

    tk.Button(janela_editar, text="Salvar Edição", command=salvar_edicao).grid(row=9, column=0, columnspan=2, pady=10)


def excluir_livro():
    def excluir():
        isbn = entry_isbn.get()
        senha_banco = entry_senha.get()

        if not isbn:
            messagebox.showerror("Erro", "ISBN é obrigatório.")
            return

        if not senha_banco:
            messagebox.showerror("Erro", "Senha do banco é obrigatória.")
            return

        # Conectar ao banco com a senha fornecida
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="biblioteca",
                user="postgres",
                password="123456",
                client_encoding="utf-8" 
            )
            conn.set_client_encoding('UTF8')
        except Exception as e:
            print("Erro na conexão:", e)
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados. Verifique a senha.")
            return

        try:
            cursor = conn.cursor()

            # Obter o ID do título relacionado ao ISBN
            cursor.execute("SELECT ID_titulo FROM Livro WHERE ISBN = %s", (isbn,))
            titulo_relacionado = cursor.fetchone()

            if titulo_relacionado is None:
                messagebox.showerror("Erro", "Livro não encontrado.")
                return

            id_titulo = titulo_relacionado[0]

            # Excluir registros relacionados na tabela Aluguel
            cursor.execute("DELETE FROM Aluguel WHERE ISBN = %s", (isbn,))

            # Excluir o livro
            cursor.execute("DELETE FROM Livro WHERE ISBN = %s", (isbn,))

            # Verificar se ainda existem outros livros relacionados ao título
            cursor.execute("SELECT COUNT(*) FROM Livro WHERE ID_titulo = %s", (id_titulo,))
            livros_restantes = cursor.fetchone()[0]

            if livros_restantes == 0:
                # Excluir o título se nenhum livro estiver associado a ele
                cursor.execute("DELETE FROM Titulo WHERE ID_titulo = %s", (id_titulo,))

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

    tk.Label(janela_excluir, text="Senha do Banco de Dados:").grid(row=1, column=0, padx=10, pady=10)
    entry_senha = tk.Entry(janela_excluir, show="*")
    entry_senha.grid(row=1, column=1, padx=10, pady=10)

    tk.Button(janela_excluir, text="Excluir", command=excluir).grid(row=2, column=0, columnspan=2, pady=10)


def alugar_livro():
    def alugar():
        isbn = entry_isbn.get()
        cpf = entry_cpf.get()

        if not isbn or not cpf:
            messagebox.showerror("Erro", "ISBN e CPF são obrigatórios.")
            return

        conn = conectar()
        if conn is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            return

        try:
            cursor = conn.cursor()

            # Verificar se o livro está disponível
            cursor.execute("SELECT Qntd_disponivel FROM Livro WHERE ISBN = %s", (isbn,))
            resultado = cursor.fetchone()

            if not resultado:
                messagebox.showerror("Erro", "Livro não encontrado.")
                return

            qntd_disponivel = resultado[0]

            if qntd_disponivel <= 0:
                messagebox.showerror("Erro", "Livro não disponível para aluguel.")
                return

            # Subtrair uma unidade da quantidade disponível
            cursor.execute(
                "UPDATE Livro SET Qntd_disponivel = Qntd_disponivel - 1 WHERE ISBN = %s",
                (isbn,)
            )

            # Registrar o aluguel
            data_aluguel = datetime.now().strftime('%Y-%m-%d')
            cursor.execute(
                "INSERT INTO Aluguel (Data_aluguel, CPF, ISBN) VALUES (%s, %s, %s)",
                (data_aluguel, cpf, isbn)
            )

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
