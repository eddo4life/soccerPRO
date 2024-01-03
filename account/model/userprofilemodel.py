from database.connection import DatabaseConnector
from labs.lab import Lab


class UserProfileModel:
    def __init__(self, account_id=None, username=None, name=None, sex=None, first_name=None,
                 address=None, telephone=None, nif_cin=None, password=None, status=None):
        self.__account_id = account_id
        self.__username = username
        self.__name = name
        self.__sex = sex
        self.__first_name = first_name
        self.__address = address
        self.__telephone = telephone
        self.__nif_cin = nif_cin
        self.__password = password
        self.__sold = '0.0'
        self.__status = status

    # Getter and Setter for username
    def get_account_id(self):
        return self.__account_id

    def get_username(self):
        return self.__username

    def set_username(self, username):
        self.__username = username

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

    def get_first_name(self):
        return self.__first_name

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def get_address(self):
        return self.__address

    def set_address(self, address):
        self.__address = address

    def get_telephone(self):
        return self.__telephone

    def set_telephone(self, telephone):
        self.__telephone = str(telephone)

    def get_nif_cin(self):
        return self.__nif_cin

    def set_nif_cin(self, nif_cin):
        self.__nif_cin = nif_cin

    # Getter and Setter for password
    def get_password(self):
        return self.__password

    def get_sold(self):
        return self.__sold

    def get_status(self):
        return self.__status

    def set_password(self, password):
        self.__password = password

    def set_sold(self, sold):
        self.__sold = sold

    def set_status(self, status):
        self.__status = status

    def retrieve_data(self, user_id, user_password):
        conn = DatabaseConnector()
        conn.connect()
        # Create a cursor
        cursor = conn.get_con().cursor()
        # Execute the query
        query = "SELECT * FROM parieur WHERE telephone = %s or username = %s and mot_de_passe=%s and etat!='s' LIMIT 1;"
        cursor.execute(query, (user_id, user_id, user_password))

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
            self.set_status(result[10])
        else:
            return None

    @staticmethod
    def get_all():
        conn = DatabaseConnector()
        conn.connect()
        datas = []
        try:
            with conn.get_con().cursor() as cursor:
                query = "SELECT code,username,nom,prenom,sexe,telephone,adresse,solde,etat FROM parieur where etat='A'"
                cursor.execute(query)
                datas.extend(cursor.fetchall())
        except Exception as e:
            # Handle the case when the table is not found (improve exception handling later).
            Lab.invoke_config(f'Exception: {e}')

        finally:
            conn.disconnect()
        return datas

    def valid_data(self):
        return all([self.__username, self.__name, self.__first_name, self.__address, self.__telephone, self.__nif_cin])

    # signing up
    def save(self):
        conn = DatabaseConnector()
        conn.connect()
        cursor = conn.get_con().cursor(prepared=True)
        try:
            query = """
                            INSERT INTO parieur
                            (code, nom, prenom, sexe, adresse, telephone, nif_cin, username, mot_de_passe, solde, etat)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
            value = (self.__account_id, self.__name, self.__first_name, self.__sex, self.__address,
                     self.__telephone, self.__nif_cin, self.__username, self.__password, self.__sold, self.__status)

            cursor.execute(query, value)
            conn.get_con().commit()
        except Exception as err:
            conn.disconnect()
            return str(err)
        finally:
            conn.disconnect()
        return None

    # update profile
    def update(self):
        conn = DatabaseConnector()
        conn.connect()
        cursor = conn.get_con().cursor(prepared=True)
        try:
            query = """
                        UPDATE parieur SET nom=%s, prenom=%s, sexe=%s, adresse=%s, telephone=%s, nif_cin=%s, username=%s, mot_de_passe=%s, etat=%s where code=%s
                    """
            value = (self.__name, self.__first_name, self.__sex, self.__address, self.__telephone, self.__nif_cin,
                     self.__username,
                     self.__password, self.__status, self.__account_id)

            cursor.execute(query, value)
            conn.get_con().commit()
        except Exception as err:
            print(f"Error: {err}")

        finally:
            conn.disconnect()

    @staticmethod
    def delete_account(code):
        conn = DatabaseConnector()
        conn.connect()
        cursor = conn.get_con().cursor(prepared=True)
        try:
            query = " UPDATE parieur SET etat='S' where code=%s"
            cursor.execute(query, (code,))
            conn.get_con().commit()
        except Exception as err:
            print(f"Error: {err}")

        finally:
            conn.disconnect()

    @staticmethod
    def update_sold(account_id, new_amount):
        conn = DatabaseConnector()
        conn.connect()
        cursor = conn.get_con().cursor(prepared=True)
        try:
            query = "UPDATE parieur SET solde=solde+%s WHERE code=%s"
            value = (new_amount, account_id)
            cursor.execute(query, value)
            conn.get_con().commit()
        except Exception as err:
            print(f"Error: {err}")

        finally:
            conn.disconnect()

    @staticmethod
    def reset_password(password, nif_cin, telephone):
        conn = DatabaseConnector()
        conn.connect()
        cursor = conn.get_con().cursor(prepared=True)
        try:
            query = "SELECT * FROM parieur where telephone =%s and nif_cin=%s"
            cursor.execute(query, (telephone, nif_cin))
            if cursor.fetchall():
                query = "UPDATE parieur SET mot_de_passe=%s WHERE nif_cin =%s and telephone=%s"
                value = (password, nif_cin, telephone)
                cursor.execute(query, value)
                conn.get_con().commit()
            else:
                return False
        except Exception as err:
            print(f"Error: {err}")
        finally:
            conn.disconnect()
        return True
