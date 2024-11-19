INSERT INTO Endereco (CEP, Estado, Cidade, Rua, Numero) VALUES
('57000-000', 'Alagoas', 'Maceió', 'Rua A', 123),
('57020-000', 'Alagoas', 'Maceió', 'Rua B', 456),
('57030-000', 'Alagoas', 'Maceió', 'Rua C', 789),
('57040-000', 'Alagoas', 'Maceió', 'Rua D', 101),
('57050-000', 'Alagoas', 'Maceió', 'Rua E', 202),
('57060-000', 'Alagoas', 'Maceió', 'Rua F', 303),
('57070-000', 'Alagoas', 'Maceió', 'Rua G', 404),
('57080-000', 'Alagoas', 'Maceió', 'Rua H', 505),
('57090-000', 'Alagoas', 'Maceió', 'Rua I', 606),
('57100-000', 'Alagoas', 'Maceió', 'Rua J', 707);

INSERT INTO Usuario (CPF, Nome, Sobrenome, Email, Telefone, ID_Endereco) VALUES
('1234567890', 'João', 'Silva', 'joao.silva@email.com', '(82) 99999-9999', 1),
('9876543210', 'Maria', 'Oliveira', 'maria.oliveira@email.com', '(82) 98888-8888', 2),
('4510237890', 'Ana', 'Souza', 'ana.souza@email.com', '(82) 97777-7777', 3),
('6549873210', 'Pedro', 'Lima', 'pedro.lima@email.com', '(82) 96666-6666', 4),
('3216549870', 'Clara', 'Menezes', 'clara.menezes@email.com', '(82) 95555-5555', 5),
('7896541230', 'Lucas', 'Santos', 'lucas.santos@email.com', '(82) 94444-4444', 6),
('1597534860', 'Carla', 'Ramos', 'carla.ramos@email.com', '(82) 93333-3333', 7),
('8527419630', 'Tiago', 'Costa', 'tiago.costa@email.com', '(82) 92222-2222', 8),
('9517534560', 'Fernanda', 'Silveira', 'fernanda.silveira@email.com', '(82) 91111-1111', 9),
('7539514860', 'Paulo', 'Souza', 'paulo.souza@email.com', '(82) 90000-0000', 10);

INSERT INTO Titulo (Titulo, Autor, Editora, Ano) VALUES
('Introdução a Python', 'John Smith', 'Editora Tech', 2020),
('Banco de Dados Avançado', 'Jane Doe', 'Editora Code', 2021),
('Estruturas de Dados', 'Alan Turing', 'Editora Ciência', 2019),
('Redes de Computadores', 'Andrew Tanenbaum', 'Editora Redes', 2018),
('Fundamentos de Matemática', 'Donald Knuth', 'Editora Matemática', 2022),
('Engenharia de Software', 'Ian Sommerville', 'Editora Soft', 2020),
('Machine Learning Básico', 'Andrew Ng', 'Editora AI', 2021),
('Algoritmos Avançados', 'Robert Sedgewick', 'Editora Ciência', 2019),
('Inteligência Artificial', 'Stuart Russell', 'Editora AI', 2022),
('Matemática Discreta', 'Rosen', 'Editora Matemática', 2020);

INSERT INTO Livro (ISBN, Edicao, Qntd_total, Qntd_disponivel, ID_titulo) VALUES
('9781234567897', '1ª', 10, 7, 1),
('9789876543214', '2ª', 5, 3, 2),
('9781112223334', '3ª', 8, 6, 3),
('9784445556667', '5ª', 6, 4, 4),
('9787778889990', '2ª', 15, 12, 5),
('9781231231234', '1ª', 12, 9, 6),
('9783213213210', '2ª', 7, 5, 7),
('9787897897896', '3ª', 9, 6, 8),
('9784564564563', '4ª', 10, 8, 9),
('9786546546549', '2ª', 14, 11, 10);

INSERT INTO Aluguel (Data_aluguel, Data_devolucao, CPF, ISBN) VALUES
('2024-11-15', '2024-11-22', '1234567890', '9781234567897'),
('2024-11-16', '2024-11-23', '9876543210', '9789876543214'),
('2024-11-17', '2024-11-24', '4510237890', '9781112223334'),
('2024-11-18', '2024-11-25', '6549873210', '9784445556667'),
('2024-11-19', '2024-11-26', '3216549870', '9787778889990'),
('2024-11-20', '2024-11-27', '1234567890', '9781231231234'),
('2024-11-21', '2024-11-28', '9876543210', '9783213213210'),
('2024-11-22', '2024-11-29', '4510237890', '9787897897896'),
('2024-11-23', '2024-11-30', '6549873210', '9784564564563'),
('2024-11-24', '2024-12-01', '3216549870', '9786546546549');