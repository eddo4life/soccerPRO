from PyQt5.QtWidgets import QWidget, QFormLayout, QComboBox, QHBoxLayout, QDateEdit, QTimeEdit, QLineEdit, QLabel

from account.model.matchmanagementmodel import MatchManagementModel


class Matches(QWidget):
    def __init__(self):
        super().__init__()

        self.match_model = MatchManagementModel()
        self.top_championship = self.match_model.get_top_championship()['top_uefa_championship']
        self.clubs = self.match_model.get_clubs()
        self.national_teams = self.match_model.get_national_teams()
        print('printing')
        print(self.national_teams)
        self.init_form()

    def init_form(self):
        self.form1 = QFormLayout()
        self.form2 = QFormLayout()
        self.hbox = QHBoxLayout()
        self.country_box = QComboBox()
        # base on which competition... refactor later
        self.country_box.addItems([nt for nt in self.national_teams.keys()])
        self.championship_box = QComboBox()
        self.championship_box.addItems(['Championnat', 'Coupe du monde', 'Eliminatoire', 'Amical'])

        self.championship_box.currentIndexChanged.connect(self.selected_championship)

        self.form1.addRow("Pays", self.country_box)
        self.form1.addRow("Championat", self.championship_box)

        self.form1.addRow("Date", QDateEdit())
        self.form1.addRow('Time', QTimeEdit())

        receiver_team = QComboBox()
        receiver_team.addItems([])
        visiter_team = QComboBox()
        visiter_team.addItems([])

        self.form1.addRow("Equipe receveuse", receiver_team)
        self.form1.addRow("Equipe visiteuse", visiter_team)

        self.form1.addRow("Cote", QLineEdit("1.2"))
        score = QLineEdit("0:0")
        score.setEnabled(False)
        self.form1.addRow("Score depart", score)

        self.hbox.addLayout(self.form1)
        self.hbox.addWidget(QLabel('a picture goes here.....................'))
        self.setLayout(self.hbox)

    def selected_championship(self):
        value = self.championship_box.currentText()
        if value == 'Championnat':
            print("Running tests for Championnat")
        elif value == 'Coupe du monde':
            print("Running tests for Coupe du monde")
        elif value == 'Eliminatoire':
            print("Running tests for Eliminatoire")
        elif value == 'Amical':
            print("Running tests for Amical")
        else:
            print("Unknown match type")
