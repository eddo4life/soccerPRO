import json
import sys

import mysql.connector
from PyQt5.QtWidgets import QDialog


def load_credentials():
    """
    Load database credentials data from a JSON file.

    Returns:
        dict: A dictionary containing the credentials.
    """
    datas = {}
    file_path = 'config.json'
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            datas = json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        from config.config import Configuration
        # try to create the file if the file is deleted
        Configuration().save_configuration()
        # make a recursive call to retry the process
        return load_credentials()
    except json.JSONDecodeError:
        print(f"Error: Unable to decode JSON from '{file_path}'.")
        from config.config import Configuration
        # try to create the file if the file was corrupted
        Configuration().save_configuration()
        # make a recursive call to retry the process
        return load_credentials()
    except Exception as e:
        print(f"Error: An unexpected error occurred while loading data from '{file_path}': {e}")

    return datas


class DatabaseConnector:
    def __init__(self, data=None):
        """
        Initializes a DatabaseConnector instance with default connection parameters.
        """
        if not data:
            data = load_credentials()
        self.host = str(data['host']).strip()
        self.user = str(data['user']).strip()
        self.password = str(data['password']).strip()
        self.database = str(data['database']).strip()
        self.__connection = None

    def connect(self, show_config=True):
        """
        Establishes a connection to the MySQL database using the provided parameters.
        """
        try:
            self.__connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return "Success!"
        except mysql.connector.Error as err:

            if show_config:
                from config.config import Configuration
                dialog = Configuration()
                if dialog.exec_() != QDialog.Accepted:
                    sys.exit()
            else:
                return err.__str__()

    def get_con(self):
        """
        Returns the MySQL connection object.
        """
        return self.__connection

    def disconnect(self):
        """
        Disconnects from the MySQL database if a connection is active.
        """
        if self.__connection:
            if self.__connection.is_connected():
                self.__connection.close()
