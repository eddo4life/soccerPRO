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
    layout = widget.layout()
    for i in range(layout.count()):
        try:
            item = layout.itemAt(i)
            if isinstance(item.widget(), QCheckBox) and item.widget().text().lower() == target_text:
                item.widget().setChecked(False)
        except Exception as e:
            print(f"An exception occurred: {str(e)}")


class Event(BaseWidget):
    def __init__(self):
        super().__init__()
        self.bcm_event_list = []
        self.bcm_selected_event_list = []

        for d in UserEventModel.load():  # gather data only for events
            self.add_widget(self.card(d))  # using the add_widget method from the super class BaseWidget

        # add both event and ticket horizontally to the main layout

        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self.scroll_area)

        main_layout.setStretchFactor(self.scroll_area, 2)  # give more space to the events

        # manage ticket class

        self.ticket = Ticket(self.bcm_selected_event_list)
        # add action for clearing the ticket
        self.ticket.clear_btn.clicked.connect(self.clear_ticket)

        # create a main layout for tickets
        main_layout_ticket = QVBoxLayout()
        main_layout_ticket.addWidget(self.ticket.scroll_area)
        main_layout_ticket.addLayout(self.ticket.add_buttons())
        # create a main widget for tickets
        ticket_widgets = QWidget()
        ticket_widgets.setLayout(main_layout_ticket)
        main_layout.addWidget(ticket_widgets)
        main_layout.setStretchFactor(ticket_widgets, 1)

        self.setLayout(main_layout)

    def card(self, dic):
        bcm = BetCardModel(dic)
        wdg = QWidget()
        wdg.setFixedHeight(200)
        # the main layout
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
        self.setStyleSheet(
            """
            QLineEdit{
            border:None;
            }
            """
        )
        score2.setFixedSize(80, 25)
        score2.setValidator(QIntValidator())
        score2.setPlaceholderText(bcm.get_away_team()[0:3] + "(0)")
        score_label = QLabel('Scores :')
        score_label.setFixedSize(55, 25)
        bottom_hbox.addWidget(score_label)
        bottom_hbox.addWidget(score1)
        bottom_hbox.addWidget(score2)
        bcm.set_score_home_team(score1)
        bcm.set_score_away_team(score2)
        bottom_hbox.setAlignment(Qt.AlignLeft)

        vbox.addLayout(bottom_hbox)
        # add unique checkbox to select a specific match
        chb = QCheckBox('Placer')
        vbox.addWidget(chb)
        wdg.setLayout(vbox)
        chb.clicked.connect(lambda: self.add_remove(chb, wdg, bcm))
        # set the widget as unique id for the id card model (no need perhaps...), if validation process is failed,
        # we show the card
        bcm.set_id_card(wdg)
        # # add that model to the list or card ('event')
        self.bcm_event_list.append(bcm)

        return wdg

    def add_remove(self, chb, card, bcm):

        if chb.isChecked():
            self.remove_widget(card)  # remove from the event list ('UI'), to avoid adding same event twice
            self.ticket.add_widget(card)  # add to the ticket
            self.bcm_selected_event_list.append(bcm)
        else:
            self.ticket.remove_widget(card)  # remove from the ticket list
            self.bcm_selected_event_list.remove(bcm)
            self.add_widget(card)  # add back to the event list

    def clear_ticket(self):
        # Remove and delete all items from the layout
        layout = self.ticket.layout
        while layout.count():
            widget = layout.takeAt(0).widget()
            if widget is not None:
                # search for the checkbox and unselect it
                unselect_checkbox(widget)
                self.add_widget(widget)


class Ticket(BaseWidget):
    def __init__(self, event_list):
        super().__init__()
        # gather an instance from the event, for the selected event list
        self.event_list = event_list
        self.clear_btn = QPushButton('clear')

    def add_buttons(self):
        validate_btn = QPushButton('validate')
        # add components to the layout
        hbox = QHBoxLayout()
        hbox.addWidget(self.clear_btn)
        hbox.addWidget(validate_btn)
        if not UserProfile.account_id:
            validate_btn.setEnabled(False)
        # add actions
        validate_btn.clicked.connect(self.validate)
        return hbox

    def validate(self):
        if self.event_list:
            BetModel(self.event_list).save()
        else:
            QMessageBox.warning(None, "", 'Veuillez placer au moins un paris!', QMessageBox.Ok)
