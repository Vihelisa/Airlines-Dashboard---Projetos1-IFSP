CREATE DATABASE AirlinesDashboards;
USE AirlinesDashboards;

-- Tabela Empresa
CREATE TABLE Empresa (
    idEmpresa SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    sigla VARCHAR(10) NOT NULL,
    nacionalidade VARCHAR(50) NOT NULL
);

-- Tabela Funcionario
CREATE TABLE Funcionario (
    idFunc SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    empresa_nome VARCHAR(255),
    idEmpresa INT,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    cargo VARCHAR(50),
    FOREIGN KEY (idEmpresa) REFERENCES Empresa(idEmpresa) ON DELETE CASCADE
);

