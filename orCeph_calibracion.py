import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
from orCeph_interfaz import Ui_MainWindow

class Aplicacion(QMainWindow):
    def __init__(self, width, height):
        super().__init__()
        
        self.inicializar_gui(width, height)

    def inicializar_gui(self, width, height):
        print(width, height)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self, width, height)
        
        self.ui.btn_buscar.clicked.connect(self.open_image)
        

        self.posicion_1 = [0, 0]
        self.posicion_2 = [0, 0]

        self.show()
    
    
    def mousePressEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.posicion_1[0] = event.pos().x()
            self.posicion_1[1] = event.pos().y()
    
    def mouseReleaseEvent(self, event):
        self.posicion_2[0] = event.pos().x()
        self.posicion_2[1] = event.pos().y()

        self.update()
    
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        pincel = QPen(Qt.black, 5)

        painter.setPen(pincel)
        painter.drawLine(self.posicion_1[0], self.posicion_1[1], self.posicion_2[0], self.posicion_2[1])

        painter.end()
    
    
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
        self.ui.photo.setPixmap(pixmap)
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