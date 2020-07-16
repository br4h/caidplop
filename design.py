import sys
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTextEdit, QApplication, QWidget, QComboBox, QLabel

DATA = {'comfort': '', 'proximity': 0, 'area': 0}


class NetworkApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ok')
        self.setGeometry(200, 200, 800, 600)

        area_text = QTextEdit('bruh', self)
        area_text.move(20, 150)
        area_text.resize(200, 25)
        area_text.show()

        proximity_text = QTextEdit('bruh2', self)
        proximity_text.move(20, 200)
        proximity_text.resize(200, 25)
        proximity_text.textChanged.connect(self.on_proximity_changed)
        proximity_text.show()

        comfort_text = QComboBox(self)
        comfort_text.addItems(['Газ', 'Электричество', 'Вода',
                               'Газ,Электричество', 'Газ,Вода', 'Элетричество,Вода',
                               'Газ,Электричество,Вода'])
        comfort_text.move(20, 250)
        comfort_text.resize(200, 25)
        comfort_text.activated[str].connect(self.on_activated)
        comfort_text.show()

        price_text = QLabel(self)
        price_text.move(270, 130)
        price_text.resize(400, 200)
        price_text.setText('1231231263')
        price_text.setFont(QFont('SansSerif', 48))

        self.show()

    def on_activated(self, text):
        DATA['comfort'] = text
        print(DATA['comfort'])

    def on_proximity_changed(self):
        DATA['proximity'] = self.sender().text()
        print(DATA['proximity'])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    net_app = NetworkApp()
    sys.exit(app.exec_())