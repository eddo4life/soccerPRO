CREATE TABLE `parieur` (
  `code` varchar(255) NOT NULL,
  `nom` varchar(255) NOT NULL,
  `prenom` varchar(255) NOT NULL,
  `sexe` varchar(1) NOT NULL,
  `adresse` varchar(255) NOT NULL,
  `telephone` int NOT NULL,
  `nif_cin` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `mot_de_passe` varchar(255) NOT NULL,
  `solde` float NOT NULL DEFAULT '0',
  `etat` char(1) NOT NULL DEFAULT 'A',
  PRIMARY KEY (`code`),
  UNIQUE KEY `telephone` (`telephone`),
  UNIQUE KEY `nif_cin` (`nif_cin`),
  UNIQUE KEY `username` (`username`)
);

