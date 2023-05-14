import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
from orCeph_interfaz import Ui_MainWindow
from functools import partial

from moduloSteiner import calcularPlanos2, calcularAngulos2

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
        
        
        self.ui.btn_reajustar.clicked.connect(self.colocarDistancia)
        self.ui.btn_calcular.clicked.connect(self.calcularSteiner)
        self.ui.btn_aceptarDistancia.clicked.connect(self.setDistancia)

        self.show()

    def setDistancia(self):
        self.ui.distanciaInput = self.ui.input_medida.value()
        self.ui.unidadInput = self.ui.select_unidad.currentText()
        if(self.ui.distanciaInput == 0):
            alert = QMessageBox()
            alert.setIcon(QMessageBox.Information)
            alert.setText("Porfavor ingrese la distancia entre los puntos ingresados")
            alert.setWindowTitle("Alert")
            alert.setStandardButtons(QMessageBox.Ok)
            alert.exec_()
            return
        else:
            self.ui.pixelUnidad = abs(1 * self.ui.distanciaInput / (self.ui.puntosDistancia['PuntoB'][1]-self.ui.puntosDistancia['PuntoA'][1]))
            # print(self.pixelInUnidad)  Cuantos mm equivale 1px
            for i, arg in enumerate(self.puntosSteinerList):
                self.ui.buttonList[i].setEnabled(True)
                self.ui.btn_calcular.setEnabled(True)
            self.ui.photo.distancia = False
            self.ui.lbl_indicacion.setText("Presione uno de los botones del listado de Puntos de Steiner para colocarlo:")
    

    def colocarDistancia(self):
        self.ui.photo.setDistancia(self.ui)
        self.ui.lbl_indicacion.setText("Coloque dos puntos en la radiografía para trazar una linea:")
    
    def calcularSteiner(self):
        # print(f'Puntos Steiner: \n {self.ui.puntosSteiner}')
        self.ui.planos = calcularPlanos2(self.ui.puntosSteiner, self.ui.planos)
        self.ui.angulos = calcularAngulos2(self.ui.puntosSteiner, self.ui.planos, self.ui.angulos)
        for plano,valor in self.ui.planos.items():
           self.ui.planos[plano] = valor * self.ui.pixelUnidad
        print(f'Planos: \n ${self.ui.planos}')
        print(f'Angulos: \n ${self.ui.angulos}')


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
        self.ui.btn_reajustar.setEnabled(True)
        self.ui.btn_reajustar.setText("Colocar Distancia")
        self.ui.lbl_indicacion.setText("Presione el botón 'Colocar distancia'.")




def main():
    app = QApplication(sys.argv)
    desktop = app.desktop()
    size_screen = desktop.screenGeometry()
    print(size_screen.width(), size_screen.height())
    ventana = Aplicacion(size_screen.width(), size_screen.height())

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()