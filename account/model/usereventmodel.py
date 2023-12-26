from account.view.user.profile.userprofile import UserProfile
from database.connection import DatabaseConnector


class UserEventModel:

    @staticmethod
    def load_data_for(status):
        if status == 'pending':
            return UserEventModel.load_pending_events()
        elif status == 'won':
            return UserEventModel.load_won_events()
        elif status == 'lost':
            return UserEventModel.load_lost_events()

    @staticmethod
    def load_pending_events():
        # encours ou non encore joue
        query = """
                    SELECT * FROM pariage JOIN matches ON pariage.id_match = matches.id WHERE matches.etat = 'e' or matches.etat = 'n' and pariage.id_compte=%s;
                    """

        return UserEventModel.load(query)

    @staticmethod
    def load_won_events():
        # encours ou non encore joue
        query = """
                        SELECT * FROM pariage 
                                 JOIN matches ON pariage.id_match = matches.id 
                                          WHERE matches.etat = 't' and matches.score_final = pariage.score_prevu and pariage.id_compte=%s;
                        """

        return UserEventModel.load(query)

    @staticmethod
    def load_lost_events():
        # encours ou non encore joue
        query = """
                       SELECT * FROM pariage 
                              JOIN matches ON pariage.id_match = matches.id 
                                  WHERE matches.etat = 't' and matches.score_final != pariage.score_prevu and pariage.id_compte=%s;
                        """

        return UserEventModel.load(query)

    @staticmethod
    def load(query=None):
        query_not_null = query  # make sure the query was not null
        if not query:
            query = "SELECT * FROM matches WHERE etat='n' "

        conn = DatabaseConnector()
        conn.connect()
        data = []
        try:
            with conn.get_con().cursor() as cursor:
                if UserProfile.account_id and query_not_null:
                    cursor.execute(query, (UserProfile.account_id,))
                else:
                    cursor.execute(query)
                columns = [col[0] for col in cursor.description]  # Fetch column names
                rows = cursor.fetchall()
                for row in rows:
                    # Create a dictionary for each row using column names
                    row_dict = dict(zip(columns, row))
                    row_dict['date_match'] = row_dict['date_match'].strftime('%Y-%m-%d')
                    row_dict['heure_match'] = str(row_dict['heure_match']).removesuffix(':00')
                    # split the score values
                    row_dict['score_away_team'] = str(row_dict['score_final'].split(':')[0])
                    row_dict['score_home_team'] = str(row_dict['score_final'].split(':')[1])
                    data.append(row_dict)
        except:
            ...
        finally:
            if conn.get_con():
                conn.get_con().close()
        return data
