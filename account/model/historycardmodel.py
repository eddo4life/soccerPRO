from account.model.betcardmodel import BetCardModel


class HistoryCardModel(BetCardModel):
    def __init__(self, dic):
        """
        Initializes a HistoryCardModel instance.

        Args:
            dic (dict): A dictionary containing data for initializing the history card.
        """
        super().__init__(dic)
        self.__predicted_score = dic['score_prevu']
        self.__bet_price = dic['montant']
        self.__date = dic['date_pariage']
        self.__status = dic['etat']
        self.__calculate_reward()
        self.__current_score = dic['score_final']

    def get_current_score(self):
        """
        Get the current score of the history card.

        Returns:
            str: The current score.
        """
        return self.__current_score

    def __calculate_reward(self):
        """
        Calculate and set the reward for the history card.
        """
        self.__reward = round(float(self.__bet_price) * float(self.get_cote()), 2)

    def get_predicted_score(self):
        """
        Get the predicted score of the history card.

        Returns:
            str: The predicted score.
        """
        return self.__predicted_score

    def get_bet_price(self):
        """
        Get the bet price of the history card.

        Returns:
            str: The bet price.
        """
        return self.__bet_price

    def get_reward(self):
        """
        Get the reward of the history card.

        Returns:
            float: The reward.
        """
        return self.__reward

    def get_date(self):
        """
        Get the date of the history card.

        Returns:
            str: The date.
        """
        return self.__date

    def get_status(self):
        """
        Get the status of the history card.

        Returns:
            str: The status.
        """
        return self.__get_status(self.__status)

    @staticmethod
    def __get_status(stat):
        """
        Get the human-readable status based on the provided status code.

        Args:
            stat (str): The status code.

        Returns:
            str: The human-readable status.
        """
        if stat == 'n':
            return 'Non Encore Joué'
        elif stat == 'e':
            return 'Encours'
        elif stat == 't':
            return 'Terminé'
        elif stat == 't':
            return 'Annulé'
