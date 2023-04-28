import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt5 import uic

class Aplicacion(QMainWindow):
    def __init__(self):
        super().__init__()

        self.inicializarGui()

    def inicializarGui(self):
        uic.loadUi('orCeph_demo.ui', self)
        self.show()

def main():
    app = QApplication(sys.argv)
    ventana = Aplicacion()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()