import sys, re
from PyQt5 import uic, QtWidgets
from NeuroLand import domofond_parser


#  https://www.domofond.ru/uchastokzemli-na-prodazhu-skoropuskovskiy-1648805439

class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi('ver2.ui', self)
        self.link = str()
        self.data = str()

    def get_link(self):
        try:
            self.data = domofond_parser.get_data_by_link(self.lineEdit.text())
            self.data = list([x.split(':')[1].replace(',', '.').replace(' ', '') for x in self.data.split(';')[:-1]])
            print(self.data)
            self.lineEdit_4.setText(f'{self.data[0][:-3]}')
            self.lineEdit_3.setText(f'{self.data[1][:-2]}')

            self.doubleSpinBox_1.setValue(float(self.data[-2]))  # Транспорт
            self.doubleSpinBox_2.setValue(float(self.data[3]))  # Экология
            self.doubleSpinBox_3.setValue(float(self.data[5]))  # ЖКХ
        except Exception as e:
            print(e)

    # '10сот', '4км', '570000', Эколгоия: 3.1, Чистота: 2.9, ЖКХ: 2.7, Соседи: 3.7,
    # Условия для детей: 3.5, Спорт и отдых: 3.1, Магазины: 4.2, Транспорт: 2.9, Безопасность: 3.2
    def initUI(self):
        self.setFixedSize(800, 600)
        self.setWindowTitle("NeuroLand")
        # self.pushButton_4.clicked.connect(lambda: self.get_link())
        self.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    root = UI()
    root.initUI()

    app.exec_()
