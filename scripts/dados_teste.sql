INSERT INTO Usuario (nome, email, telefone) VALUES 
('Ana Silva', 'ana@email.com', '123456789')
ON CONFLICT (email) DO NOTHING;

INSERT INTO Usuario (nome, email, telefone) VALUES 
('Matheus Pereira', 'joao@email.com', '987654321')
ON CONFLICT (email) DO NOTHING;

INSERT INTO Livro (titulo, autor, ano, disponibilidade) VALUES 
('Harry Potter e a Pedra Filosofal', 'J. K. Rowling', 1997, TRUE),
('O Cortico', 'Aluisio Azevedo', 1890, TRUE),
('Dom Casmurro', 'Machado de Assis', 1899, TRUE);

INSERT INTO Aluguel (usuario_id, livro_id, data_aluguel) VALUES 
(1, 1, '2024-11-10'),
(2, 2, '2024-11-11');

INSERT INTO Administradores (senha) VALUES ('1234')
ON CONFLICT DO NOTHING;