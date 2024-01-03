import json
import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFormLayout, QDialog, QLineEdit, QTextEdit, QPushButton, QHBoxLayout, QLabel, \
    QTabWidget, QVBoxLayout, QWidget, QMessageBox

from database.connection import DatabaseConnector


class Configuration(QDialog):
    def __init__(self):
        super().__init__()
        self.setModal(True)
        self.setWindowTitle('Config')
        self.matches = 'scripts/xparyaj_matches.sql'
        self.paryaj = 'scripts/xparyaj_pariage.sql'
        self.parieur = 'scripts/xparyaj_parieur.sql'
        self.notice = ''
        self.init_ui()

    def init_ui(self):
        # Create a tab widget to hold multiple tabs
        tab_widget = QTabWidget(self)

        # Add tabs for Queries and Connection Fields
        tab_widget.addTab(self.create_connection_tab(), 'Connection Fields')
        tab_widget.addTab(self.create_queries_tab(), 'Tables(struct)')

        # Set the main layout as a vertical layout containing the tab widget
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(tab_widget)

        # Set fixed size and prevent resizing
        self.setFixedSize(self.sizeHint())

    def create_queries_tab(self):
        # Create a QWidget for the Queries tab
        queries_tab = QWidget()

        # Create a layout for the Queries tab
        queries_layout = QVBoxLayout(queries_tab)

        # Create a QTextEdit for displaying queries
        self.queries_text_edit = QTextEdit()
        queries_layout.addWidget(self.queries_text_edit)
        font = QFont()
        font.setPointSize(10)  # adjust the font size
        self.queries_text_edit.setFont(font)
        # Make the QTextEdit non-editable
        self.queries_text_edit.setReadOnly(True)
        # Append text to QTextEdit using read_sql_file
        self.append_text(self.matches)
        self.append_text(self.paryaj)
        self.append_text(self.parieur)
        self.notice_label = QLabel()
        if len(self.notice) == 0:
            self.notice_label.setText('Notice: 100% OK!')
            self.notice_label.setStyleSheet('color:green')
        else:
            self.notice_label.setText('Notice : ' + self.notice + 'The application may not function correctly.')
            self.notice_label.setStyleSheet('color:red')
        queries_layout.addWidget(self.notice_label)

        return queries_tab

    def create_connection_tab(self):
        # Create a QWidget for the Connection Fields tab
        connection_tab = QWidget()

        # Create a layout for the Connection Fields tab
        connection_layout = QFormLayout(connection_tab)

        connection_layout.setSpacing(30)

        # Input fields for host, user, password, and database
        self.host_input = QLineEdit('localhost')
        connection_layout.addRow('Host', self.host_input)

        self.user_input = QLineEdit('root')
        connection_layout.addRow('User', self.user_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText('mysql password (if any)')
        connection_layout.addRow('Password', self.password_input)

        self.database_input = QLineEdit()
        self.database_input.setPlaceholderText('Database name')
        connection_layout.addRow('Database', self.database_input)

        # Status label to display connection status
        self.status_label = QLabel()
        connection_layout.addRow('Status :', self.status_label)

        # Create a horizontal box layout for buttons
        hbox_layout = QHBoxLayout()

        # Buttons for testing, saving, clearing, connecting, and canceling
        self.test_button = QPushButton('Tester')
        self.test_button.clicked.connect(self.test_connection)
        hbox_layout.addWidget(self.test_button)

        self.save_button = QPushButton('Sauvegarder')
        self.save_button.clicked.connect(self.save_configuration)
        hbox_layout.addWidget(self.save_button)

        self.clear_button = QPushButton('Clear')
        self.clear_button.clicked.connect(self.clear_fields)
        hbox_layout.addWidget(self.clear_button)

        self.connect_button = QPushButton('Connect')
        self.connect_button.clicked.connect(self.connect_to_database)
        hbox_layout.addWidget(self.connect_button)

        self.cancel_button = QPushButton('Exit')
        self.cancel_button.clicked.connect(self.close)
        hbox_layout.addWidget(self.cancel_button)

        connection_layout.addRow(hbox_layout)

        return connection_tab

    def test_connection(self):
        conn = DatabaseConnector(self.retrieve_input_data())
        text = conn.connect(False)
        self.status_label.setStyleSheet("color: green;" if 'success' in text.lower() else "color: red;")
        self.status_label.setText(text)

    def retrieve_input_data(self):
        # Get data from input fields
        host = self.host_input.text()
        user = self.user_input.text()
        password = self.password_input.text()
        database = self.database_input.text()

        # Create a dictionary with the configuration data
        return {
            "host": host,
            "user": user,
            "password": password,
            "database": database
        }

    def save_configuration(self):
        # Save the configuration data to a JSON file

        try:
            with open('config.json', 'w') as json_file:
                json.dump(self.retrieve_input_data(), json_file, indent=4)
            self.status_label.setText("Config data successfully saved to config.json")
        except IOError as e:
            self.status_label.setText(f"Error writing to config.json: {e}")
            sys.exit()
        except Exception as e:
            self.status_label.setText(f"An unexpected error occurred: {e}")
            sys.exit()

    def read_sql_file(self, file_path):
        try:
            with open(file_path, 'r') as sql_file:
                return sql_file.read().strip()

        except IOError as e:
            self.notice += f"Failed to read the file '{file_path}': {str(e)}\n"

    def append_text(self, file_path):
        content = self.read_sql_file(file_path)
        if content is not None:
            self.queries_text_edit.append(content)

    def clear_fields(self):
        # Clear all input fields and status label
        self.host_input.setText('localhost')
        self.user_input.setText('root')
        self.password_input.clear()
        self.database_input.clear()
        self.status_label.clear()

    def connect_to_database(self):
        """
        Connects to the database using the input data retrieved by the `retrieve_input_data` method.

        Raises:
            QMessageBox: Displays an information message if the connection and table creation are successful.
                          Displays a warning message if an error occurs during the process.

        Returns:
            None
        """
        conn = DatabaseConnector(self.retrieve_input_data())
        conn.connect(False)
        if conn.get_con():
            try:
                with conn.get_con().cursor(prepared=True) as cursor:
                    cursor.execute('DROP TABLE IF EXISTS matches;')
                    cursor.execute(self.read_sql_file(self.matches))

                    cursor.execute('DROP TABLE IF EXISTS pariage;')
                    cursor.execute(self.read_sql_file(self.paryaj))

                    cursor.execute('DROP TABLE IF EXISTS parieur;')
                    cursor.execute(self.read_sql_file(self.parieur))

                    conn.get_con().commit()
                    # Launch the application again
                    QMessageBox.information(None, "Success'", "Veuillez sauvegarder et relancer l'application!",
                                            QMessageBox.Ok)
            except Exception as err:
                QMessageBox.warning(None, "Error", err.__str__(), QMessageBox.Ok)
            finally:
                conn.disconnect()
        else:
            self.status_label.setText('Veuillez vous connecter a une base!')
