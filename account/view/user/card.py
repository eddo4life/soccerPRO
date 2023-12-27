from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget, QScrollArea

from account.model.historycardmodel import HistoryCardModel
from account.model.usereventmodel import UserEventModel


class Card(QWidget):
    def __init__(self, status):
        """
        Initializes the Card widget.

        Parameters:
        - status: str
            The status of events to load.

        Returns:
        None
        """
        super().__init__()
        vbox = QVBoxLayout()

        # Gather data for full events (matches and bet)
        for counter, d in enumerate(UserEventModel.load_data_for(status)):
            vbox.addWidget(self.card(counter, d))

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_widget = QWidget()
        scroll_widget.setLayout(vbox)

        scroll_area.setWidget(scroll_widget)

        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def card(self, count, dic):
        """
        Creates and returns a widget representing a history card with relevant information.

        Parameters:
        - count: int
            The index or counter for alternating background colors.
        - dic: dict
            The dictionary containing history card data.

        Returns:
        QWidget
        """
        hcm = HistoryCardModel(dic)
        wdg = QWidget()
        vbox = QVBoxLayout()
        wdg.setFixedHeight(180)

        # Set background color based on index
        if count % 2 == 0:
            wdg.setStyleSheet('background-color:rgb(253,253,253)')
        else:
            wdg.setStyleSheet('background-color:rgb(247,247,247)')

        top_hbox = QHBoxLayout()
        teams = hcm.get_home_team() + " - " + hcm.get_away_team()
        teams_label = QLabel('<h2>' + teams + '</h2>')

        stat_label = QLabel("(" + hcm.get_status() + ")")
        top_hbox.addWidget(teams_label)
        top_hbox.addWidget(stat_label)
        top_hbox.setAlignment(Qt.AlignLeft)

        country_championship = hcm.get_country() + " - " + hcm.get_type_of_match()

        vbox.addLayout(top_hbox)
        vbox.addWidget(QLabel(country_championship))
        middle_hbox = QHBoxLayout()

        middle_hbox.addWidget(QLabel(
            'Cote ' + str(hcm.get_cote()) + ' - Bet price ' + str(hcm.get_bet_price()) + ' - Reward ' + str(
                hcm.get_reward())))
        middle_hbox.setAlignment(Qt.AlignLeft)
        vbox.addLayout(middle_hbox)

        score_label = QLabel('<h3>Scores</h3>')
        vbox.addWidget(score_label)
        bottom_hbox = QHBoxLayout()

        bottom_hbox.addWidget(
            QLabel('Event ' + str(hcm.get_current_score()) + ' - Predicted ' + str(hcm.get_predicted_score())))
        bottom_hbox.setAlignment(Qt.AlignLeft)
        vbox.addLayout(bottom_hbox)

        # Additional information can be added to the card

        wdg.setLayout(vbox)

        return wdg
