from database.connection import DatabaseConnector
from labs.lab import Lab


class MatchManagementModel:
    def __init__(self, id_match, type_de_match, pays, date_match, heure_match, equipe_visiteuse, equipe_receveuse, cote,
                 score_final='0:0', etat='N'):
        self.__id_match = id_match
        self.__type_de_match = type_de_match
        self.__pays = pays
        self.__date_match = date_match
        self.__heure_match = heure_match
        self.__equipe_visiteuse = equipe_visiteuse
        self.__equipe_receveuse = equipe_receveuse
        self.__cote = cote.replace(",", ".")
        self.__score_final = MatchManagementModel.removeLeadingZeros(score_final)
        self.__etat = etat

    @staticmethod
    def removeLeadingZeros(score_str):
        """
        Removes leading zeros from the hour part of a time string.

        Parameters:
        - time_str (str): A time string in the format "HH:MM".

        Returns:
        - str: The formatted time string with leading zeros removed from the hour part.
        """

        # Convert the string to an integer, removing leading zeros
        score1, score2 = map(int, score_str.split(':'))

        # Format the integers back to a string without leading zeros
        return f"{score1}:{score2}"

    @staticmethod
    def load():
        conn = DatabaseConnector()
        conn.connect()
        data = []
        try:
            with conn.get_con().cursor() as cursor:
                cursor.execute("SELECT * FROM Matches WHERE etat!='s'")
                data = cursor.fetchall()
        except Exception as e:
            # Handle the case when the table is not found (improve exception handling later).
            Lab.invoke_config(f'Exception: {e}')
        finally:
            conn.disconnect()
        return data

    def save(self):
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
        except Exception as err:
            print(f"Error: {err}")

        finally:
            conn.disconnect()

    @staticmethod
    def delete(id_match):
        conn = DatabaseConnector()
        conn.connect()
        cursor = conn.get_con().cursor(prepared=True)
        try:
            query = "UPDATE matches SET etat='S' WHERE id=%s"

            cursor.execute(query, (id_match,))
            conn.get_con().commit()
        except Exception as err:
            print(f"Error: {err}")
        finally:
            conn.disconnect()

    def update(self):
        conn = DatabaseConnector()
        conn.connect()
        cursor = conn.get_con().cursor(prepared=True)
        try:
            query = """
                          UPDATE matches SET  
                          type_de_match=%s, pays=%s, date_match=%s, heure_match=%s, equipe_receveuse=%s, equipe_visiteuse=%s, cote=%s, score_final=%s, etat=%s 
                          WHERE id=%s and etat!='t' 
                      """
            value = (self.__type_de_match, self.__pays, self.__date_match, self.__heure_match, self.__equipe_receveuse,
                     self.__equipe_visiteuse, self.__cote, self.__score_final, self.__etat, self.__id_match)
            cursor.execute(query, value)
            conn.get_con().commit()
        except Exception as err:
            print(f"Error: {err}")
        finally:
            conn.disconnect()

    def cancel_match_and_refund(self):
        conn = DatabaseConnector()
        conn.connect()
        cursor = conn.get_con().cursor(prepared=True)

        try:
            # Get details of the canceled match
            query_select = "SELECT id_compte, montant FROM pariage WHERE id_match = %s"
            cursor.execute(query_select, (self.__id_match,))
            refund_details = cursor.fetchall()

            # Refund each user
            for user_id, refund_amount in refund_details:
                query_update = "UPDATE parieur SET solde = solde + %s WHERE code = %s"
                cursor.execute(query_update, (refund_amount, user_id))

            # Delete the canceled match from 'pariage' table
            query_delete = "DELETE FROM pariage WHERE id_match = %s"
            cursor.execute(query_delete, (self.__id_match,))

            conn.get_con().commit()

        except Exception as err:
            print(f"Error: {err}")
        finally:
            conn.disconnect()

    def refund_users_if_scores_match(self):
        conn = DatabaseConnector()
        conn.connect()
        cursor = conn.get_con().cursor(prepared=True)

        try:
            # Get the cote,final score of the match
            query_match = "SELECT cote,score_final FROM matches WHERE id = %s"
            cursor.execute(query_match, (self.__id_match,))
            cote, match_score = cursor.fetchone()

            # Check if scores match in pariage table
            query_pariage = "SELECT id_compte, montant, score_prevu FROM pariage WHERE id_match = %s"
            cursor.execute(query_pariage, (self.__id_match,))
            pariage_details = cursor.fetchall()

            for user_id, refund_amount, predicted_score in pariage_details:
                if predicted_score == match_score:
                    # Refund the user
                    query_update = "UPDATE parieur SET solde = solde + %s WHERE code = %s"
                    cursor.execute(query_update, ((float(refund_amount) * float(cote)), user_id))

            conn.get_con().commit()
        except Exception as err:
            print(f"Error: {err}")

        finally:
            conn.disconnect()

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
