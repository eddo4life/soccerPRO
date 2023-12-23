from database.connection import DatabaseConnector


class UserProfileModel:
    def __init__(self, username=None, name=None, sex=None, first_name=None,
                 address=None, telephone=None, nif_cin=None, password=None):
        self.__account_id = None
        self.__username = username
        self.__name = name
        self.__sex = sex
        self.__first_name = first_name
        self.__address = address
        self.__telephone = telephone
        self.__nif_cin = nif_cin
        self.__password = password
        self.__sold = None

    # Getter and Setter for username
    def get_account_id(self):
        return self.__account_id

    def get_username(self):
        return self.__username

    def set_username(self, username):
        self.__username = username

    # Getter and Setter for name
    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    # Getter and Setter for sex
    def get_sex(self):
        return self.__sex

    def set_sex(self, sex):
        self.__sex = sex

    def set_account_id(self, account_id):
        self.__account_id = account_id

    # Getter and Setter for first_name
    def get_first_name(self):
        return self.__first_name

    def set_first_name(self, first_name):
        self.__first_name = first_name

    # Getter and Setter for address
    def get_address(self):
        return self.__address

    def set_address(self, address):
        self.__address = address

    # Getter and Setter for telephone
    def get_telephone(self):
        return self.__telephone

    def set_telephone(self, telephone):
        self.__telephone = str(telephone)

    # Getter and Setter for nif_cin
    def get_nif_cin(self):
        return self.__nif_cin

    def set_nif_cin(self, nif_cin):
        self.__nif_cin = nif_cin

    # Getter and Setter for password
    def get_password(self):
        return self.__password

    def get_sold(self):
        return self.__sold

    def set_password(self, password):
        self.__password = password

    def set_sold(self, sold):
        self.__sold = sold

    def retrieve_data(self):
        conn = DatabaseConnector()
        conn.connect()
        # Create a cursor
        cursor = conn.get_con().cursor()

        # Execute the query
        telephone_number = '5555432'
        query = "SELECT * FROM parieur WHERE telephone = %s LIMIT 1;"
        cursor.execute(query, (telephone_number,))

        # Fetch the result
        result = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        conn.get_con().close()

        # Check if a result was found
        if result:
            # Create an instance of UserProfileModel and set the variables
            self.set_account_id(result[0])
            self.set_name(result[1])
            self.set_first_name(result[2])
            self.set_sex(result[3])
            self.set_address(result[4])
            self.set_telephone(result[5])
            self.set_nif_cin(result[6])
            self.set_username(result[7])
            self.set_password(result[8])
            self.set_sold(result[9])

        else:
            print("No data found for the given telephone number.")

    def get_all(self):
        conn = DatabaseConnector()
        conn.connect()
        datas = []
        try:
            with conn.get_con().cursor() as cursor:
                query = "SELECT code,username,nom,prenom,sexe,telephone,adresse,solde,etat FROM parieur"
                cursor.execute(query)
                datas.extend(cursor.fetchall())
        except Exception as e:
            print(f'Exception: {e}')

        finally:
            if conn:
                conn.get_con().close()
        return datas

    @staticmethod
    def update_sold(account_id, new_amount):
        conn = DatabaseConnector()
        conn.connect()
        cursor = conn.get_con().cursor(prepared=True)
        try:
            query = """
                UPDATE parieur SET solde=solde+%s WHERE code=%s
            """
            value = (new_amount, account_id)

            cursor.execute(query, value)
            print('query executed')
            conn.get_con().commit()
            print("Data successfully updated.")
        except Exception as err:
            print(f"Error: {err}")

        if conn.get_con().is_connected():
            conn.get_con().close()
