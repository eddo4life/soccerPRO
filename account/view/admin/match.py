from PyQt5.QtWidgets import QWidget, QFormLayout, QComboBox, QHBoxLayout, QDateEdit, QTimeEdit, QLineEdit, QLabel


class Matches(QWidget):
    def __init__(self):
        super().__init__()
        self.init_form()

    def init_form(self):
        self.form1 = QFormLayout()
        self.form2 = QFormLayout()
        self.hbox = QHBoxLayout()
        self.country_box = QComboBox()
        self.country_box.addItems(['Angleterre', 'Espagne', 'Italy', 'Allemagne', 'France'])
        self.championship_box = QComboBox()
        self.championship_box.addItems(['Championnat', 'coupe du monde', 'éliminatoire', 'amical'])

        self.form1.addRow("Pays", self.country_box)
        self.form1.addRow("Championat", self.championship_box)

        self.form1.addRow("Date", QDateEdit())
        self.form1.addRow('Time', QTimeEdit())

        receiver_team = QComboBox()
        receiver_team.addItems(['Angleterre', 'Espagne', 'Italy', 'Allemagne', 'France'])
        visiter_team = QComboBox()
        visiter_team.addItems(['Angleterre', 'Espagne', 'Italy', 'Allemagne', 'France'])

        self.form1.addRow("Equipe receveuse", receiver_team)
        self.form1.addRow("Equipe visiteuse", visiter_team)

        self.form1.addRow("Cote", QLineEdit("1.2"))
        score=QLineEdit("0:0")
        score.setEnabled(False)
        self.form1.addRow("Score depart", score)

        self.hbox.addLayout(self.form1)
        self.hbox.addWidget(QLabel('a picture goes here.....................'))
        self.setLayout(self.hbox)
