import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class PhotoLabel(QLabel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignCenter)
        self.posicion = [0,0]
        self.setText('\n\n Drop Image Here \n\n')
        self.setStyleSheet('''
        QLabel {
            border: 4px dashed #aaa;
        }''')


    def setPixmap(self, *args, **kwargs):
        pixmap = QPixmap(*args, **kwargs)

        super().setPixmap(pixmap)
        self.setStyleSheet('''
        QLabel {
            border: none;
        }''')


    


class Template(QWidget):

    def __init__(self):
        super().__init__()
        self.photo = PhotoLabel()
        self.posicion = [0,0]
        self.title = QLabel('¡Bienvenido a OrCeph!')
        self.title.setFont(QFont('Arial', 20, 100))
        label = QLabel('Ingrese la radiografía:')
        label.setFont(QFont('Arial', 12))
        btn = QPushButton('Browse')
        btn.clicked.connect(self.open_image)
        self.grid = QGridLayout(self)
        self.grid.addWidget(self.title, 0, 0, 2, 0, Qt.AlignCenter)
        self.grid.addWidget(label, 1, 0, Qt.AlignRight)
        self.grid.addWidget(btn, 1, 1, Qt.AlignLeft)
        self.grid.addWidget(self.photo, 2, 0, 8, 2)
        self.setAcceptDrops(True)
        self.showMaximized()
        #self.resize(300, 200)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            filename = event.mimeData().urls()[0].toLocalFile()
            event.accept()
            self.open_image(filename)
        else:
            event.ignore()

    def open_image(self, filename=None):
        if not filename:
            filename, _ = QFileDialog.getOpenFileName(self, 'Select Photo', QDir.currentPath(), "Images (*.png *.jpg *.jpeg)")
            if not filename:
                return
        self.grid.removeWidget(self.title);
        pixmap = QPixmap(filename)
        self.photo.setPixmap(pixmap)
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = Template()
    gui.show()
    sys.exit(app.exec_())