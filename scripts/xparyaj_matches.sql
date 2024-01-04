CREATE TABLE `matches` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type_de_match` enum('Championnat','Coupe du monde','Eliminatoire','Amical') NOT NULL,
  `pays` varchar(255) NOT NULL,
  `date_match` date NOT NULL,
  `heure_match` time NOT NULL,
  `equipe_receveuse` varchar(255) NOT NULL,
  `equipe_visiteuse` varchar(255) NOT NULL,
  `cote` decimal(10,2) NOT NULL,
  `score_final` varchar(5) NOT NULL DEFAULT '0:0',
  `etat` enum('N','E','T','A','S') NOT NULL DEFAULT 'N',
  PRIMARY KEY (`id`)
);
