from account.model.betcardmodel import BetCardModel


class HistoryCardModel(BetCardModel):
    def __init__(self, dic):
        super().__init__(dic)
        self.__predicted_score = dic['score_prevu']
        self.__bet_price = dic['montant']
        self.__date = dic['date_pariage']
        self.__status = dic['etat']
        self.__calculate_reward()
        self.__current_score = dic['score_final']

    def get_current_score(self):
        return self.__current_score

    def __calculate_reward(self):
        self.__reward = round(float(self.__bet_price) * float(self.get_cote()), 2)

    def get_predicted_score(self):
        return self.__predicted_score

    def get_bet_price(self):
        return self.__bet_price

    def get_reward(self):
        return self.__reward

    def get_date(self):
        return self.__date

    def get_status(self):
        return self.__get_status(self.__status)

    @staticmethod
    def __get_status(stat):
        if stat == 'n':
            return 'Non Encore Joue'
        elif stat == 'e':
            return 'Encours'
        elif stat == 't':
            return 'Terminé'
        elif stat == 't':
            return 'Annulé'
