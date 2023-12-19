from database.connection import DatabaseConnector


class UserProfileModel:
    def __init__(self, username=None, name=None, sex=None, first_name=None,
                 address=None, telephone=None, nif_cin=None, password=None):
        self._username = username
        self._name = name
        self._sex = sex
        self._first_name = first_name
        self._address = address
        self._telephone = telephone
        self._nif_cin = nif_cin
        self._password = password

    # Getter and Setter for username
    def get_username(self):
        return self._username

    def set_username(self, username):
        self._username = username

    # Getter and Setter for name
    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    # Getter and Setter for sex
    def get_sex(self):
        return self._sex

    def set_sex(self, sex):
        self._sex = sex

    # Getter and Setter for first_name
    def get_first_name(self):
        return self._first_name

    def set_first_name(self, first_name):
        self._first_name = first_name

    # Getter and Setter for address
    def get_address(self):
        return self._address

    def set_address(self, address):
        self._address = address

    # Getter and Setter for telephone
    def get_telephone(self):
        return self._telephone

    def set_telephone(self, telephone):
        self._telephone = str(telephone)

    # Getter and Setter for nif_cin
    def get_nif_cin(self):
        return self._nif_cin

    def set_nif_cin(self, nif_cin):
        self._nif_cin = nif_cin

    # Getter and Setter for password
    def get_password(self):
        return self._password

    def set_password(self, password):
        self._password = password

    def retrieve_data(self):
        conn = DatabaseConnector()
        conn.connect()
        # Create a cursor
        cursor = conn.get_con().cursor()

        # Execute the query
        telephone_number = '99988'
        query = f"SELECT * FROM parieur WHERE telephone = '{telephone_number}' LIMIT 1;"
        cursor.execute(query)

        # Fetch the result
        result = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        conn.get_con().close()

        # Check if a result was found
        if result:
            # Create an instance of UserProfileModel and set the variables
            self.set_username(result[7])
            self.set_name(result[1])
            self.set_first_name(result[2])
            self.set_sex(result[3])
            self.set_address(result[4])
            self.set_telephone(result[5])
            self.set_nif_cin(result[6])
            self.set_password(result[8])
        else:
            print("No data found for the given telephone number.")

    def get_all(self):
        conn = DatabaseConnector()
        conn.connect()
        self.datas = []
        try:
            with conn.get_con().cursor() as cursor:
                query = "SELECT code,username,nom,prenom,sexe,telephone,adresse,solde,etat FROM parieur"
                cursor.execute(query)
                self.datas.extend(cursor.fetchall())
        except Exception as e:
            print(f'Exception: {e}')

        finally:
            if conn:
                conn.get_con().close()
        return self.datas
