import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGridLayout, QPushButton, QWidget, QLineEdit)
from PyQt5.QtCore import Qt


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setGeometry(100, 100, 300, 400)

        self.display = QLineEdit(self)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFixedHeight(40)

        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(self.display, 0, 0, 1, 4)

        # Button labels
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3)
        ]

        # Add buttons to the grid
        for label, row, col in buttons:
            button = QPushButton(label, self)
            button.setFixedSize(60, 60)
            button.clicked.connect(self.on_button_click)
            self.grid_layout.addWidget(button, row, col)

        self.clear_button = QPushButton("C", self)
        self.clear_button.setFixedSize(60, 60)
        self.clear_button.clicked.connect(self.clear)
        self.grid_layout.addWidget(self.clear_button, 5, 0)

        self.parent_widget = QWidget(self)
        self.parent_widget.setLayout(self.grid_layout)
        self.setCentralWidget(self.parent_widget)

    def on_button_click(self):
        sender = self.sender()
        text = sender.text()

        current_text = self.display.text()

        if text == "=":
            try:
                result = str(eval(current_text))
                self.display.setText(result)
            except Exception:
                self.display.setText("Error")
        else:
            new_text = current_text + text
            self.display.setText(new_text)

    def clear(self):
        self.display.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec_())
