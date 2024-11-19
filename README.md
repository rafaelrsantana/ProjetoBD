
# Sistema de Gerenciamento de Biblioteca

Este projeto consiste no desenvolvimento de um sistema para gerenciamento de bibliotecas. Ele foi desenvolvido como parte da disciplina de Banco de Dados do curso de Engenharia de Computação na Universidade Federal de Alagoas (UFAL). O sistema permite a administração de usuários, livros e o controle de aluguéis, utilizando modelagem e normalização de banco de dados.

## Funcionalidades

- **Gerenciamento de Usuários:** Cadastro, edição, exclusão e listagem de usuários.
- **Gerenciamento de Livros:** Cadastro, edição, exclusão e listagem de livros.
- **Controle de Aluguéis:** Registro de empréstimos e devoluções de livros.
  
## Tecnologias Utilizadas

- **Banco de Dados:** PostgreSQL, com a modelagem normalizada até a Terceira Forma Normal (3FN).
- **Interface do Sistema:** Desenvolvida em Python.
- **Interação com o Banco de Dados:** Biblioteca `psycopg2` para conexão e execução de operações no PostgreSQL.

## Como Executar

1. Certifique-se de ter o PostgreSQL instalado e configurado.
2. Crie o banco de dados com os arquivos da pasta Scripts.
3. Instale as dependências do Python utilizando `pip install psycopg2`.
4. Execute o script Python para interagir com o sistema.

## Prints
Tela inicial:
![Screenshot 2024-11-19 142939](https://github.com/user-attachments/assets/0f9e1a38-03c1-439f-8781-b3fd10eb5043)

Listar Usuários:
![Screenshot 2024-11-19 143021](https://github.com/user-attachments/assets/006eaf2d-a029-42c0-ba8b-367d69d56d8c)

Cadastrar Usuário:
![Screenshot 2024-11-19 143409](https://github.com/user-attachments/assets/4b29c1fa-0df0-4f4a-a674-623e19c5a384)
![Screenshot 2024-11-19 143501](https://github.com/user-attachments/assets/a168cc49-55b7-47b9-a268-1bdb7b35f8a2)


Editar Usuário:
![Screenshot 2024-11-19 143742](https://github.com/user-attachments/assets/65799484-d09e-4be5-9cf1-d3518af12ca2)

Excluir Usuário:
![Screenshot 2024-11-19 143917](https://github.com/user-attachments/assets/d32eae07-c599-43ba-aaf2-ffec9b279de3)

Listar e buscar Livros:
![Screenshot 2024-11-19 144100](https://github.com/user-attachments/assets/9eda4c72-b056-42cc-bbd1-5e10b62a6f46)
![Screenshot 2024-11-19 144351](https://github.com/user-attachments/assets/10335ec2-0d2e-4059-b1c7-3299d7747ffa)


Cadastrar Livro:
![Screenshot 2024-11-19 144511](https://github.com/user-attachments/assets/be5ab945-f715-4218-abe0-00533cb7fee3)

Editar Livro:
![Screenshot 2024-11-19 144636](https://github.com/user-attachments/assets/1ebe82fe-8da7-4afe-aa1a-db685e5704c2)

Excluir Livro:
![Screenshot 2024-11-19 144756](https://github.com/user-attachments/assets/57e455da-8ee5-4cba-b649-1ae0af9cc57a)

Alugar Livro:
![Screenshot 2024-11-19 144959](https://github.com/user-attachments/assets/f879cdd5-86c6-4d03-9fd6-977d156da0e3)
![Screenshot 2024-11-19 145025](https://github.com/user-attachments/assets/94eaa404-9008-4fbb-b11a-ba9f76abcf91)


Devolver Livro:
![Screenshot 2024-11-19 145156](https://github.com/user-attachments/assets/9d21ec65-32f5-4810-bfc3-7bffd4c858af)
