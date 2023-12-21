from database.connection import DatabaseConnector


class MatchManagementModel:
    def __init__(self, type_de_match, pays, date_match, heure_match, equipe_visiteuse, equipe_receveuse, cote,
                 score_final='0:0', etat='N'):
        self.__type_de_match = type_de_match
        self.__pays = pays
        self.__date_match = date_match
        self.__heure_match = heure_match
        self.__equipe_visiteuse = equipe_visiteuse
        self.__equipe_receveuse = equipe_receveuse
        self.__cote = cote.replace(",", ".")
        self.__score_final = score_final
        self.__etat = etat

    def save(self):
        print("Saving")
        print(self.__str__())
        self.enregistrer()

    def enregistrer(self):
        conn = DatabaseConnector()
        conn.connect()
        cursor = conn.get_con().cursor(prepared=True)
        try:
            query = """
                          INSERT INTO matches
                          (id, type_de_match, pays, date_match, heure_match, equipe_receveuse, equipe_visiteuse, cote, score_final, etat)
                          VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                      """
            value = (self.__type_de_match, self.__pays, self.__date_match, self.__heure_match, self.__equipe_receveuse,
                     self.__equipe_visiteuse, self.__cote, self.__score_final, self.__etat)
            cursor.execute(query, value)
            conn.get_con().commit()
            print("Data successfully inserted.")
        except Exception as err:
            print(f"Error: {err}")

        if conn.get_con().is_connected():
            conn.get_con().close()

    # Getter methods

    def get_type_de_match(self):
        return self.__type_de_match

    def get_pays(self):
        return self.__pays

    def get_date_match(self):
        return self.__date_match

    def get_heure_match(self):
        return self.__heure_match

    def get_equipe_visiteuse(self):
        return self.__equipe_visiteuse

    def get_equipe_receveuse(self):
        return self.__equipe_receveuse

    def get_cote(self):
        return self.__cote

    def get_score_final(self):
        return self.__score_final

    def get_etat(self):
        return self.__etat

        # Setter methods

    def set_type_de_match(self, type_de_match):
        self.__type_de_match = type_de_match

    def set_pays(self, pays):
        self.__pays = pays

    def set_date_match(self, date_match):
        self.__date_match = date_match

    def set_heure_match(self, heure_match):
        self.__heure_match = heure_match

    def set_equipe_visiteuse(self, equipe_visiteuse):
        self.__equipe_visiteuse = equipe_visiteuse

    def set_equipe_receveuse(self, equipe_receveuse):
        self.__equipe_receveuse = equipe_receveuse

    def set_cote(self, cote):
        self.__cote = cote.replace(",", ".")

    def set_score_final(self, score_final):
        self.__score_final = score_final

    def set_etat(self, etat):
        self.__etat = etat

    def __str__(self):
        return f"Match(type_de_match={self.__type_de_match}, pays={self.__pays}, date_match={self.__date_match}, " \
               f"heure_match={self.__heure_match}, equipe_visiteuse={self.__equipe_visiteuse}, " \
               f"equipe_receveuse={self.__equipe_receveuse}, cote={self.__cote}, score_final={self.__score_final}, " \
               f"etat={self.__etat})"
