class BetCardModel:
    def __init__(self, dic):
        self.__match_id = dic['id']
        self.__home_team = dic['equipe_receveuse']
        self.__away_team = dic['equipe_visiteuse']
        self.__time = dic['heure_match']
        self.__country = dic['pays']
        self.__type_of_match = dic['type_de_match']
        self.__cote = dic['cote']
        self.__amount = None
        self.__score_away_team = None
        self.__score_home_team = None

    def get_id_match(self):
        return self.__match_id

    def get_home_team(self):
        return self.__home_team

    def get_away_team(self):
        return self.__away_team

    def get_time(self):
        return self.__time

    def get_country(self):
        return self.__country

    def get_type_of_match(self):
        return self.__type_of_match

    def get_cote(self):
        return self.__cote

    def get_score_away_team(self):
        return self.__score_away_team

    def get_score_home_team(self):
        return self.__score_home_team

    def get_amount(self):
        return self.__amount

    def set_amount(self, amount):
        self.__amount = amount

    def set_score_away_team(self, score):
        self.__score_away_team = score

    def set_score_home_team(self, score):
        self.__score_home_team = score
