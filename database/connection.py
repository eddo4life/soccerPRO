import os
import sys

import mysql.connector
from PyQt5.QtWidgets import QMessageBox


class DatabaseConnector:
    def __init__(self):
        """
        Initializes a DatabaseConnector instance with default connection parameters.
        """
        self.host = 'localhost'
        self.user = 'root'
        self.password = 'password'
        self.database = 'xparyaj'
        self.__connection = None

    def connect(self):
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

        except mysql.connector.Error as err:
            QMessageBox.warning(None, "Connection Error", err.__str__() + str(Locate.file_location()), QMessageBox.Ok)
            sys.exit()

    def get_con(self):
        """
        Returns the MySQL connection object.

        Returns:
            mysql.connector.connection_cext.CMySQLConnection: The MySQL connection object.
        """
        return self.__connection

    def disconnect(self):
        """
        Disconnects from the MySQL database if a connection is active.
        """
        if self.__connection:
            if self.__connection.is_connected():
                self.__connection.close()


class Locate:
    """
    A class for handling file location information when the connection to the database fails.

    Attributes:
    - No class attributes defined.

    Methods:
    - file_location: Returns a formatted string containing the script directory,
      and script filename.

    """

    @staticmethod
    def file_location():
        # Get the script file name
        script_location = os.path.abspath(__file__)
        script_directory, script_filename = os.path.split(script_location)
        result = f"""
        
Script directory: {script_directory}

Script filename: {script_filename}
                 """
        return result
