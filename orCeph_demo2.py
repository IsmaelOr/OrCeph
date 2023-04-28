# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'orCeph_demo.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DibujoPunto(object):
    def setupUi(self, DibujoPunto, width, height):
        DibujoPunto.setObjectName("DibujoPunto")
        # DibujoPunto.resize(973, 733)
        # DibujoPunto.showMaximized()
        DibujoPunto.setFixedSize(width, height - 70)
        DibujoPunto.move(0,0)
        # DibujoPunto.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget = QtWidgets.QWidget(DibujoPunto)
        self.centralwidget.setObjectName("centralwidget")
        self.lbl_indicacion = QtWidgets.QLabel(self.centralwidget)
        self.lbl_indicacion.setGeometry(QtCore.QRect(30, 60, 701, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_indicacion.setFont(font)
        self.lbl_indicacion.setObjectName("lbl_indicacion")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 20, 500, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setGeometry(QtCore.QRect(width - 300, 110, 280, 38))
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget_2)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.widget_2)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.horizontalLayout.addWidget(self.doubleSpinBox)
        self.comboBox = QtWidgets.QComboBox(self.widget_2)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout.addWidget(self.comboBox)
        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.widget_3.setGeometry(QtCore.QRect(width - 300, 160, 281, height - 250))
        self.widget_3.setObjectName("widget_3")
        self.label_3 = QtWidgets.QLabel(self.widget_3)
        self.label_3.setGeometry(QtCore.QRect(10, 20, 261, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.line = QtWidgets.QFrame(self.widget_3)
        self.line.setGeometry(QtCore.QRect(10, 30, 261, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.listView = QtWidgets.QListView(self.widget_3)
        self.listView.setGeometry(QtCore.QRect(10, 40, 261, height - 300))
        self.listView.setObjectName("listView")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(30, 100, 611, 571))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        DibujoPunto.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(DibujoPunto)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 973, 21))
        self.menubar.setObjectName("menubar")
        DibujoPunto.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(DibujoPunto)
        self.statusbar.setObjectName("statusbar")
        DibujoPunto.setStatusBar(self.statusbar)

        self.retranslateUi(DibujoPunto)
        QtCore.QMetaObject.connectSlotsByName(DibujoPunto)

    def retranslateUi(self, DibujoPunto):
        _translate = QtCore.QCoreApplication.translate
        DibujoPunto.setWindowTitle(_translate("DibujoPunto", "orCeph"))
        self.lbl_indicacion.setText(_translate("DibujoPunto", "Coloque dos puntos de los cuales conozca la distancia entre ellos:"))
        self.label_2.setText(_translate("DibujoPunto", "¡Bienvenido a OrCeph!"))
        self.label.setText(_translate("DibujoPunto", "Distancia entre los puntos:"))
        self.comboBox.setItemText(0, _translate("DibujoPunto", "mm"))
        self.comboBox.setItemText(1, _translate("DibujoPunto", "cm"))
        self.comboBox.setItemText(2, _translate("DibujoPunto", "in"))
        self.label_3.setText(_translate("DibujoPunto", "Lista de Puntos de Steiner:"))
