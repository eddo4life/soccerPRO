import json


class MatchManagementModel:

    def __init__(self):
        self.__clubs = self.__load_clubs('football_club_teams.json')
        self.__national_teams = self.__load_clubs('football_national_teams.json')
        self.__uefa_championship = self.__load_clubs('top_uefa_championship.json')

    def get_clubs(self):
        return self.__clubs

    def get_national_teams(self):
        return self.__national_teams

    def get_top_championship(self):
        return self.__uefa_championship

    def __load_clubs(self, fname):
        file_name = "account/model/" + fname
        # Initialize an empty dictionary
        football_teams_dict = {}

        # Load data from the JSON file
        try:
            with open(file_name, "r") as file:
                football_teams_dict = json.load(file)
            print(f"Successfully loaded data from {file_name}")
        except FileNotFoundError:
            print(f"Error: {file_name} not found.")
        except json.JSONDecodeError:
            print(f"Error: Unable to decode {file_name}. Ensure it is a valid JSON file.")

        # Display the loaded dictionary
        print("Loaded Football Teams Dictionary:")
        print(json.dumps(football_teams_dict, indent=2))
        return football_teams_dict
