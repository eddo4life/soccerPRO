from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QPushButton, QLineEdit, QMessageBox
from PyQt5.QtWidgets import QWidget, QCheckBox, QLabel, QVBoxLayout, QHBoxLayout

from account.model.betcardmodel import BetCardModel
from account.model.betmodel import BetModel
from account.model.usereventmodel import UserEventModel
from account.view.user.basewidget import BaseWidget
from account.view.user.profile.userprofile import UserProfile


def unselect_checkbox(widget, target_text='placer'):
    """
    Unselects a checkbox with a specified target text within a given widget's layout.

    Parameters:
    - widget: QWidget
        The widget containing the layout with checkboxes.
    - target_text: str, optional (default='placer')
        The target text of the checkbox to be unselected.

    Returns:
    None
    """
    layout = widget.layout()
    for i in range(layout.count()):
        try:
            item = layout.itemAt(i)
            if isinstance(item.widget(), QCheckBox) and item.widget().text().lower() == target_text:
                item.widget().setChecked(False)
        except Exception as e:
            print(f"An exception occurred: {str(e)}")


class Event(BaseWidget):
    def __init__(self, home):
        """
        Initializes the Event widget, displaying a list of events with associated information.

        Parameters:
        - home: QWidget
            The main window or parent widget.

        Returns:
        None
        """
        super().__init__()
        self.bcm_selected_event_list = []

        # Populate the widget with events
        for d in UserEventModel.load():
            self.add_widget(self.card(d))

        # Horizontal layout for events and tickets
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self.scroll_area)
        main_layout.setStretchFactor(self.scroll_area, 2)

        # Ticket management
        self.ticket = Ticket(self.bcm_selected_event_list, home)
        self.ticket.clear_btn.clicked.connect(self.clear_ticket)

        # Vertical layout for tickets
        main_layout_ticket = QVBoxLayout()
        main_layout_ticket.addWidget(self.ticket.scroll_area)
        main_layout_ticket.addLayout(self.ticket.add_buttons())

        ticket_widgets = QWidget()
        ticket_widgets.setLayout(main_layout_ticket)
        main_layout.addWidget(ticket_widgets)
        main_layout.setStretchFactor(ticket_widgets, 1)

        self.setLayout(main_layout)

    def card(self, dic):
        """
        Creates and returns a widget representing an event card with relevant information.

        Parameters:
        - dic: dict
            The dictionary containing event data.

        Returns:
        QWidget
        """
        bcm = BetCardModel(dic)
        wdg = QWidget()
        wdg.setFixedHeight(200)

        # Main layout
        vbox = QVBoxLayout()
        top_hbox = QHBoxLayout()

        teams = bcm.get_home_team() + " - " + bcm.get_away_team()
        teams_label = QLabel('<h2>' + teams + '</h2>')
        time_label = QLabel("(" + bcm.get_time() + ")")

        top_hbox.addWidget(teams_label)
        top_hbox.addWidget(time_label)
        top_hbox.setAlignment(Qt.AlignLeft)

        country_championship = bcm.get_country() + " - " + bcm.get_type_of_match()

        vbox.addLayout(top_hbox)
        vbox.addWidget(QLabel(country_championship))
        middle_hbox = QHBoxLayout()
        middle_hbox.addWidget(QLabel('cote ' + str(bcm.get_cote())))

        amount_edit = QLineEdit()
        amount_edit.setPlaceholderText('montant')
        amount_edit.setFixedSize(80, 25)
        validator = QDoubleValidator()
        amount_edit.setValidator(validator)
        middle_hbox.addWidget(amount_edit)
        bcm.set_amount(amount_edit)
        vbox.addLayout(middle_hbox)

        bottom_hbox = QHBoxLayout()
        score1 = QLineEdit()
        score1.setValidator(QIntValidator())
        score1.setPlaceholderText(bcm.get_home_team()[0:3] + "(0)")
        score1.setFixedSize(80, 25)

        score2 = QLineEdit()
        score2.setValidator(QIntValidator())
        score2.setPlaceholderText(bcm.get_away_team()[0:3] + "(0)")
        score2.setFixedSize(80, 25)
        score_label = QLabel('Scores :')
        score_label.setFixedSize(55, 25)

        bottom_hbox.addWidget(score_label)
        bottom_hbox.addWidget(score1)
        bottom_hbox.addWidget(score2)
        bcm.set_score_home_team(score1)
        bcm.set_score_away_team(score2)
        bottom_hbox.setAlignment(Qt.AlignLeft)

        vbox.addLayout(bottom_hbox)

        # Add unique checkbox to select a specific match
        chb = QCheckBox('Placer')
        vbox.addWidget(chb)
        wdg.setLayout(vbox)
        chb.clicked.connect(lambda: self.add_remove(chb, wdg, bcm))

        return wdg

    def add_remove(self, chb, card, bcm):
        """
        Adds or removes an event card based on checkbox state, and updates the ticket.

        Parameters:
        - chb: QCheckBox
            The checkbox associated with the event card.
        - card: QWidget
            The event card widget.
        - bcm: BetCardModel
            The BetCardModel object associated with the event card.

        Returns:
        None
        """
        if chb.isChecked():
            self.remove_widget(card)
            self.ticket.add_widget(card)
            self.bcm_selected_event_list.append(bcm)
        else:
            self.ticket.remove_widget(card)
            self.bcm_selected_event_list.remove(bcm)
            self.add_widget(card)

    def clear_ticket(self):
        """
        Clears the selected events in the ticket.

        Returns:
        None
        """
        self.bcm_selected_event_list.clear()
        layout = self.ticket.layout
        while layout.count():
            widget = layout.takeAt(0).widget()
            if widget is not None:
                unselect_checkbox(widget)
                self.add_widget(widget)


class Ticket(BaseWidget):
    def __init__(self, event_list, home):
        """
        Initializes the Ticket widget.

        Parameters:
        - event_list: list
            List of selected events.
        - home: QWidget
            The main window or parent widget.

        Returns:
        None
        """
        super().__init__()
        self.home = home  # Instance from the home page to update the sold label
        self.event_list = event_list
        self.clear_btn = QPushButton('Clear')

    def add_buttons(self):
        """
        Creates and returns a layout with buttons for the ticket.

        Returns:
        QHBoxLayout
        """
        validate_btn = QPushButton('Validate')
        hbox = QHBoxLayout()
        hbox.addWidget(self.clear_btn)
        hbox.addWidget(validate_btn)

        # Disable the "Validate" button if the user is not logged in
        if not UserProfile.account_id:
            validate_btn.setEnabled(False)

        # Connect actions to buttons
        validate_btn.clicked.connect(self.validate)
        return hbox

    def validate(self):
        """
        Validates and saves the selected events in the ticket.

        Returns:
        None
        """
        if self.event_list:
            if UserProfile.user_status[0] == 'A':  # Check if the account is active
                res = BetModel().save_events(self.event_list)
                if type(res) == bool:
                    self.home.set_sold(UserProfile.user_fund)
                    QMessageBox.information(None, "Success", 'Paris effectué avec succès', QMessageBox.Ok)
                    # Revalidate the history tab
                    self.home.revalidate_history_tab()
                else:
                    QMessageBox.warning(None, "Echec", res, QMessageBox.Ok)
            else:
                QMessageBox.warning(None, "Compte inactif", 'Veuillez réactiver votre compte!', QMessageBox.Ok)
        else:
            QMessageBox.warning(None, "Panier vide", 'Veuillez placer au moins un pari!', QMessageBox.Ok)
