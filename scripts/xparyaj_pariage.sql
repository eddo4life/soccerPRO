
CREATE TABLE `pariage` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_compte` varchar(255) NOT NULL,
  `id_match` varchar(255) NOT NULL,
  `date_pariage` date NOT NULL,
  `score_prevu` varchar(5) NOT NULL,
  `montant` double DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

