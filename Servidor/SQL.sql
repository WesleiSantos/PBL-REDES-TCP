CREATE TABLE `lixeira` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `host` VARCHAR(30),
  `port` INT,
  `status` BOOLEAN NOT NULL, 
  `coord_x` INT NOT NULL, 
  `coord_y` INT NOT NULL, 
  `capacity` INT NOT NULL,
  `qtd_used` DOUBLE NOT NULL,
  PRIMARY KEY(`coord_x`, `coord_y`)
);