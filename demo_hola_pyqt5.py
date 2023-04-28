import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QDesktopWidget

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('OrCeph')
        #self.setGeometry(0,0, QDesktopWidget().screenGeometry().width(), QDesktopWidget().screenGeometry().height())
        #self.setFixedSize(QDesktopWidget().screenGeometry().width(), QDesktopWidget().screenGeometry().height()) #(ancho, alto)
        #self.showFullScreen()
        self.showMaximized()

def main():
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()