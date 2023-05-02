# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'orCeph_interfaz.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, width, height):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(width, height - 70)
        MainWindow.move(0,0)
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setGeometry(QtCore.QRect(width - 300, 110, 280, 38))
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lbl_ditancia = QtWidgets.QLabel(self.widget_2)
        self.lbl_ditancia.setObjectName("lbl_ditancia")
        self.horizontalLayout.addWidget(self.lbl_ditancia)
        self.input_medida = QtWidgets.QDoubleSpinBox(self.widget_2)
        self.input_medida.setObjectName("input_medida")
        self.horizontalLayout.addWidget(self.input_medida)
        self.select_unidad = QtWidgets.QComboBox(self.widget_2)
        self.select_unidad.setObjectName("select_unidad")
        self.select_unidad.addItem("")
        self.select_unidad.addItem("")
        self.select_unidad.addItem("")
        self.horizontalLayout.addWidget(self.select_unidad)
        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.widget_3.setGeometry(QtCore.QRect(width - 300, 160, 281, height - 350))
        self.widget_3.setObjectName("widget_3")
        self.lbl_lista = QtWidgets.QLabel(self.widget_3)
        self.lbl_lista.setGeometry(QtCore.QRect(10, 20, 261, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_lista.setFont(font)
        self.lbl_lista.setObjectName("lbl_lista")
        self.line = QtWidgets.QFrame(self.widget_3)
        self.line.setGeometry(QtCore.QRect(10, 30, 261, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.listView = QtWidgets.QListView(self.widget_3)
        self.listView.setGeometry(QtCore.QRect(10, 40, 261, height - 400))
        self.listView.setObjectName("listView")
        self.btn_calcular = QtWidgets.QPushButton(self.centralwidget)
        self.btn_calcular.setGeometry(QtCore.QRect(width - 290, 900, 261, 41))
        self.btn_calcular.setObjectName("btn_calcular")
        self.imagen = QtWidgets.QLabel(self.centralwidget)
        self.imagen.setGeometry(QtCore.QRect(30, 150, width-400, height-250))
        self.imagen.setObjectName("imagen")
        self.imagen.setStyleSheet('''
        QLabel {
            border: 4px dashed #aaa;
        }''')
        self.btn_mas = QtWidgets.QPushButton(self.centralwidget)
        self.btn_mas.setGeometry(QtCore.QRect(width-350, height-580, 41, 23))
        self.btn_mas.setObjectName("btn_mas")
        self.btn_menos = QtWidgets.QPushButton(self.centralwidget)
        self.btn_menos.setGeometry(QtCore.QRect(width-350, height-550, 41, 23))
        self.btn_menos.setObjectName("btn_menos")
        self.lbl_zoom = QtWidgets.QLabel(self.centralwidget)
        self.lbl_zoom.setGeometry(QtCore.QRect(width-350, height-600, 41, 16))
        self.lbl_zoom.setObjectName("lbl_zoom")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(30, 20, 536, 60))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_titulo = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_titulo.setFont(font)
        self.lbl_titulo.setObjectName("lbl_titulo")
        self.verticalLayout.addWidget(self.lbl_titulo)
        self.lbl_indicacion = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_indicacion.setFont(font)
        self.lbl_indicacion.setObjectName("lbl_indicacion")
        self.verticalLayout.addWidget(self.lbl_indicacion)
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(30, 90, 281, 25))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lbl_radiografia = QtWidgets.QLabel(self.widget1)
        self.lbl_radiografia.setObjectName("lbl_radiografia")
        self.horizontalLayout_2.addWidget(self.lbl_radiografia)
        self.btn_buscar = QtWidgets.QPushButton(self.widget1)
        self.btn_buscar.setObjectName("btn_buscar")
        self.horizontalLayout_2.addWidget(self.btn_buscar)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1086, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "orCeph"))
        self.lbl_ditancia.setText(_translate("MainWindow", "Distancia entre los puntos:"))
        self.select_unidad.setItemText(0, _translate("MainWindow", "mm"))
        self.select_unidad.setItemText(1, _translate("MainWindow", "cm"))
        self.select_unidad.setItemText(2, _translate("MainWindow", "in"))
        self.lbl_lista.setText(_translate("MainWindow", "Lista de Puntos de Steiner:"))
        self.btn_calcular.setText(_translate("MainWindow", "Calcular"))
        self.imagen.setText(_translate("MainWindow", "Imagen"))
        self.btn_mas.setText(_translate("MainWindow", "+"))
        self.btn_menos.setText(_translate("MainWindow", "-"))
        self.lbl_zoom.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Zoom</p></body></html>"))
        self.lbl_titulo.setText(_translate("MainWindow", "¡Bienvenido a OrCeph!"))
        self.lbl_indicacion.setText(_translate("MainWindow", "Coloque dos puntos de los cuales conozca la distancia entre ellos:"))
        self.lbl_radiografia.setText(_translate("MainWindow", "Ingrese la radiografía: "))
        self.btn_buscar.setText(_translate("MainWindow", "Buscar Imagen"))
