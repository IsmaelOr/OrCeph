import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
from orCeph_interfaz import Ui_MainWindow
from functools import partial

class Aplicacion(QMainWindow):
    def __init__(self, width, height):
        super().__init__()
        
        self.inicializar_gui(width, height)

    def inicializar_gui(self, width, height):
        print(width, height)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self, width, height)
        
        self.ui.btn_buscar.clicked.connect(self.open_image)

        self.puntosSteinerList = list(self.ui.puntosSteiner.keys())

        for i, arg in enumerate(self.puntosSteinerList):
            self.ui.buttonList[i].clicked.connect(partial(self.drawPoint, arg, i))
        
        self.ui.btn_calcular.clicked.connect(self.calcularSteiner)

        self.show()

    
    def calcularSteiner(self):
        print(f'Puntos Steiner: \n {self.ui.puntosSteiner}')

    def drawPoint(self,label, num_button):
        self.ui.photo.setPoint(label, num_button,self.ui)
        
    
    def open_image(self, filename=None):
        if not filename:
            filename, _ = QFileDialog.getOpenFileName(self, 'Select Photo', QDir.currentPath(), "Images (*.png *.jpg *.jpeg)")
            if not filename:
                return
            info = QFileInfo(filename)
            image_info = QImageReader(filename)
            medidas = image_info.size()
            width = medidas.width()
            height = medidas.height()
            print(width, height);
            if(info.size() > 5242880):
                alert = QMessageBox()
                alert.setIcon(QMessageBox.Information)
                alert.setText("Your image is greater than 5MB")
                alert.setWindowTitle("Alert")
                alert.setStandardButtons(QMessageBox.Ok)
                alert.exec_()
                return
        pixmap = QPixmap(filename)
        scaled_pixmap = pixmap.scaled(1590, int(height * (1590 / width)))
        self.ui.photo.setPixmap(scaled_pixmap)
        self.ui.scroll2.setStyleSheet("")
        self.ui.scroll2.setStyleSheet("border: 1px solid black;")
        self.ui.photo.setFixedSize(1590, int(height * (1590 / width)))




def main():
    app = QApplication(sys.argv)
    desktop = app.desktop()
    size_screen = desktop.screenGeometry()
    print(size_screen.width(), size_screen.height())
    ventana = Aplicacion(size_screen.width(), size_screen.height())

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()