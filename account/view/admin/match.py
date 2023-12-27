from PyQt5.QtCore import QTime, QDateTime, Qt
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QWidget, QComboBox, QHBoxLayout, QDateEdit, QTimeEdit, QLineEdit, QPushButton, \
    QLabel, QVBoxLayout, QTableWidget, QAbstractItemView, QTableWidgetItem

from account.model.matchmanagementmodel import MatchManagementModel
from account.model.teamsdataloader import TeamsDataLoader
from labs.lab import Lab


class Matches(QWidget):
    def __init__(self):
        """
        Constructor for the Matches widget.
        """
        super().__init__()

        # Lists of championship types and match statuses
        self.championship_list = ['Coupe du monde', 'Championnat', 'Eliminatoire', 'Amical']
        self.status_list = ['N', 'E', 'T', 'A', 'S']

        # Initialize TeamsDataLoader to load data about teams
        self.tdl = TeamsDataLoader()
        self.top_championship = self.tdl.get_top_championship()
        self.clubs = self.tdl.get_clubs()
        self.national_teams = self.tdl.get_national_teams()
        self.national_teams_list = list(self.national_teams.keys())

        # Initialize the form
        self.init_form()

    def init_form(self):
        """
        Initialize the UI elements for the Matches widget.
        """
        # Layout setup
        self.layout = QVBoxLayout()

        # Combo boxes for selecting country, championship, home team, away team, and match status
        self.country_box = QComboBox()
        self.championship_box = QComboBox()
        self.home_team_box = QComboBox()
        self.away_team_box = QComboBox()
        self.status_box = QComboBox()

        # Date and time input fields
        self.layout.addWidget(QLabel("Pays"))
        self.layout.addWidget(self.country_box)
        self.layout.addWidget(QLabel("Championat"))
        self.layout.addWidget(self.championship_box)
        self.layout.addWidget(QLabel("Date"))
        self.date = QDateEdit()
        self.layout.addWidget(self.date)
        self.time = QTimeEdit()
        self.layout.addWidget(QLabel("Time"))
        self.layout.addWidget(self.time)

        # Home team and away team selection
        self.layout.addWidget(QLabel("Equipe receveuse"))
        self.layout.addWidget(self.home_team_box)
        self.layout.addWidget(QLabel("Equipe visiteuse"))
        self.layout.addWidget(self.away_team_box)

        # Cote (odds), score, and match status input fields
        self.layout.addWidget(QLabel("Cote"))
        self.cote = QLineEdit("1,2")
        self.cote.setValidator(QDoubleValidator())
        self.layout.addWidget(self.cote)

        self.score = QLineEdit("0:0")
        self.score.setEnabled(False)
        self.layout.addWidget(QLabel("Score"))
        self.layout.addWidget(self.score)

        self.layout.addWidget(QLabel("Etat"))
        self.layout.addWidget(self.status_box)

        # Button layout for Clear and Save buttons
        buttons_layout = QHBoxLayout()
        self.clear_btn = QPushButton('Clear')
        buttons_layout.addWidget(self.clear_btn)
        self.save_btn = QPushButton()
        buttons_layout.addWidget(self.save_btn)

        self.layout.addLayout(buttons_layout)

        # Set up button click events
        Lab.set_size_policy_fixed(self.save_btn)
        self.save_btn.clicked.connect(self.save_event)
        Lab.set_size_policy_fixed(self.clear_btn)
        self.clear_btn.clicked.connect(self.init_fields)
        # Set up combobox currentIndexChanged events
        self.championship_box.currentIndexChanged.connect(self.selected_championship)

        # Main layout
        self.hbox = QHBoxLayout()
        self.hbox.addLayout(self.layout)
        self.hbox.addWidget(self.show_event())
        self.hbox.setStretchFactor(self.layout, 1)
        self.hbox.setStretchFactor(self.table, 4)
        self.setLayout(self.hbox)

        # Initialize form fields
        self.init_fields()

    def init_fields(self):
        """
        Initialize the form fields to default values.
        """
        # Initialize match status combo box
        self.revalidate_combobox(self.status_box, self.status_list)
        # Initialize championship, which will automatically initialize other fields due to the connected signal
        self.revalidate_combobox(self.championship_box, self.championship_list)
        # Set default date and time
        self.date.setDateTime(QDateTime.fromString(Lab.get_current_date(), Qt.ISODate))
        self.time.setTime(QTime.fromString(Lab.get_current_time(), "HH:mm"))
        # Set default text values for odds and score
        self.cote.setText('1.2')
        self.score.setText('0:0')
        self.id_match = None  # An event without an ID is bound to save, not update.
        self.save_btn.setText('Save event')
        # Enable or disable components based on the provided parameter
        self.enable_components()

    def enable_components(self, is_enabled=True):
        """
        Enable or disable UI components based on the provided parameter.
        """
        self.championship_box.setEnabled(is_enabled)
        self.home_team_box.setEnabled(is_enabled)
        self.country_box.setEnabled(is_enabled)
        self.home_team_box.setEnabled(is_enabled)
        self.away_team_box.setEnabled(is_enabled)
        # The score should initially be 0:0 and not editable
        self.score.setEnabled(not is_enabled)
        self.date.setEnabled(is_enabled)
        self.time.setEnabled(is_enabled)

    def revalidate_combobox(self, combobox, datas):
        """
        Clear and update a combo box with new data.

        Args:
            combobox (QComboBox): The combo box to update.
            datas (list): The new data to populate in the combo box.
        """
        if datas:
            # Clear the combobox
            combobox.clear()
            # Update the combobox with the new list
            combobox.addItems(datas)

    def selected_country(self):
        """
        Slot method called when the country selection changes.
        """
        country = self.country_box.currentText()
        if country and self.championship_box.currentText().lower() == 'championnat':
            self.revalidate_clubs_base_on_selected_country(country)

    def revalidate_clubs_base_on_selected_country(self, country):
        """
        Revalidate home and away team combo boxes based on the selected country.

        Args:
            country (str): The selected country.
        """
        try:
            self.revalidate_combobox(self.home_team_box, self.clubs[country])
            self.revalidate_combobox(self.away_team_box, self.clubs[country][::-1])
        except Exception as e:
            print('Error', str(e))

    def selected_championship(self):
        """
        Slot method called when the championship selection changes.
        """
        self.country_box.blockSignals(True)  # Disable signals temporarily
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
            self.revalidate_combobox(self.country_box, self.national_teams_list)
            # home and  away team
            self.revalidate_combobox(self.home_team_box, self.national_teams_list)
            self.revalidate_combobox(self.away_team_box, self.national_teams_list[::-1])
        elif value == 'Eliminatoire' or value == 'Amical':
            # all national teams (top 50) and clubs
            teams = Lab.get_flattened_values(self.clubs)
            teams.extend(list(self.national_teams.keys()))
            # home and  away team
            self.revalidate_combobox(self.home_team_box, teams)
            self.revalidate_combobox(self.away_team_box, teams[::-1])
            # country the match can be played
            self.revalidate_combobox(self.country_box, list(self.national_teams.keys()))
        else:
            print("Unknown match type")
        self.country_box.blockSignals(False)  # Re-enable signals

    def save_event(self):
        """
        Save or update a match event based on the form data.
        """
        championship = self.championship_box.currentText()
        country = self.country_box.currentText()
        away_team = self.away_team_box.currentText()
        home_team = self.home_team_box.currentText()

        etat = self.status_box.currentText()
        date_match = Lab.get_current_date()
        heure_match = Lab.get_current_time()
        mmm = MatchManagementModel(self.id_match, championship, country, date_match, heure_match, away_team, home_team,
                                   self.cote.text(), self.score.text(), etat)
        if self.id_match:
            mmm.update()
        else:
            mmm.save()
        # clear/init the fields
        self.init_fields()
        self.load()

    def show_event(self):
        """
        Create and return a QTableWidget for displaying match events.

        Returns:
            QTableWidget: The table widget for displaying match events.
        """
        self.table = QTableWidget()
        self.table.clicked.connect(self.handle_table_click)
        # Set the table as not editable
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        header = ["ID", "TYPE DE MATCH", "PAYS", "DATE", "HEURE", "EQUPE RECEVEUSE", "EQUIPE VISITEUSE", "COTE",
                  "SCORE", "ETAT"]
        self.table.setColumnCount(len(header))
        self.table.setAlternatingRowColors(True)
        self.table.setHorizontalHeaderLabels(header)
        self.table.verticalHeader().setVisible(False)
        # load data to the table
        self.load()

        return self.table

    def load(self):
        """
        Load match data into the table.
        """
        # clearing the table
        self.table.setRowCount(0)
        # filling the table
        for row_number, row_data in enumerate(MatchManagementModel.load()):
            self.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                item = QTableWidgetItem(str(column_data))
                self.table.setItem(row_number, column_number, item)

    def handle_table_click(self, item):
        """
        Handle the click event on the table. Populate form fields based on the selected row.

        Args:
            item (QTableWidgetItem): The selected item in the table.
        """
        selected_row = item.row()

        #  ["ID", "TYPE DE MATCH", "PAYS", "DATE", "HEURE", "EQUPE RECEVEUSE", "EQUIPE VISITEUSE", "COTE",
        #                   "SCORE", "ETAT"]
        if selected_row >= 0 and self.table.item(selected_row, 9).text().lower() != 't':
            #  enabling or disabling components
            self.enable_components(False)
            # retrieve the id
            id_item = self.table.item(selected_row, 0)
            self.id_match = id_item.text()
            type_match_item = self.table.item(selected_row, 1)
            country_item = self.table.item(selected_row, 2)
            date_item = self.table.item(selected_row, 3)
            time_item = self.table.item(selected_row, 4)
            home_team_item = self.table.item(selected_row, 5)
            away_team_item = self.table.item(selected_row, 6)
            cote_item = self.table.item(selected_row, 7)
            score_item = self.table.item(selected_row, 8)
            status_item = self.table.item(selected_row, 9)
            # change save_btn's text from Save to Update
            self.save_btn.setText('Update event')

            # select the country
            country_match = country_item.text().capitalize()
            index = self.country_box.findText(country_match)
            if index != -1:
                self.country_box.setCurrentIndex(index)

            # select the championship
            type_match = type_match_item.text().capitalize()
            index = self.championship_box.findText(type_match)
            if index != -1:
                self.championship_box.setCurrentIndex(index)

            # home_team
            home_team = home_team_item.text().capitalize()
            index = self.home_team_box.findText(home_team)
            if index != -1:
                self.home_team_box.setCurrentIndex(index)

            # away_team
            away_team = away_team_item.text().capitalize()
            index = self.away_team_box.findText(away_team)
            if index != -1:
                self.away_team_box.setCurrentIndex(index)

            # date
            self.date.setDateTime(QDateTime.fromString(date_item.text(), Qt.ISODate))
            # time
            # to handle both 0-9 and 10-24hr format
            self.time.setTime(QTime.fromString(time_item.text(), "HH:mm:ss"))
            self.time.setTime(QTime.fromString(time_item.text(), "H:mm:ss"))
            # cote
            self.cote.setText(cote_item.text())
            # score
            self.score.setText(score_item.text())
            # status
            index = self.status_box.findText(status_item.text().upper())
            if index != -1:
                self.status_box.setCurrentIndex(index)
