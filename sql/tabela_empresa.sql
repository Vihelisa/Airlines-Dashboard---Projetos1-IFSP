-- Tabela Empresa
CREATE TABLE Empresa (
    id_empresa SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    sigla VARCHAR(10) NOT NULL,
    nacionalidade VARCHAR(50) NOT NULL
);

INSERT INTO Empresa (id_empresa, nome, sigla, nacionalidade) VALUES (1, 'GOL LINHAS AÉREAS S.A.', 'GLO', 'BRASILEIRA');
INSERT INTO Empresa (id_empresa, nome, sigla, nacionalidade) VALUES (2, 'AZUL LINHAS AEREAS BRASILEIRAS S/A', 'AZU', 'BRASILEIRA');
INSERT INTO Empresa (id_empresa, nome, sigla, nacionalidade) VALUES (3, 'TAM LINHAS AEREAS S.A.', 'TAM', 'BRASILEIRA');

