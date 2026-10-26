CREATE DATABASE PASSGEN;

USE passgen;

-- Cria a tabela das credênciais do login com a senha.
CREATE TABLE CREDENCIAIS (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    SITE VARCHAR(100),
    EMAIL VARCHAR(100) UNIQUE,
    SENHA TEXT NOT NULL,
    CRIADO TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE credenciais;

-- Criar tabela para configurações básicas como a senha master
CREATE TABLE configuracao (
  ID int NOT NULL AUTO_INCREMENT,
  SALT blob,
  VER_SENHAM blob,
  PRIMARY KEY (ID)
);

DROP TABLE configuracao;