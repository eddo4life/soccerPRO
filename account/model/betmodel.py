from account.view.user.profile.userprofile import UserProfile
from database.connection import DatabaseConnector
from labs.lab import Lab


class BetModel:
    def __init__(self, bcm_list):
        # testing if amount(s) is/are ok
        res = BetModel.get_amount(bcm_list)
        # a boolean is returned
        if type(res) is bool:
            # saving
            for bcm in bcm_list:
                self.__account_id = UserProfile.account_id
                self.__match_id = bcm.get_id_match()
                # home-away (QlineEditInstance)
                self.__score = BetModel.get_score(bcm)
                self.__amount = bcm.get_amount().text()
                self.__date = (Lab.get_current_date())
        else:
            print('amount not ok for card', res)

    @staticmethod
    def get_score(bcm):
        home_team = bcm.get_score_home_team().text()
        away_team = bcm.get_score_away_team().text()
        if len(home_team.strip()) == 0:
            home_team = '0'
        if len(away_team.strip()) == 0:
            away_team = '0'

        return home_team + ":" + away_team

    @staticmethod
    def get_amount(bcm_list):
        # create a list of invalid events
        lst = []
        for bcm in bcm_list:
            amount = bcm.get_amount().text()
            if len(amount) != 0:
                if float(amount) < 10 or float(75000) > 75000:
                    # amount out of bound
                    lst.append(bcm)
            else:
                # the amount field was found empty
                lst.append(bcm)

        return lst if lst else False

    def save(self):
        conn = DatabaseConnector()
        conn.connect()
        cursor = conn.get_con().cursor(prepared=True)
        try:
            query = """
                                    INSERT INTO pariage
                                    (id, id_compte, id_match, date_pariage, score_prevu, montant)
                                    VALUES (NULL, %s, %s, %s, %s, %s)
                                """
            value = (self.__account_id, self.__match_id, self.__date, self.__score,
                     self.__amount)
            cursor.execute(query, value)
            conn.get_con().commit()
        except Exception as err:
            print(f"Error: {err}")

        if conn.get_con().is_connected():
            conn.get_con().close()
