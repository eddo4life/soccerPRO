from account.view.user.profile.userprofile import UserProfile
from database.connection import DatabaseConnector
from labs.lab import Lab


class BetModel:
    def __init__(self):
        self.__match_id = None
        self.__score = None
        self.__amount = None
        self.__date = None
        self.__account_id = None

    def save_events(self, bcm_list):
        # testing if amount(s) is/are ok
        total_fund = BetModel.get_total_amount(bcm_list)
        # check if the result is not null
        if total_fund:
            if total_fund != -1:
                # now test if the total is >= to the user current fund
                if UserProfile.user_fund >= total_fund:
                    # retrieving the id
                    self.__account_id = UserProfile.account_id
                    # iterating for each event and save them
                    for bcm in bcm_list:
                        self.__match_id = bcm.get_id_match()
                        # home-away (QlineEdit instance)
                        self.__score = BetModel.get_score(bcm)
                        self.__amount = bcm.get_amount().text()
                        self.__date = (Lab.get_current_date())
                        self.save()
                    # finally update the fund
                    UserProfile.user_fund -= total_fund
                    self.update_fund(UserProfile.user_fund)
                    # operations were 'successful'
                    return True
                else:
                    return 'Insufficient fund : ' + str(total_fund) + " for " + str(UserProfile.user_fund)
            else:
                return 'Amount out of bound, correct range [10-75000]'
        else:
            return 'An amount field was found empty'

    @staticmethod
    def get_total_amount(bcm_list):
        total_fund = 0.0
        for bcm in bcm_list:
            amount = bcm.get_amount().text()
            if len(amount) != 0:
                # converting the amount in float
                amount = float(amount)
                if amount < 10 or amount > 75000:
                    # amount out of bound
                    return -1
                else:
                    # amount ok
                    total_fund += amount
            else:
                # the amount field was found empty
                return None

        return total_fund

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

    def update_fund(self, fund):
        conn = DatabaseConnector()
        conn.connect()
        cursor = conn.get_con().cursor(prepared=True)
        try:
            query = "UPDATE parieur SET solde=%s WHERE code=%s"
            value = (fund, self.__account_id)
            cursor.execute(query, value)
            conn.get_con().commit()
        except Exception as err:
            print(f"Error: {err}")

        if conn.get_con().is_connected():
            conn.get_con().close()

    @staticmethod
    def get_score(bcm):
        home_team = bcm.get_score_home_team().text()
        away_team = bcm.get_score_away_team().text()
        if len(home_team.strip()) == 0:
            home_team = '0'
        if len(away_team.strip()) == 0:
            away_team = '0'

        return home_team + ":" + away_team
