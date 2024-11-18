DROP TABLE IF EXISTS Aluguel CASCADE;
DROP TABLE IF EXISTS Livro CASCADE;
DROP TABLE IF EXISTS Usuario CASCADE;
DROP TABLE IF EXISTS Administradores CASCADE;

CREATE TABLE Usuario (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefone VARCHAR(15)
);

CREATE TABLE Livro (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    autor VARCHAR(100),
    ano INT,
    disponibilidade BOOLEAN DEFAULT TRUE,
    usuario_id INT REFERENCES Usuario(id)
);

CREATE TABLE Aluguel (
    id SERIAL PRIMARY KEY,
    livro_id INT REFERENCES Livro(id) ON DELETE CASCADE,
    usuario_id INT REFERENCES Usuario(id) ON DELETE CASCADE,
    data_aluguel TIMESTAMP DEFAULT NOW(),
    data_devolucao TIMESTAMP
);

CREATE TABLE Administradores (
    id SERIAL PRIMARY KEY,
    senha VARCHAR(255) NOT NULL
);