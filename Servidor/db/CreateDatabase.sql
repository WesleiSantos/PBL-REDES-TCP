USE Cidade_Inteligente;
CREATE TABLE lixeira (
    id INT NOT NULL AUTO_INCREMENT,
    host VARCHAR(30),port INT,
    status BOOLEAN NOT NULL,
    coord_x INT NOT NULL,
    coord_y INT NOT NULL,
    capacity INT NOT NULL,
    qtd_used DOUBLE NOT NULL,
    PRIMARY KEY(coord_x, coord_y), 
    KEY (id)
);
CREATE TABLE caminhao (id INT NOT NULL AUTO_INCREMENT,
    status BOOLEAN NOT NULL,
    coord_x INT NOT NULL,
    coord_y INT NOT NULL,
    capacity INT NOT NULL,
    qtd_used DOUBLE NOT NULL,
    next_trash INT,
    PRIMARY KEY(id)
);
SET character_set_client = utf8;
SET character_set_connection = utf8;
SET character_set_results = utf8;
SET collation_connection = utf8_general_ci;