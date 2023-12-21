from PyQt5.QtCore import QTime, QDate, QDateTime, Qt
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QWidget, QComboBox, QHBoxLayout, QDateEdit, QTimeEdit, QLineEdit, QPushButton, \
    QLabel, QVBoxLayout

from account.model.matchmanagementmodel import MatchManagementModel
from account.model.teamsdataloader import TeamsDataLoader
from labs.lab import Lab


class Matches(QWidget):
    def __init__(self):
        super().__init__()

        self.tdl = TeamsDataLoader()
        self.top_championship = self.tdl.get_top_championship()
        self.clubs = self.tdl.get_clubs()
        self.national_teams = self.tdl.get_national_teams()

        self.init_form()

    def init_form(self):

        # self.form1 = QFormLayout()
        # self.country_box = QComboBox()
        # # base on which competition... refactor later
        # self.country_box.addItems(list(self.national_teams.keys()))
        # self.championship_box = QComboBox()
        # self.championship_box.addItems(['Coupe du monde', 'Championnat', 'Eliminatoire', 'Amical'])
        #
        # self.form1.addRow("Pays", self.country_box)
        # self.championship_box.currentIndexChanged.connect(self.selected_championship)
        # self.country_box.currentIndexChanged.connect(self.selected_country)
        #
        # self.form1.addRow("Championat", self.championship_box)
        #
        # self.form1.addRow("Date", QDateEdit())
        # self.form1.addRow('Time', QTimeEdit())
        #
        # self.home_team = QComboBox()
        # self.home_team.addItems(self.national_teams.keys())
        # self.away_team = QComboBox()
        # self.away_team.addItems(list(self.national_teams.keys())[::-1])
        #
        # self.form1.addRow("Equipe receveuse", self.home_team)
        # self.form1.addRow("Equipe visiteuse", self.away_team)
        #
        # self.form1.addRow("Cote", QLineEdit("1.2"))
        # score = QLineEdit("0:0")
        # score.setEnabled(False)
        # self.form1.addRow("Score depart", score)
        # self.save_btn = QPushButton('Save event')
        # self.form1.addRow(self.save_btn)

        self.layout = QVBoxLayout()

        self.country_box = QComboBox()
        self.country_box.addItems(list(self.national_teams.keys()))

        self.championship_box = QComboBox()
        self.championship_box.addItems(['Coupe du monde', 'Championnat', 'Eliminatoire', 'Amical'])
        self.championship_box.currentIndexChanged.connect(self.selected_championship)

        self.layout.addWidget(QLabel("Pays"))
        self.layout.addWidget(self.country_box)

        self.layout.addWidget(QLabel("Championat"))
        self.layout.addWidget(self.championship_box)

        self.layout.addWidget(QLabel("Date"))
        self.date = QDateEdit()
        self.date.setDateTime(QDateTime.fromString(Lab.get_current_date(), Qt.ISODate))
        self.date.setDisabled(True)
        self.layout.addWidget(self.date)
        self.time = QTimeEdit()
        self.time.setTime(QTime.fromString(Lab.get_current_time(), "HH:mm"))
        self.time.setDisabled(True)
        self.layout.addWidget(QLabel("Time"))
        self.layout.addWidget(self.time)

        self.home_team = QComboBox()
        self.home_team.addItems(self.national_teams.keys())

        self.away_team = QComboBox()
        self.away_team.addItems(list(self.national_teams.keys())[::-1])

        self.layout.addWidget(QLabel("Equipe receveuse"))
        self.layout.addWidget(self.home_team)

        self.layout.addWidget(QLabel("Equipe visiteuse"))
        self.layout.addWidget(self.away_team)

        self.layout.addWidget(QLabel("Cote"))
        self.cote = QLineEdit("1,2")
        self.cote.setValidator(QDoubleValidator())
        self.layout.addWidget(self.cote)

        score = QLineEdit("0:0")
        score.setEnabled(False)
        self.layout.addWidget(QLabel("Score depart"))
        self.layout.addWidget(score)

        self.save_btn = QPushButton('Save event')
        self.layout.addWidget(self.save_btn)
        # ajust the the size
        Lab.set_size_policy_fixed(self.save_btn)
        self.save_btn.clicked.connect(self.save_event)

        background = QWidget()
        background.setStyleSheet(
            f"background-image: url(admin-bet.png); background-position: center;background-size: cover;")
        self.hbox = QHBoxLayout()
        self.hbox.addLayout(self.layout)
        self.hbox.addWidget(background)
        self.hbox.setStretchFactor(self.layout, 2)
        self.hbox.setStretchFactor(background, 1)
        self.setLayout(self.hbox)

    def revalidate_combobox(self, combobox, datas):
        if datas:
            # Clear the combobox
            combobox.clear()
            # Update the combobox with the new list
            combobox.addItems(datas)

    def selected_country(self):
        country = self.country_box.currentText()
        if country and self.championship_box.currentText().lower() == 'championnat':
            self.revalidate_clubs_base_on_selected_country(country)

    def revalidate_clubs_base_on_selected_country(self, country):
        try:
            self.revalidate_combobox(self.home_team, self.clubs[country])
            self.revalidate_combobox(self.away_team, self.clubs[country][::-1])
        except Exception as e:
            print('Error', str(e))

    def selected_championship(self):
        value = self.championship_box.currentText()
        if value == 'Championnat':
            # only for top 5 championship
            self.revalidate_combobox(self.country_box, Lab.get_flattened_values(self.top_championship))
            country = self.country_box.currentText()
            # home and  away team
            # base on the country...
            self.revalidate_clubs_base_on_selected_country(country)

        elif value == 'Coupe du monde':
            # all national teams (top 50)
            national_teams = list(self.national_teams.keys())
            self.revalidate_combobox(self.country_box, national_teams)
            # home and  away team
            self.revalidate_combobox(self.home_team, national_teams)
            self.revalidate_combobox(self.away_team, national_teams[::-1])
        elif value == 'Eliminatoire' or value == 'Amical':
            # all national teams (top 50) and clubs
            teams = Lab.get_flattened_values(self.clubs)
            teams.extend(list(self.national_teams.keys()))
            # home and  away team
            self.revalidate_combobox(self.home_team, teams)
            self.revalidate_combobox(self.away_team, teams[::-1])
            # country the match can be played
            self.revalidate_combobox(self.country_box, list(self.national_teams.keys()))
        else:
            print("Unknown match type")

    def save_event(self):
        championship = self.championship_box.currentText()
        country = self.country_box.currentText()
        away_team = self.away_team.currentText()
        home_team = self.home_team.currentText()
        cote = self.cote.text()

        date_match = Lab.get_current_date()
        heure_match = Lab.get_current_time()
        mmm = MatchManagementModel(championship, country, date_match, heure_match, away_team, home_team, cote, etat='N')
        mmm.save()
