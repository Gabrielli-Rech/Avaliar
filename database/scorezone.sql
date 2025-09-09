
-- ========================================
-- ScoreZone MySQL - Banco completo
-- ========================================

CREATE DATABASE IF NOT EXISTS scorezone CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE scorezone;

-- -----------------------------
-- Usuários
-- -----------------------------
CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL, -- hash na aplicação
    avatar_url VARCHAR(400),
    icon_url VARCHAR(400),
    capa_url VARCHAR(400),
    bio TEXT,
    tema ENUM('dark','light') NOT NULL DEFAULT 'dark',
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- -----------------------------
-- Classificação indicativa
-- -----------------------------
CREATE TABLE classificacao (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    faixa_etaria VARCHAR(20) NOT NULL,
    descricao VARCHAR(200)
);

INSERT IGNORE INTO classificacao (faixa_etaria, descricao) VALUES
('Livre', 'Indicado para todos os públicos'),
('10+', 'Não recomendado para menores de 10 anos'),
('12+', 'Não recomendado para menores de 12 anos'),
('14+', 'Não recomendado para menores de 14 anos'),
('16+', 'Não recomendado para menores de 16 anos'),
('18+', 'Conteúdo adulto');

-- -----------------------------
-- Itens
-- -----------------------------
CREATE TABLE items (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(300) NOT NULL,
    subtitulo VARCHAR(300),
    categoria ENUM('jogo','livro','filme','serie') NOT NULL,
    descricao TEXT,
    ano INT,
    plataforma VARCHAR(200),
    publisher VARCHAR(200),
    diretor_autor VARCHAR(200),
    capa_url VARCHAR(400),
    largura_img INT,
    altura_img INT,
    classificacao_id BIGINT DEFAULT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (classificacao_id) REFERENCES classificacao(id)
);

-- -----------------------------
-- Subcategorias e ligação
-- -----------------------------
CREATE TABLE subcategories (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

INSERT IGNORE INTO subcategories (nome) VALUES 
('Ação'), ('Terror'), ('Comédia'), ('Drama'), ('Aventura'), ('Ficção Científica');

CREATE TABLE item_subcategories (
    item_id BIGINT NOT NULL,
    subcategory_id BIGINT NOT NULL,
    PRIMARY KEY(item_id, subcategory_id),
    FOREIGN KEY(item_id) REFERENCES items(id) ON DELETE CASCADE,
    FOREIGN KEY(subcategory_id) REFERENCES subcategories(id) ON DELETE CASCADE
);

-- -----------------------------
-- Reviews
-- -----------------------------
CREATE TABLE reviews (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    item_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    nota TINYINT NOT NULL CHECK (nota BETWEEN 1 AND 10),
    titulo VARCHAR(300),
    comentario TEXT,
    visibilidade ENUM('public','private','moderation') DEFAULT 'public',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY one_review_per_user_item (item_id, user_id),
    FOREIGN KEY(item_id) REFERENCES items(id) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE review_images (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    review_id BIGINT NOT NULL,
    uploader_id BIGINT,
    url VARCHAR(400) NOT NULL,
    descricao VARCHAR(300),
    ordem INT DEFAULT 0,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(review_id) REFERENCES reviews(id) ON DELETE CASCADE,
    FOREIGN KEY(uploader_id) REFERENCES users(id) ON DELETE SET NULL
);

-- -----------------------------
-- Likes/reactions
-- -----------------------------
CREATE TABLE review_likes (
    review_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    tipo VARCHAR(30) DEFAULT 'like',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(review_id, user_id, tipo),
    FOREIGN KEY(review_id) REFERENCES reviews(id) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- -----------------------------
-- Imagens dos itens
-- -----------------------------
CREATE TABLE item_images (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    item_id BIGINT NOT NULL,
    url VARCHAR(400) NOT NULL,
    legenda VARCHAR(300),
    ordem INT DEFAULT 0,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(item_id) REFERENCES items(id) ON DELETE CASCADE
);

-- -----------------------------
-- Favoritos
-- -----------------------------
CREATE TABLE favorites (
    user_id BIGINT NOT NULL,
    item_id BIGINT NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(user_id, item_id),
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(item_id) REFERENCES items(id) ON DELETE CASCADE
);

-- -----------------------------
-- Listas do usuário
-- -----------------------------
CREATE TABLE user_lists (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    titulo VARCHAR(150) NOT NULL,
    descricao TEXT,
    tipo VARCHAR(50),
    publico BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE list_items (
    list_id BIGINT NOT NULL,
    item_id BIGINT NOT NULL,
    nota_pessoal TINYINT CHECK (nota_pessoal BETWEEN 1 AND 10),
    observacao TEXT,
    adicionado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(list_id, item_id),
    FOREIGN KEY(list_id) REFERENCES user_lists(id) ON DELETE CASCADE,
    FOREIGN KEY(item_id) REFERENCES items(id) ON DELETE CASCADE
);

-- ==============================
-- Trigger Classificação Indicativa
-- ==============================
DELIMITER $$

CREATE TRIGGER set_classificacao_before_insert
BEFORE INSERT ON items
FOR EACH ROW
BEGIN
    DECLARE cid BIGINT;

    IF EXISTS (SELECT 1 FROM subcategories s
               JOIN item_subcategories isub ON s.id = isub.subcategory_id
               WHERE isub.item_id = NEW.id AND s.nome = 'Terror') THEN
        SELECT id INTO cid FROM classificacao WHERE faixa_etaria = '14+' LIMIT 1;
        SET NEW.classificacao_id = cid;
    ELSEIF EXISTS (SELECT 1 FROM subcategories s
                   JOIN item_subcategories isub ON s.id = isub.subcategory_id
                   WHERE isub.item_id = NEW.id AND s.nome = 'Ação') THEN
        SELECT id INTO cid FROM classificacao WHERE faixa_etaria = '12+' LIMIT 1;
        SET NEW.classificacao_id = cid;
    ELSE
        SELECT id INTO cid FROM classificacao WHERE faixa_etaria = 'Livre' LIMIT 1;
        SET NEW.classificacao_id = cid;
    END IF;
END $$

DELIMITER ;
