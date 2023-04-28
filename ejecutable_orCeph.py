import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
from orCeph_demo import Ui_DibujoPunto

class Aplicacion(QMainWindow):
    def __init__(self):
        super().__init__()
        self.inicializarGui()

    def inicializarGui(self):
        self.ui = Ui_DibujoPunto()
        self.ui.setupUi(self)

        self.posicion = [0,0]

        self.show()

    def mousePressEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.posicion[0] = event.pos().x()
            self.posicion[1] = event.pos().y()

            self.update()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        pincel = QPen(Qt.black, 7)

        painter.setPen(pincel)
        painter.drawPoint(self.posicion[0], self.posicion[1])
        painter.end()



def main():
    app = QApplication(sys.argv)
    ventana = Aplicacion()

    sys.exit(app.exec_())

if(__name__ == "__main__"):
    main()
