from database.connection import DatabaseConnector


class UserEventModel:
    @staticmethod
    def load():
        conn = DatabaseConnector()
        conn.connect()
        data = []
        try:
            with conn.get_con().cursor() as cursor:
                query = "SELECT * FROM Matches"
                cursor.execute(query)
                columns = [col[0] for col in cursor.description]  # Fetch column names
                rows = cursor.fetchall()
                for row in rows:
                    # Create a dictionary for each row using column names
                    row_dict = dict(zip(columns, row))
                    row_dict['date_match'] = row_dict['date_match'].strftime('%Y-%m-%d')
                    row_dict['heure_match'] = str(row_dict['heure_match'])
                    data.append(row_dict)
        except Exception as e:
            print(f'Exception: {e}')
        finally:
            if conn.get_con():
                conn.get_con().close()
        return data

