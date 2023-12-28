from PyQt5.QtCore import QTime, QDateTime, Qt
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QWidget, QComboBox, QHBoxLayout, QDateEdit, QTimeEdit, QLineEdit, QPushButton, \
    QLabel, QVBoxLayout, QTableWidget, QAbstractItemView, QTableWidgetItem, QMessageBox

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
        # retrieve values from dict to list
        self.national_teams_list = list(self.national_teams.keys())
        self.clubs_list = Lab.get_flattened_values(self.clubs)
        # Initialize the status state
        self.status = self.status_list[0]

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
        self.status_box.currentIndexChanged.connect(self.analyze_status)
        self.away_team_box.currentIndexChanged.connect(self.set_club_or_national_team_to_away_box)
        self.home_team_box.currentIndexChanged.connect(self.set_club_or_national_team_to_away_box)

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
        self.__id_match = None  # An event without an ID is bound to save, not update.
        self.save_btn.setText('Save event')
        # Enable or disable components based on the provided parameter
        self.enable_components()

    def enable_components(self, is_enabled=True):
        """
        Enable or disable UI components based on the provided parameter.
        all access are granted if saving, but not for updating
        """
        self.championship_box.setEnabled(is_enabled)
        self.home_team_box.setEnabled(is_enabled)
        self.home_team_box.setEnabled(is_enabled)
        self.away_team_box.setEnabled(is_enabled)
        # The score should initially be 0:0 and not editable
        self.score.setEnabled(not is_enabled)

        # The date/time and country where the match is going to be played can be modified

        # self.date.setEnabled(is_enabled)
        # self.time.setEnabled(is_enabled)
        # self.country_box.setEnabled(is_enabled)

    def set_club_or_national_team_to_away_box(self):
        """
        Set the options for the away team based on the selected home team and championship.

        This method is responsible for dynamically updating the options in the away team combo box based on the
        selected home team and championship. It ensures that the away team options are updated appropriately based on
        whether the selected teams are clubs or national teams.

        Returns:
            None
        """
        # Block signals before proceeding with any update to avoid recursive calls
        self.championship_box.blockSignals(True)
        self.home_team_box.blockSignals(True)
        self.away_team_box.blockSignals(True)

        # Get the selected home and away team
        selected_home_team = self.home_team_box.currentText()
        selected_away_team = self.away_team_box.currentText()

        # Check if both home and away selected teams are not the same
        if selected_away_team != selected_home_team:
            # Get the currently selected championship
            championship = self.championship_box.currentText().lower()
            if championship == 'eliminatoire' or championship == 'amical':
                if selected_home_team in self.clubs_list:
                    # The team is a club
                    self.revalidate_combobox(self.away_team_box, self.clubs_list)
                else:
                    # It's probably a national team
                    self.revalidate_combobox(self.away_team_box, list(self.national_teams.keys()))
        else:
            # Show an information message to inform the user that the action is not allowed
            QMessageBox.information(None, "Action refusée",
                                    "Vous devez choisir deux équipes différentes.",
                                    QMessageBox.Ok)
            # Select two different teams to avoid conflicts
            self.home_team_box.setCurrentIndex(0)
            self.away_team_box.setCurrentIndex(1)

        # Enable back the signals
        self.championship_box.blockSignals(False)
        self.home_team_box.blockSignals(False)
        self.away_team_box.blockSignals(False)

    def analyze_status(self):
        """
        Analyze the status change and handle restrictions.

        This method is responsible for analyzing the change in status from a previous status to a new one.
        If the new status is 'S' (Supprimer) and the previous status was either 'E' (Encours) or 'N'
        (Non Encore Joue), it displays an information message to inform the user that deletion
        is not allowed for events that are either in progress or not yet played. It also reverts the status back
        to the previous one in the GUI element (status_box).

        If the new status is 'N' (Non Encore Joue) and the previous status was 'E' (Encours), it displays an
        information message to inform the user that the action is not allowed for events that have already started.

        Returns:
            None
        """
        # Get the previous and current status
        previous_status = self.status
        current_status = self.status_box.currentText()

        # Check if the current status is 'S' (Supprimer)
        if current_status == 'S':
            # Check if the previous status was 'E' (Encours) or 'N' (Non Encore Joue)
            if previous_status == 'E' or previous_status == 'N':
                # Show an information message to inform the user that deletion is not allowed
                QMessageBox.information(None, "Suppression refusée",
                                        "Vous pouvez supprimer un événement soit terminé soit annulé.", QMessageBox.Ok)

                # Select back the previous status in the GUI element (status_box)
                index = self.status_box.findText(previous_status)
                if index != -1:
                    self.status_box.setCurrentIndex(index)
        elif current_status == 'N':
            # Check if the previous status was 'E' (Encours)
            if previous_status == 'E':
                # Show an information message to inform the user that the action is not allowed
                QMessageBox.information(None, "Action refusée",
                                        "Vous pouvez mettre en mode (non encore joué) un événement qui a été déjà commencé.",
                                        QMessageBox.Ok)

                # Select back the previous status in the GUI element (status_box)
                index = self.status_box.findText(previous_status)
                if index != -1:
                    self.status_box.setCurrentIndex(index)

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
        self.home_team_box.blockSignals(True)
        self.away_team_box.blockSignals(True)

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

            # home and away team
            self.revalidate_combobox(self.away_team_box, self.clubs_list[::-1])
            # extend national national teams to clubs
            self.revalidate_combobox(self.home_team_box, self.clubs_list + list(self.national_teams.keys()))
            # country the match can be played
            self.revalidate_combobox(self.country_box, list(self.national_teams.keys()))

        self.country_box.blockSignals(False)  # Re-enable signals
        self.home_team_box.blockSignals(False)
        self.away_team_box.blockSignals(False)

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
        mmm = MatchManagementModel(self.__id_match, championship, country, date_match, heure_match, away_team,
                                   home_team,
                                   self.cote.text(), self.score.text(), etat)
        if self.__id_match:
            if etat == 'A':
                mmm.cancel_match_and_refund()
            elif etat == 'T':
                mmm.refund_users_if_scores_match()
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
            self.__id_match = id_item.text()
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
            self.status = status_item.text().upper()
            index = self.status_box.findText(self.status)
            if index != -1:
                self.status_box.blockSignals(True)
                self.status_box.setCurrentIndex(index)
                self.status_box.blockSignals(False)
