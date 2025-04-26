-- Script SQL para criar a tabela 'produto' no banco de dados SQLite


CREATE TABLE IF NOT EXISTS produto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL,
    data_validade TEXT,
    descricao TEXT,
    status TEXT DEFAULT 'ativo'
);
