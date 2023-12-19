import mysql.connector


class DatabaseConnector:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = 'ThD.CABE16432578@'
        self.database = 'xparyaj'
        self.__connection = None

    def connect(self):
        self.__connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        if not self.__connection.is_connected():
            print('connection failed')

    def get_con(self):
        return self.__connection

    def disconnect(self):
        if self.__connection.is_connected():
            self.__connection.close()
