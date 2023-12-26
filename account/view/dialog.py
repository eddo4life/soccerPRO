from PyQt5.QtWidgets import QMessageBox


class ConfirmDialog:
    @classmethod
    def confirmed(cls, msg="Are you sure you want to proceed?"):
        # Create a QMessageBox
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("Confirmation Dialog")
        msg_box.setText(msg)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)

        # Process the result
        return msg_box.exec_() == QMessageBox.Yes
