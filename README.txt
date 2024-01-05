+==========UBUNTU:Participants==========+
+-------+-----------+-------------------+
| code  | nom       | prenom            |
+-------+-----------+-------------------+
| 33569 | THEODORIS | Boaz Eddy Cadet   |
| 33190 | ROJOUR    | Dariancy Develyne |
| 33648 | JEAN      | Somara Maillekar  |
| 33900 | THEORK    | Annold Casimir    |
+-------+-----------+-------------------+

#########################################

1) Paramètre de connexion

Les paramètres d'accès à la base de données (hôte, utilisateur, mot de passe et nom de la base de données) sont dans un fichier 'config.json' situé à la racine du projet sous 'ubuntu'. Cette configuration sera effectuée automatiquement via une interface qui apparaîtra en cas d'absence de connexion. Cette fonctionnalité est exclusivement dédiée à l'installation.

Ces informations sont vérifiées dans le fichier 'connection.py' situé à : ubuntu\database. [À analyser en cas de problème d'authentification]

NB : Le fichier 'config.json' doit impérativement conserver ses propriétés (nom, format -> JSON), et toute modification gauchement effectuée entraînera une exception [perte de connection] (il est fortement déconseillé de l'éditer manuellement). En cas de suppression ou de corruption du fichier, le système le recréera automatiquement.

2) Structure SQL

Le script complet de la base de données se trouve dans le dossier 'scripts' situé à la racine du projet sous 'ubuntu'. Les requêtes (de creation de tables) seront exécutées automatiquement lors de la tentative d'établissement de la connexion (si la table existe, elle sera recréée).Les tables doivent impérativement conserver leur structure, car cela pourrait entraîner un dysfonctionnement de l'application. Toutes les instructions données ont été respectées, et aucun champ n'a été ajouté, mais la structure proposée doit rester intacte. Vous pouvez les vérifier dans leur dossier ('scripts') respectif et, lors de la tentative de connexion, vous pouvez également les analyser dans 'Tables(struct)' QTabWidget.


Note : Avant de tenter une connexion 'connect' ou de sauvegarder 'save', il est vivement recommandé de tester 'test' pour s'assurer que tout fonctionne correctement (veuillez également préciser la base de données pour créer les tables). Il est également nécessaire de sauvegarder les propriétés de connexion avant de relancer l'application après avoir établi la connexion.




@UBUNTU