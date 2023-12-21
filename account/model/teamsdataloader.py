import json


class TeamsDataLoader:

    def __init__(self):
        self.__clubs = self.__load_clubs('account/model/football_club_teams.json')
        self.__national_teams = self.__load_clubs('account/model/football_national_teams.json')
        self.__uefa_championship = self.__load_clubs('account/model/top_uefa_championship.json')

    def get_clubs(self):
        return self.__clubs

    def get_national_teams(self):
        return self.__national_teams

    def get_top_championship(self):
        return self.__uefa_championship

    def __load_clubs(self, file_path):
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
