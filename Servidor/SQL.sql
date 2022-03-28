CREATE TABLE `lixeira` (
  `id` INT PRIMARY KEY,
  `host` VARCHAR(30) NOT NULL,
  `port` INT NOT NULL,
  `status` BOOLEAN NOT NULL, 
  `coord_x` INT NOT NULL, 
  `coord_y` INT NOT NULL, 
  `capacity` INT NOT NULL,
  `qtd_used` DOUBLE NOT NULL
);