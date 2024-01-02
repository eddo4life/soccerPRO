
CREATE TABLE `matches` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type_de_match` enum('championnat','coupe du monde','eliminatoire','amical') NOT NULL,
  `pays` varchar(255) NOT NULL,
  `date_match` date NOT NULL,
  `heure_match` time NOT NULL,
  `equipe_receveuse` varchar(255) NOT NULL,
  `equipe_visiteuse` varchar(255) NOT NULL,
  `cote` decimal(10,2) NOT NULL,
  `score_final` varchar(5) NOT NULL DEFAULT '0:0',
  `etat` enum('n','e','t','a','s') NOT NULL DEFAULT 'n',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
