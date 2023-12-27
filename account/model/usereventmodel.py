from account.view.user.profile.userprofile import UserProfile
from database.connection import DatabaseConnector


class UserEventModel:
    @staticmethod
    def load_data_for(status):
        """
        Load user events based on the specified status.

        Args:
            status (str): The status of the events ('pending', 'won', or 'lost').

        Returns:
            list: A list of dictionaries representing user events.
        """
        if status == 'pending':
            return UserEventModel.load_pending_events()
        elif status == 'won':
            return UserEventModel.load_won_events()
        elif status == 'lost':
            return UserEventModel.load_lost_events()

    @staticmethod
    def load_pending_events():
        """
        Load pending user events.

        Returns:
            list: A list of dictionaries representing pending user events.
        """
        query = """
            SELECT * FROM pariage JOIN matches ON pariage.id_match = matches.id 
            WHERE (matches.etat = 'e' OR matches.etat = 'n') AND pariage.id_compte=%s;
        """
        return UserEventModel.load(query)

    @staticmethod
    def load_won_events():
        """
        Load won user events.

        Returns:
            list: A list of dictionaries representing won user events.
        """
        query = """
            SELECT * FROM pariage JOIN matches ON pariage.id_match = matches.id 
            WHERE matches.etat = 't' AND matches.score_final = pariage.score_prevu AND pariage.id_compte=%s;
        """
        return UserEventModel.load(query)

    @staticmethod
    def load_lost_events():
        """
        Load lost user events.

        Returns:
            list: A list of dictionaries representing lost user events.
        """
        query = """
            SELECT * FROM pariage JOIN matches ON pariage.id_match = matches.id 
            WHERE matches.etat = 't' AND matches.score_final != pariage.score_prevu AND pariage.id_compte=%s;
        """
        return UserEventModel.load(query)

    @staticmethod
    def load(query=None):
        """
        Load user events based on the provided query.

        Args:
            query (str): SQL query to fetch user events. If None, a default query is used.

        Returns:
            list: A list of dictionaries representing user events.
        """
        query_not_null = query  # Make sure the query is not null
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
                    # Split the score values
                    row_dict['score_away_team'] = str(row_dict['score_final'].split(':')[0])
                    row_dict['score_home_team'] = str(row_dict['score_final'].split(':')[1])
                    data.append(row_dict)
        except Exception as e:
            print(f'Error {e}')
        finally:
            conn.disconnect()
        return data
