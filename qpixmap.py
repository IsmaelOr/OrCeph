import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Template(QWidget):
    def __init__(self):
        super().__init__()
        self.showMaximized()
        self.grid = QGridLayout(self)
        pixmap = QPixmap()
        self.grid.addWidget(pixmap,0,0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = Template()
    gui.show()
    sys.exit(app.exec_())