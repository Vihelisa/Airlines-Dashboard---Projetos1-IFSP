CREATE DATABASE AirlinesDashboards;
USE AirlinesDashboards;

-- Tabela Empresa
CREATE TABLE Empresa (
    idEmpresa INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(255) NOT NULL,
    Sigla VARCHAR(10) NOT NULL,
    Nacionalidade VARCHAR(50) NOT NULL
);

-- Tabela Funcionario
CREATE TABLE Funcionario (
    idFunc INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(255) NOT NULL,
    Empresa_Nome VARCHAR(255),
    idEmpresa INT NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Senha VARCHAR(255) NOT NULL,
    Cargo VARCHAR(50) NOT NULL,
    FOREIGN KEY (idEmpresa) REFERENCES Empresa(idEmpresa) ON DELETE CASCADE
);

-- Tabela Rotas
CREATE TABLE Rotas (
    idRota INT AUTO_INCREMENT PRIMARY KEY,
    idEmpresa INT NOT NULL,
    EMPRESA_SIGLA VARCHAR(10),
    EMPRESA_NOME VARCHAR(255),
    EMPRESA_NACIONALIDADE VARCHAR(50),
    ANO INT NOT NULL,
    MES INT NOT NULL,
    AEROPORTO_DE_ORIGEM_SIGLA VARCHAR(10),
    AEROPORTO_DE_ORIGEM_NOME VARCHAR(255),
    AEROPORTO_DE_ORIGEM_UF VARCHAR(2),
    AEROPORTO_DE_ORIGEM_REGIAO VARCHAR(50),
    AEROPORTO_DE_ORIGEM_PAIS VARCHAR(50),
    AEROPORTO_DE_ORIGEM_CONTINENTE VARCHAR(50),
    AEROPORTO_DE_DESTINO_SIGLA VARCHAR(10),
    AEROPORTO_DE_DESTINO_NOME VARCHAR(255),
    AEROPORTO_DE_DESTINO_UF VARCHAR(2),
    AEROPORTO_DE_DESTINO_REGIAO VARCHAR(50),
    AEROPORTO_DE_DESTINO_PAIS VARCHAR(50),
    AEROPORTO_DE_DESTINO_CONTINENTE VARCHAR(50),
    NATUREZA VARCHAR(50),
    PASSAGEIROS_PAGOS INT,
    PASSAGEIROS_GRATIS INT,
    ASK DECIMAL(10, 2),
    RPK DECIMAL(10, 2),
    DISTANCIA_VOADA_KM DECIMAL(10, 2),
    DECOLAGENS INT,
    ASSENTOS INT,
    HORAS_VOADAS DECIMAL(10, 2),
    FOREIGN KEY (idEmpresa) REFERENCES Empresa(idEmpresa) ON DELETE CASCADE
);