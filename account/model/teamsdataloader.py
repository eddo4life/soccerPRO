import json


class TeamsDataLoader:
    def __init__(self):
        """
        Initializes a TeamsDataLoader instance, loading football clubs, national teams, and top UEFA championship data.
        """
        self.__clubs = self.__load_clubs('account/model/football_club_teams.json')
        self.__national_teams = self.__load_clubs('account/model/football_national_teams.json')
        self.__uefa_championship = self.__load_clubs('account/model/top_uefa_championship.json')

    def get_clubs(self):
        """
        Get the dictionary of football clubs.

        Returns:
            dict: A dictionary containing football clubs data.
        """
        return self.__clubs

    def get_national_teams(self):
        """
        Get the dictionary of national teams.

        Returns:
            dict: A dictionary containing national teams data.
        """
        return self.__national_teams

    def get_top_championship(self):
        """
        Get the dictionary of top UEFA championship data.

        Returns:
            dict: A dictionary containing top UEFA championship data.
        """
        return self.__uefa_championship

    def __load_clubs(self, file_path):
        """
        Load football clubs or national teams data from a JSON file.

        Args:
            file_path (str): The file path to the JSON file.

        Returns:
            dict: A dictionary containing football clubs or national teams data.
        """
        football_teams_dict = {}

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                football_teams_dict = json.load(file)
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
        except json.JSONDecodeError:
            print(f"Error: Unable to decode JSON from '{file_path}'.")
        except Exception as e:
            print(f"Error: An unexpected error occurred while loading data from '{file_path}': {e}")

        return football_teams_dict
