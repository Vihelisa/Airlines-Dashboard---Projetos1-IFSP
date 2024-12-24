CREATE DATABASE AirlinesDashboards;
USE AirlinesDashboards;

-- Tabela Empresa
CREATE TABLE Empresa (
    idEmpresa SERIAL PRIMARY KEY,
    Nome VARCHAR(255) NOT NULL,
    Sigla VARCHAR(10) NOT NULL,
    Nacionalidade VARCHAR(50) NOT NULL
);

-- Tabela Funcionario
CREATE TABLE Funcionario (
    idFunc SERIAL PRIMARY KEY,
    Nome VARCHAR(255) NOT NULL,
    Empresa_Nome VARCHAR(255),
    idEmpresa INT NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Senha VARCHAR(255) NOT NULL,
    Cargo VARCHAR(50),
    FOREIGN KEY (idEmpresa) REFERENCES Empresa(idEmpresa) ON DELETE CASCADE
);

