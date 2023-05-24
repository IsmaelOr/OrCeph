import sys
import atexit
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QScreen
from orCeph_interfaz import Ui_MainWindow
from functools import partial
from fpdf import FPDF
from moduloSteiner import calcularPlanos2, calcularAngulos2, calcularFacial
from datetime import datetime
import os
import Poli_rc
from PIL import Image

class Aplicacion(QMainWindow):
    def __init__(self, width, height):
        super().__init__()
        
        self.inicializar_gui(width, height)

    def inicializar_gui(self, width, height):
        self.pdf = None
        print(width, height)
        self.setWindowTitle("Portada")
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self, width, height)
        
        self.ui.btn_buscar.clicked.connect(self.open_image)

        self.puntosSteinerList = list(self.ui.puntosSteiner.keys())

        for i, arg in enumerate(self.puntosSteinerList):
            self.ui.buttonList[i].clicked.connect(partial(self.drawPoint, arg, i))
        
        
        self.ui.btn_reajustar.clicked.connect(self.colocarDistancia)
        self.ui.btn_calcular.clicked.connect(self.calcularSteiner)
        self.ui.btn_aceptarDistancia.clicked.connect(self.setDistancia)
        self.ui.btn_verPlanos.clicked.connect(self.ui.photo.showPlanos)
        #self.ui.btn_verAngulos.clicked.connect(self.ui.photo.showAngulos)
        self.ui.btn_verPuntos.clicked.connect(self.ui.photo.showPuntos)
        self.ui.btn_descargarTrazado.clicked.connect(self.downloadTrazado)
        #self.ui.btn_descargarInforme.clicked.connect(partial(self.crearInforme, self.ui.puntosSteiner, self.ui.planos, self.ui.angulos))
        self.ui.btn_descargarInforme.clicked.connect(self.downloadInforme)
        self.ui.btn_verResultados.clicked.connect(self.showResultados)
        self.show()

    def showResultados(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        #print(os.path.abspath(os.getcwd()))
        #print(current_directory)
        self.ui.web_view.load(QUrl.fromLocalFile(f"{current_directory}/tempInforme.pdf"))
        self.ui.widget_5.hide()
        self.ui.widget_13.show()

    def downloadInforme(self):
        filepath, _ = QFileDialog.getSaveFileName(self, 'Guardar Informe de Resultados', 'Informe de Resultados', 'PDF (*.pdf)')
        if(filepath):
            self.pdf.output(filepath)

    def downloadTrazado(self):
        if self.ui.photo.pixmapPlanos:
            filepath, _ = QFileDialog.getSaveFileName(self, 'Guardar Pixmap', 'Trazado', 'Images (*.png *.jpg)')
            if(filepath):
                self.ui.photo.pixmapPlanos.save(filepath)

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
        self.ui.planos = calcularPlanos2(self.ui.puntosSteiner, self.ui.planos, self.ui)
        self.ui.angulos = calcularAngulos2(self.ui.puntosSteiner, self.ui.planos, self.ui.angulos, self.ui)
        for plano,valor in self.ui.planos.items():
           self.ui.planos[plano] = valor * self.ui.pixelUnidad
        print(f'Planos: \n ${self.ui.planos}')
        print(f'Angulos: \n ${self.ui.angulos}')
        if(len(self.ui.planos) != 0):
            current_directory = os.path.dirname(os.path.abspath(__file__))
            self.ui.photo.pixmapPlanos.save(f"{current_directory}/tempTrazado.png", "PNG")
            self.ui.btn_verPlanos.setEnabled(True)
            self.ui.btn_descargarTrazado.setEnabled(True)
        self.ui.btn_verPuntos.setEnabled(True)
        self.ui.btn_verResultados.setEnabled(True)
        #informe_pdf = self.crearInforme(self.ui.puntosSteiner, self.ui.planos, self.ui.angulos)
        self.ui.btn_descargarInforme.setEnabled(True)
        self.pdf = self.crearInforme(self.ui.puntosSteiner, self.ui.planos, self.ui.angulos)

    def crearInforme(self,puntos, planos, angulos):
        datos_planos = [
            'PM (Go-Gn)', 'SN', 'NA', 'NB', 'ND', 'III-AII', 'IIS-AIS', 'N-Ba', 'Po-Or', 'Pt-Gn', 'N-Gn', 'III-OMI', 'Linea S', 
            ['Pg-(NB)', 4, 1, 'Sínfisis mandibular retruida', 'Sínfisis mandibular normal', 'Sínfisis mandibular protruida'], 
            ['Silla-L', 51, 2, 'Posición adelantada mandíbula', 'Ortognático', 'Posición atrasada mandíbula'], 
            ['Silla-E', 22, 2, 'Posición atrasada del cóndilo', 'Ortognática', 'Posición adelantada del cóndilo'], 
            ['(Pg\'-Prn)-LI', 0, 1, 'Proquelia', 'Normal', 'Retroquelia'], 
            ['(Pg\'-Prn)-LS', 0, 1, 'Proquelia', 'Normal', 'Retroquelia'], 
            ['IIS-NA', 4,1, 'Retrusión del incisivo superior', 'Posición normal', 'Protrusión del incisivo superior'], 
            ['III-NB', 4,1, 'Retrusión del incisivo inferior', 'Posición normal', 'Protrusión del incisivo inferior']
        ]

        datos_angulos = [
            ['SNA', 82, 2, 'Retrusión maxilar', 'Maxialar en norma', 'Protusión maxilar'],
            ['SNB', 80, 2, 'Mandíbula retrasada', 'Mandíbular en norma', 'Mandíbula adelantada'],
            ['SND', 76, 2, 'Progenismo', 'Normal', 'Retrogenismo'],
            ['ANB', 2, 2, 'Clase III', 'Clase I', 'Clase II'],
            ['PO-SN', 14, 2, 'Mordida abierta', 'Normal', 'Mordida cerrada'],
            ['(Go-Gn)-(S-N)', 32, 2, 'Crecimiento vertical', 'Mesofacial', 'Crecimiento horizontal'],
            ['(IIS-AIS)-(N-A)', 22, 2, 'Proinclinación Incisiva', 'Normal', 'Retroinclinación Incisiva'],
            ['(III-AII)-(N-A)', 25, 1, 'Proinclinación Incisiva', 'Normal', 'Retroinclinación Incisiva'],
            ['(III-AII)-(IIS-AIS)', 130,5, 'Protusión dentaria', 'Normal', 'Mordida cerrada'],
            ['(A-B)-(Go-Gn)', 74, 2, 'Mordida abierta', 'Normal', 'Mordida cerrada'],
            ['(IIS-AIS)-(N-B)', 22, 1, 'Vestibuloversión', 'Normal', 'Linguoversión'],
            ['(III-AII)-(N-B)', 25,2, 'Vestibulogresión', 'Normal', 'Linguogresión'],
            ['(Ar-Go)-(Go-Me)', 130, 5, 'Crecimiento vertical', 'Mesofacial', 'Crecimiento horizontal'],
            ['(ENA-ENP)-(Go-Gn)', 5,2, 'Inclinación mordida abierta', 'Normal', 'Inclinación mordida cerrada'],
            ['(Po-Or)-(Go-Gn)', 1, 6, 'Inclinación mordida cerrada', 'Normal', 'Inclinación mordida abierta']
        ]

        analisis_esqueletico = [
            ['SNA', 82, 2, 'Prognatismo', 'Normal', 'Retrognatismo', 'A'],
            ['(ENA-ENP)-(Go-Gn)', 5, 2, 'Inclinación mordida abierta', 'Normal', 'Inclinación mordida cerrada', 'A'],
            ['SNB', 80, 2, 'Prognatismo', 'Normal', 'Retrognatismo', 'A'],
            ['SND', 77, 2, 'Progenismo', 'Normal', 'Retrogenismo', 'A'],
            ['Silla-L', 51, 2, 'Posición adelatanda mandíbula', 'Ortognático', 'Posición atrasada mandíbula', 'P'],
            ['Silla-E', 22, 2, 'Posición atrasada del condílo', 'Ortognática', 'Posición adelantada del cóndilo', 'P'],
            ['(Ar-Go)-(Go-Me)', 125, 5, 'Crecimiento vertical', 'Mesofacial', 'Crecimiento horizontal', 'A'],
            ['(Go-Gn)-(S-N)', 32, 2, 'Crecimiento vertical', 'Mesofacial', 'Crecimiento horizontal', 'A'],
            ['ANB', 2, 2, 'Clase III', 'Clase I', 'Clase II', 'A'],
            ['(A-B)-(Go-Gn)', 74, 2, 'Mordida abierta', 'Normal', 'Mordida cerrada', 'A']
        ]

        analisis_dental = [
            ['(IIS-AIS)-(S-N)', 104, 2, 'Vestibuloversión', 'Normal', 'Linguoversión', 'A'],
            ['(IIS-AIS)-(N-A)', 22, 2, 'Proinclinación incisiva', 'Normal', 'Retroinclinación incisiva', 'A'],
            ['IIS-NA', 4, 1, 'Retrusión del incisivo superior', 'Posición normal', 'Protrusión del incisivo superior', 'P'],
            ['(III-AII)-(N-B)', 25, 2, 'Vestibulogresión', 'Normal', 'Linguogresión', 'A'],
            ['III-NB', 4, 1, 'Retrusión del incisivo inferior', 'Posición normal', 'Protrusión del incisivo inferior', 'P'],
            ['PO-SN', 14, 2, 'Mordida abierta', 'Normal', 'Mordida cerrada', 'A'],
            ['(III-AII)-(IIS-AIS)', 130,5, 'Protusión dentaria', 'Normal', 'Mordida cerrada', 'A'],
            ['Pg-(NB)', 4, 1, 'Sínfisis mandibular retruida', 'Sínfisis normal', 'Sínfisis mandibular protruida', 'P']
        ]       

        analisis_tejidos = [
            ['(Pg\'-Prn)-LI', 'Linea S (LI)',0, 1, 'Retroquelia', 'Normal', 'Proquelia'],
            ['(Pg\'-Prn)-LS', 'Linea S (LS)',0, 1, 'Retroquelia', 'Normal', 'Proquelia']
        ]

        analisis_facial = [
            ['Tr-G', 'G-Sn', 'Sn-Me', 'N-Me', 'N-Sn', 'Sn-Me','Sn-St', 'St-Me', 'Sn-Me', 'LS-St-LI'],
            ['', '', '', '100%', '43%', '57%', '1/3', '2/3', '3/3', '3mm±1']
        ]
        
        print(f'Creando PDF')
        pdf = PDF(orientation='P', unit='mm', format='A4')
        # PORTADA
        pdf.add_page()
        pdf.set_font('times', 'B', 25)
        pdf.multi_cell(w=0, h=25, txt="Reporte generado por OrCeph", border=0, align= 'C', fill = 0)
        current_directory = os.path.dirname(os.path.abspath(__file__))
        pdf.image(f"{current_directory}/Logo Steiner.jpg", x=55, y=30, w=100, h=109)
        pdf.set_font('times', 'B', 8)
        pdf.set_y(140)
        pdf.multi_cell(w=0, h=15, txt="© Ismael Ortega Estrada, IPN ESCOM. Todos los derechos reservados.", border=0, align= 'C', fill = 0)
        pdf.set_font('times', 'B', 20)
        pdf.multi_cell(w=0, h=20, txt="Datos del Paciente:", border=0, align= 'L', fill = 0)
        pdf.set_font('times', 'B', 15)
        pdf.cell(w=30, h=20, txt="Nombre:", border=0, align= 'L', fill = 0)
        nombre = self.ui.input_nombreP.text() if self.ui.input_nombreP.text() else '____________________________________'  
        pdf.multi_cell(w=0, h=20, txt=f"{nombre}", border=0, align= 'L', fill = 0)
        pdf.cell(w=30, h=20, txt="Edad:", border=0, align= 'L', fill = 0)
        edad = self.ui.input_edad.value() if self.ui.input_edad.value() != 0 else '____________________________________'
        pdf.multi_cell(w=0, h=20, txt=f"{edad}", border=0, align= 'L', fill = 0)
        pdf.cell(w=30, h=20, txt="Sexo:", border=0, align= 'L', fill = 0)
        sexo = self.ui.select_sexo.currentText() if self.ui.select_sexo.currentText() != '' else '____________________________________'  
        pdf.multi_cell(w=0, h=20, txt=f"{sexo}", border=0, align= 'L', fill = 0)
        
        pdf.add_page()
        pdf.set_font('times', 'B', 10)
        ################ Análisis Esqueletico ################
        pdf.multi_cell(w=0, h=10, txt="Análisis esquelético", border=0, align= 'C', fill = 0)
        pdf.set_font('times', 'B', 7)
        pdf.cell(w=25, h=10, txt="", border=0, align= 'C', fill = 0)
        pdf.cell(w=25, h=10, txt="Plano o Ángulo", border=1, align= 'C', fill = 0)
        pdf.cell(w=20, h=10, txt="Valor normal", border=1, align= 'C', fill = 0)
        pdf.cell(w=20, h=10, txt="Valor calculado", border=1, align= 'C', fill = 0)
        pdf.multi_cell(w=0,h=5, txt="Diagnostico", border=1, align= 'C', fill = 0)
        pdf.cell(w=90, h=5, txt="", border=0, align= 'C', fill = 0)
        pdf.cell(w=38, h=5, txt="Disminuido", border=1, align= 'C', fill = 0)
        pdf.cell(w=23, h=5, txt="Normal", border=1, align= 'C', fill = 0)
        pdf.multi_cell(w=39, h=5, txt="Aumentado", border=1, align= 'C', fill = 0)
        pdf.set_font('times', '', 8)
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.multi_cell(w=25, h=5, txt="Posición y tamaño del maxilar superior", border=1, align= 'C', fill = 0)
        y1 = pdf.get_y()
        pdf.set_xy(x+25, y)
        for i in range(0,10):
            pdf.set_x(x+25)
            medida = 'mm' if i == 4 or i == 5 else '°'
            altura = 10 if i == 8 or i == 9 else 5 
            pdf.cell(w=25, h=altura, txt=f"{analisis_esqueletico[i][0]}", border=1, align= 'C', fill = 0)
            pdf.cell(w=20, h=altura, txt=f"{analisis_esqueletico[i][1]}±{analisis_esqueletico[i][2]}{medida}", border=1, align= 'C', fill = 0)
            if (analisis_esqueletico[i][6] == 'P' ):
                if(analisis_esqueletico[i][0] in planos):
                    valor = planos[analisis_esqueletico[i][0]]
                    pdf.cell(w=20, h=altura, txt=f"{valor:.2f}mm", border=1, align= 'C', fill = 0)
                else:
                    valor = '-'
                    pdf.cell(w=20, h=altura, txt=f"{valor}", border=1, align= 'C', fill = 0)
            else:
                if(analisis_esqueletico[i][0] in angulos):
                    valor = angulos[analisis_esqueletico[i][0]]
                    pdf.cell(w=20, h=altura, txt=f"{valor:.2f}°", border=1, align= 'C', fill = 0)
                else:
                    valor = '-'
                    pdf.cell(w=20, h=altura, txt=f"{valor}", border=1, align= 'C', fill = 0)
            pdf.set_fill_color(173, 216, 230)
            if(valor != '-' and valor < analisis_esqueletico[i][1]-analisis_esqueletico[i][2]):
                print(f"{valor} - {analisis_esqueletico[i][1]-analisis_esqueletico[i][2]}")
                pdf.cell(w=38, h=altura, txt=f"{analisis_esqueletico[i][3]}", border=1, align= 'C', fill = 1)
            else:
                pdf.cell(w=38, h=altura, txt=f"{analisis_esqueletico[i][3]}", border=1, align= 'C', fill = 0)
            if(valor != '-' and valor <= analisis_esqueletico[i][1]+analisis_esqueletico[i][2] and valor >= analisis_esqueletico[i][1]-analisis_esqueletico[i][2]):
                pdf.cell(w=23, h=altura, txt=f"{analisis_esqueletico[i][4]}", border=1, align= 'C', fill = 1)
            else:
                pdf.cell(w=23, h=altura, txt=f"{analisis_esqueletico[i][4]}", border=1, align= 'C', fill = 0)
            if(valor != '-' and valor > analisis_esqueletico[i][1]+analisis_esqueletico[i][2]):
                print(f"{valor} + {analisis_esqueletico[i][1]+analisis_esqueletico[i][2]}")
                pdf.multi_cell(w=39, h=altura, txt=f"{analisis_esqueletico[i][5]}", border=1, align= 'C', fill = 1)
            else:
                pdf.multi_cell(w=39, h=altura, txt=f"{analisis_esqueletico[i][5]}", border=1, align= 'C', fill = 0)
        pdf.set_xy(x,y1+10)
        pdf.multi_cell(w=25, h=5, txt="Posición y tamaño mandibular", border=0, align= 'C', fill = 0)
        pdf.set_xy(x,y1)
        pdf.multi_cell(w=25, h=30, txt="", border=1, align= 'C', fill = 0)
        pdf.multi_cell(w=25, h=5, txt="Relación sagital maxilomandibular", border=1, align= 'C', fill = 0)
        pdf.multi_cell(w=25, h=5, txt="Posición vertical maxilomandibular", border=1, align= 'C', fill = 0)

        pdf.multi_cell(w=0, h=5, txt="", border=0, fill=0)


        ################ Análisis Dental ################
        pdf.set_font('times', 'B', 10)
        pdf.multi_cell(w=0, h=10, txt="Análisis dental", border=0, align= 'C', fill = 0)
        pdf.set_font('times', 'B', 7)
        pdf.cell(w=25, h=10, txt="", border=0, align= 'C', fill = 0)
        pdf.cell(w=25, h=10, txt="Plano o Ángulo", border=1, align= 'C', fill = 0)
        pdf.cell(w=20, h=10, txt="Valor normal", border=1, align= 'C', fill = 0)
        pdf.cell(w=20, h=10, txt="Valor calculado", border=1, align= 'C', fill = 0)
        pdf.multi_cell(w=0,h=5, txt="Diagnostico", border=1, align= 'C', fill = 0)
        pdf.cell(w=90, h=5, txt="", border=0, align= 'C', fill = 0)
        pdf.cell(w=38, h=5, txt="Disminuido", border=1, align= 'C', fill = 0)
        pdf.cell(w=23, h=5, txt="Normal", border=1, align= 'C', fill = 0)
        pdf.multi_cell(w=39, h=5, txt="Aumentado", border=1, align= 'C', fill = 0)
        pdf.set_font('times', '', 8)
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.multi_cell(w=25, h=25, txt="", border=1, align= 'C', fill = 0)
        y1 = pdf.get_y()
        pdf.set_xy(x+25, y)
        for i in range(0,8):
            pdf.set_x(x+25)
            medida = 'mm' if i == 2 or i == 4 or i == 7 else '°'
            altura = 5
            pdf.cell(w=25, h=altura, txt=f"{analisis_dental[i][0]}", border=1, align= 'C', fill = 0)
            pdf.cell(w=20, h=altura, txt=f"{analisis_dental[i][1]}±{analisis_dental[i][2]}{medida}", border=1, align= 'C', fill = 0)
            if(analisis_dental[i][6] == 'P'):
                if(analisis_dental[i][0] in planos):
                    valor = planos[analisis_dental[i][0]]
                    pdf.cell(w=20, h=altura, txt=f"{valor:.2f}mm", border=1, align= 'C', fill = 0)
                else:
                    valor='-'
                    pdf.cell(w=20, h=altura, txt=f"{valor}", border=1, align= 'C', fill = 0)
            else:
                if(analisis_dental[i][0] in angulos):
                    valor = angulos[analisis_dental[i][0]]
                    pdf.cell(w=20, h=altura, txt=f"{valor:.2f}°", border=1, align= 'C', fill = 0)
                else:
                    valor='-'
                    pdf.cell(w=20, h=altura, txt=f"{valor}", border=1, align= 'C', fill = 0)
            if(valor != '-' and valor < analisis_dental[i][1]-analisis_dental[i][2]):
                pdf.cell(w=38, h=altura, txt=f"{analisis_dental[i][3]}", border=1, align= 'C', fill = 1)
            else:
                pdf.cell(w=38, h=altura, txt=f"{analisis_dental[i][3]}", border=1, align= 'C', fill = 0)
            if(valor != '-' and valor >= analisis_dental[i][1]-analisis_dental[i][2] and valor <= analisis_dental[i][1]+analisis_dental[i][2]):
                pdf.cell(w=23, h=altura, txt=f"{analisis_dental[i][4]}", border=1, align= 'C', fill = 1)
            else:
                pdf.cell(w=23, h=altura, txt=f"{analisis_dental[i][4]}", border=1, align= 'C', fill = 0)
            if(valor != '-' and valor > analisis_dental[i][1]+analisis_dental[i][2]):
                pdf.multi_cell(w=39, h=altura, txt=f"{analisis_dental[i][5]}", border=1, align= 'C', fill = 1)
            else:
                pdf.multi_cell(w=39, h=altura, txt=f"{analisis_dental[i][5]}", border=1, align= 'C', fill = 0)
        pdf.set_xy(x,y1)
        pdf.multi_cell(w=25, h=15, txt="", border=1, align= 'C', fill = 0)

        pdf.set_xy(x,y+5)
        pdf.multi_cell(w=25, h=5, txt="Incisivos con respecto a bases óseas", border=0, align= 'C', fill = 0)

        pdf.set_xy(x,y1+2.5)
        pdf.multi_cell(w=25, h=5, txt="Relación dentaria mentón óseo", border=0, align= 'C', fill = 0)

        pdf.set_xy(x,y1+15)

        pdf.multi_cell(w=0, h=5, txt="", border=0, fill=0)

        ################ Análisis de Tejidos Blandos ################

        pdf.set_font('times', 'B', 10)
        pdf.multi_cell(w=0, h=10, txt="Análisis de tejidos blandos", border=0, align= 'C', fill = 0)
        pdf.set_font('times', 'B', 7)
        pdf.cell(w=25, h=10, txt="", border=0, align= 'C', fill = 0)
        pdf.cell(w=25, h=10, txt="Plano o Ángulo", border=1, align= 'C', fill = 0)
        pdf.cell(w=20, h=10, txt="Valor normal", border=1, align= 'C', fill = 0)
        pdf.cell(w=20, h=10, txt="Valor calculado", border=1, align= 'C', fill = 0)
        pdf.multi_cell(w=0,h=5, txt="Diagnostico", border=1, align= 'C', fill = 0)
        pdf.cell(w=90, h=5, txt="", border=0, align= 'C', fill = 0)
        pdf.cell(w=38, h=5, txt="Disminuido", border=1, align= 'C', fill = 0)
        pdf.cell(w=23, h=5, txt="Normal", border=1, align= 'C', fill = 0)
        pdf.multi_cell(w=39, h=5, txt="Aumentado", border=1, align= 'C', fill = 0)
        pdf.set_font('times', '', 8)
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.multi_cell(w=25, h=10, txt="Perfil", border=1, align= 'C', fill = 0)
        pdf.set_xy(x+25, y)
        for i in range(0,2):
            pdf.set_x(x+25)
            medida = 'mm'
            altura = 5
            pdf.cell(w=25, h=altura, txt=f"{analisis_tejidos[i][1]}", border=1, align= 'C', fill = 0)
            pdf.cell(w=20, h=altura, txt=f"{analisis_tejidos[i][2]}±{analisis_tejidos[i][3]}{medida}", border=1, align= 'C', fill = 0)
            if(analisis_tejidos[i][0] in planos):
                valor = planos[analisis_tejidos[i][0]]
                pdf.cell(w=20, h=altura, txt=f"{valor:.2f}mm", border=1, align= 'C', fill = 0)
            else:
                valor = '-'
                pdf.cell(w=20, h=altura, txt=f"{valor}", border=1, align= 'C', fill = 0)
            if(valor != '-' and valor < analisis_tejidos[i][2]-analisis_tejidos[i][3]):
                pdf.cell(w=38, h=altura, txt=f"{analisis_tejidos[i][4]}", border=1, align= 'C', fill = 1)
            else:
                pdf.cell(w=38, h=altura, txt=f"{analisis_tejidos[i][4]}", border=1, align= 'C', fill = 0)
            if(valor != '-' and valor >= analisis_tejidos[i][2]-analisis_tejidos[i][3] and valor <= analisis_tejidos[i][2]+analisis_tejidos[i][3]):
                pdf.cell(w=23, h=altura, txt=f"{analisis_tejidos[i][5]}", border=1, align= 'C', fill = 1)
            else:
                pdf.cell(w=23, h=altura, txt=f"{analisis_tejidos[i][5]}", border=1, align= 'C', fill = 0)
            if(valor != '-' and valor > analisis_tejidos[i][2]+analisis_tejidos[i][3]):
                pdf.multi_cell(w=39, h=altura, txt=f"{analisis_tejidos[i][6]}", border=1, align= 'C', fill = 1)
            else:
                pdf.multi_cell(w=39, h=altura, txt=f"{analisis_tejidos[i][6]}", border=1, align= 'C', fill = 0)
        pdf.multi_cell(w=0, h=5, txt="", border=0, fill=0)

        ################ Análisis Facial ################
        planos_facial = {}
        planos_facial = calcularFacial(puntos, planos_facial)
        for plano,valor in planos_facial.items():
           planos_facial[plano] = valor * self.ui.pixelUnidad

        pdf.set_font('times', 'B', 10)
        pdf.multi_cell(w=0, h=10, txt="Análisis facial", border=0, align= 'C', fill = 0)
        pdf.set_font('times', 'B', 7)
        pdf.cell(w=25, h=10, txt="", border=0, align= 'C', fill = 0)
        pdf.cell(w=25, h=10, txt="Plano", border=1, align= 'C', fill = 0)
        pdf.cell(w=20, h=10, txt="Norma", border=1, align= 'C', fill = 0)
        pdf.cell(w=20, h=10, txt="Valor calculado", border=1, align= 'C', fill = 0)
        pdf.multi_cell(w=0,h=10, txt="Diagnostico", border=1, align= 'C', fill = 0)
        pdf.set_font('times', '', 8)
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.multi_cell(w=25, h=15, txt="", border=1, align= 'C', fill = 0)
        y1 = pdf.get_y()
        pdf.set_xy(x+25, y)
        yFila = y
        for i in range(0,10):
            pdf.set_xy(x+25, yFila)
            yFila = pdf.get_y() + 5
            pdf.cell(w=25, h=5, txt=f"{analisis_facial[0][i]}", border=1, align= 'C', fill = 0)

        pdf.set_xy(x+50, y)
        pdf.multi_cell(w=20, h=7.5, txt="Deben medir lo mismo", border=1, align= 'C', fill = 0)
        for i in range(3,10):
            pdf.set_x(x+50)
            pdf.multi_cell(w=20, h=5, txt=f"{analisis_facial[1][i]}", border=1, align= 'C', fill = 0)

        pdf.set_xy(x+70, y)
        for i in range(0,10):
            pdf.set_x(x+70)
            if(analisis_facial[0][i] in planos_facial):
                valor = planos_facial[analisis_facial[0][i]]
                pdf.multi_cell(w=20, h=5, txt=f"{valor:.2f}mm", border=1, align= 'C', fill = 0)
            else:
                valor='-'
                pdf.multi_cell(w=20, h=5, txt=f"{valor}", border=1, align= 'C', fill = 0)

        pdf.set_xy(x+90, y)
        if('Tr-G' in planos_facial and 'G-Sn' in planos_facial and 'Sn-Me' in planos_facial):
            if((planos_facial['Tr-G'] == planos_facial['G-Sn']) and (planos_facial['Tr-G'] == planos_facial['Sn-Me'])):
                pdf.cell(w=50, h=15, txt=f"Simétrico", border=1, align= 'C', fill = 1)
                pdf.multi_cell(w=50, h=15, txt=f"Asimétrico", border=1, align= 'C', fill = 0)
            else:
                pdf.cell(w=50, h=15, txt=f"Simétrico", border=1, align= 'C', fill = 0)
                pdf.multi_cell(w=50, h=15, txt=f"Asimétrico", border=1, align= 'C', fill = 1)
        else:
            pdf.cell(w=50, h=15, txt=f"Simétrico", border=1, align= 'C', fill = 0)
            pdf.multi_cell(w=50, h=15, txt=f"Asimétrico", border=1, align= 'C', fill = 0)

        pdf.set_x(x+90)
        if('N-Me' in planos_facial and 'N-Sn' in planos_facial and 'Sn-Me' in planos_facial):
            if((int(planos_facial['N-Sn'] * 100 / planos_facial['N-Me']) == 43) and (int(planos_facial['Sn-Me'] * 100 / planos_facial['N-Me']) == 57)):
                pdf.cell(w=33, h=15, txt=f"Los tercios coinciden", border=1, align= 'C', fill = 1)
                pdf.multi_cell(w=33, h=5, txt=f"El tercio superior esta aumentado y el inferior disminuido", border=1, align= 'C', fill = 0)
                pdf.set_xy(x+156, pdf.get_y()-15)
                pdf.multi_cell(w=34, h=5, txt=f"El tercio superior esta disminuido y el inferior aumentado", border=1, align= 'C', fill = 0)
            elif((int(planos_facial['Sn-Me'] * 100 / planos_facial['N-Me']) > 57)):
                pdf.cell(w=33, h=15, txt=f"Los tercios coinciden", border=1, align= 'C', fill = 0)
                pdf.multi_cell(w=33, h=5, txt=f"El tercio superior esta aumentado y el inferior disminuido", border=1, align= 'C', fill = 1)
                pdf.set_xy(x+156, pdf.get_y()-15)
                pdf.multi_cell(w=34, h=5, txt=f"El tercio superior esta disminuido y el inferior aumentado", border=1, align= 'C', fill = 0)
            elif((int(planos_facial['Sn-Me'] * 100 / planos_facial['N-Me']) < 57)):
                pdf.cell(w=33, h=15, txt=f"Los tercios coinciden", border=1, align= 'C', fill = 0)
                pdf.multi_cell(w=33, h=5, txt=f"El tercio superior esta aumentado y el inferior disminuido", border=1, align= 'C', fill = 0)
                pdf.set_xy(x+156, pdf.get_y()-15)
                pdf.multi_cell(w=34, h=5, txt=f"El tercio superior esta disminuido y el inferior aumentado", border=1, align= 'C', fill = 1)
        else:
            pdf.cell(w=33, h=15, txt=f"Los tercios coinciden", border=1, align= 'C', fill = 0)
            pdf.multi_cell(w=33, h=5, txt=f"El tercio superior esta aumentado y el inferior disminuido", border=1, align= 'C', fill = 0)
            pdf.set_xy(x+156, pdf.get_y()-15)
            pdf.multi_cell(w=34, h=5, txt=f"El tercio superior esta disminuido y el inferior aumentado", border=1, align= 'C', fill = 0)

        pdf.set_x(x+90)
        if('Sn-St' in planos_facial and 'St-Me' in planos_facial and 'Sn-Me' in planos_facial):
            if((int(planos_facial['Sn-St'])  == int(planos_facial['Sn-Me'] / 3)) and (int(planos_facial['St-Me'])  == (int(planos_facial['Sn-Me'] / 3))*2)):
                pdf.cell(w=33, h=15, txt=f"Los tercios coinciden", border=1, align= 'C', fill = 1)
                pdf.multi_cell(w=33, h=5, txt=f"El tercio superior esta aumentado y el inferior disminuido", border=1, align= 'C', fill = 0)
                pdf.set_xy(x+156, pdf.get_y()-15)
                pdf.multi_cell(w=34, h=5, txt=f"El tercio superior esta disminuido y el inferior aumentado", border=1, align= 'C', fill = 0)
            elif((int(planos_facial['St-Me'])  > (int(planos_facial['Sn-Me'] / 3))*2)):
                pdf.cell(w=33, h=15, txt=f"Los tercios coinciden", border=1, align= 'C', fill = 0)
                pdf.multi_cell(w=33, h=5, txt=f"El tercio superior esta aumentado y el inferior disminuido", border=1, align= 'C', fill = 1)
                pdf.set_xy(x+156, pdf.get_y()-15)
                pdf.multi_cell(w=34, h=5, txt=f"El tercio superior esta disminuido y el inferior aumentado", border=1, align= 'C', fill = 0)
            elif((int(planos_facial['St-Me'])  < (int(planos_facial['Sn-Me'] / 3))*2)):
                pdf.cell(w=33, h=15, txt=f"Los tercios coinciden", border=1, align= 'C', fill = 0)
                pdf.multi_cell(w=33, h=5, txt=f"El tercio superior esta aumentado y el inferior disminuido", border=1, align= 'C', fill = 0)
                pdf.set_xy(x+156, pdf.get_y()-15)
                pdf.multi_cell(w=34, h=5, txt=f"El tercio superior esta disminuido y el inferior aumentado", border=1, align= 'C', fill = 1)
        else:
            pdf.cell(w=33, h=15, txt=f"Los tercios coinciden", border=1, align= 'C', fill = 0)
            pdf.multi_cell(w=33, h=5, txt=f"El tercio superior esta aumentado y el inferior disminuido", border=1, align= 'C', fill = 0)
            pdf.set_xy(x+156, pdf.get_y()-15)
            pdf.multi_cell(w=34, h=5, txt=f"El tercio superior esta disminuido y el inferior aumentado", border=1, align= 'C', fill = 0)
        pdf.set_x(x+90)
        if('LS-St-LI' in planos_facial):
            if(planos_facial['LS-St-LI'] >= 2 and planos_facial['LS-St-LI'] <= 4):
                pdf.cell(w=50, h=5, txt=f"Competencia labial", border=1, align= 'C', fill = 1)
                pdf.multi_cell(w=50, h=5, txt=f"Incompetencia labial", border=1, align= 'C', fill = 0)
            else:
                pdf.cell(w=50, h=5, txt=f"Competencia labial", border=1, align= 'C', fill = 0)
                pdf.multi_cell(w=50, h=5, txt=f"Incompetencia labial", border=1, align= 'C', fill = 1)
        else:
            pdf.cell(w=50, h=5, txt=f"Competencia labial", border=1, align= 'C', fill = 0)
            pdf.multi_cell(w=50, h=5, txt=f"Incompetencia labial", border=1, align= 'C', fill = 0)



        pdf.set_xy(x,y+2.5)
        pdf.multi_cell(w=25, h=5, txt="Evaluación Sagital vertical", border=0, align= 'C', fill = 0)
        pdf.set_xy(x,y1)
        pdf.multi_cell(w=25, h=15, txt="", border=1, align= 'C', fill = 0)
        pdf.multi_cell(w=25, h=15, txt="", border=1, align= 'C', fill = 0)
        pdf.multi_cell(w=25, h=5, txt="Perfil Labial", border=1, align= 'C', fill = 0)

        pdf.set_xy(x,y1)
        pdf.multi_cell(w=25, h=5, txt="Evaluación sagital vertical 2 tercios inferiores", border=1, align= 'C', fill = 0)
        pdf.multi_cell(w=25, h=5, txt="Evaluación sagital vertical de los tercios inferiores", border=1, align= 'C', fill = 0)

        # TABLA DE PLANOS
        pdf.add_page()
        pdf.set_font('times', 'B', 10)
        pdf.multi_cell(w=0, h=10, txt="Planos o Segmentos cefalométricos", border=1, align= 'C', fill = 0)
        pdf.set_font('times', 'B', 7)
        pdf.cell(w=10, h=10, txt="Número", border=1, align= 'C', fill = 0)
        pdf.cell(w=25, h=10, txt="Plano", border=1, align= 'C', fill = 0)
        pdf.cell(w=20, h=10, txt="Valor Normal", border=1, align= 'C', fill = 0)
        pdf.cell(w=20, h=10, txt="Valor Calculado", border=1, align= 'C', fill = 0)
        pdf.multi_cell(w=0,h=5, txt="Diagnostico", border=1, align= 'C', fill = 0)
        pdf.cell(w=75, h=5, txt="", border=0, align= 'C', fill = 0)
        pdf.cell(w=38, h=5, txt="Disminuido", border=1, align= 'C', fill = 0)
        pdf.cell(w=38, h=5, txt="Normal", border=1, align= 'C', fill = 0)
        pdf.multi_cell(w=39, h=5, txt="Aumentado", border=1, align= 'C', fill = 0)
        pdf.set_font('times', '', 8)
        for i in range(0,13):
            pdf.cell(w=10, h=8, txt=f"{i+1}", border=1, align= 'C', fill = 0)
            pdf.cell(w=25, h=8, txt=f"{datos_planos[i]}", border=1, align= 'C', fill = 0)
            pdf.cell(w=20, h=8, txt=f"No aplica", border=1, align= 'C', fill = 0)
            if(datos_planos[i] in planos):
                pdf.cell(w=20, h=8, txt=f'{planos[datos_planos[i]]:.2f}mm', border=1, align= 'C', fill = 0)
            else:
                pdf.cell(w=20, h=8, txt=f'-', border=1, align= 'C', fill = 0)
            pdf.multi_cell(w=0, h=8, txt="No se prestan a medición, únicamente constituyen planos para la posterior formación del ángulo ",  border=1, align= 'C', fill = 0)
        for i in range (13, 20):
            pdf.cell(w=10, h=8, txt=f"{i+1}", border=1, align= 'C', fill = 0)
            pdf.cell(w=25, h=8, txt=f"{datos_planos[i][0]}", border=1, align= 'C', fill = 0)
            pdf.cell(w=20, h=8, txt=f"{datos_planos[i][1]}±{datos_planos[i][2]}mm", border=1, align= 'C', fill = 0)
            if(datos_planos[i][0] in planos):
                pdf.cell(w=20, h=8, txt=f'{planos[datos_planos[i][0]]:.2f}mm', border=1, align= 'C', fill = 0)
            else:
                pdf.cell(w=20, h=8, txt=f'-', border=1, align= 'C', fill = 0)

            pdf.set_fill_color(173, 216, 230)
            if((datos_planos[i][0] in planos) and (planos[datos_planos[i][0]] < (datos_planos[i][1] - datos_planos[i][2]))):
                pdf.cell(w=38, h=8, txt=f"{datos_planos[i][3]}", border=1, align= 'C', fill = 1)
            else:
                pdf.cell(w=38, h=8, txt=f"{datos_planos[i][3]}", border=1, align= 'C', fill = 0)
            if((datos_planos[i][0] in planos) and planos[datos_planos[i][0]] >= (datos_planos[i][1] - datos_planos[i][2]) and planos[datos_planos[i][0]] <= (datos_planos[i][1] + datos_planos[i][2])):
                pdf.cell(w=38, h=8, txt=f"{datos_planos[i][4]}", border=1, align= 'C', fill = 1)
            else:
                pdf.cell(w=38, h=8, txt=f"{datos_planos[i][4]}", border=1, align= 'C', fill = 0)
            if((datos_planos[i][0] in planos) and planos[datos_planos[i][0]] > (datos_planos[i][1] + datos_planos[i][2])):
                pdf.multi_cell(w=39, h=8, txt=f"{datos_planos[i][5]}", border=1, align= 'C', fill = 1)
            else:
                pdf.multi_cell(w=39, h=8, txt=f"{datos_planos[i][5]}", border=1, align= 'C', fill = 0)
        
        # TABLA DE ÁNGULOS
        pdf.add_page()
        pdf.set_font('times', 'B', 10)
        pdf.multi_cell(w=0, h=10, txt="Ángulos cefalométricos", border=1, align= 'C', fill = 0)
        pdf.set_font('times', 'B', 7)
        pdf.cell(w=10, h=10, txt="Número", border=1, align= 'C', fill = 0)
        pdf.cell(w=25, h=10, txt="Ángulo", border=1, align= 'C', fill = 0)
        pdf.cell(w=20, h=10, txt="Valor Normal", border=1, align= 'C', fill = 0)
        pdf.cell(w=20, h=10, txt="Valor Calculado", border=1, align= 'C', fill = 0)
        pdf.multi_cell(w=0,h=5, txt="Diagnostico", border=1, align= 'C', fill = 0)
        pdf.cell(w=75, h=5, txt="", border=0, align= 'C', fill = 0)
        pdf.cell(w=38, h=5, txt="Disminuido", border=1, align= 'C', fill = 0)
        pdf.cell(w=38, h=5, txt="Normal", border=1, align= 'C', fill = 0)
        pdf.multi_cell(w=39, h=5, txt="Aumentado", border=1, align= 'C', fill = 0)
        pdf.set_font('times', '', 8)
        for i in range(0,15):
            pdf.cell(w=10, h=8, txt=f"{i+1}", border=1, align= 'C', fill = 0)
            pdf.cell(w=25, h=8, txt=f"{datos_angulos[i][0]}", border=1, align= 'C', fill = 0)
            pdf.cell(w=20, h=8, txt=f"{datos_angulos[i][1]}±{datos_angulos[i][2]}°", border=1, align= 'C', fill = 0)
            if(datos_angulos[i][0] in angulos):
                pdf.cell(w=20, h=8, txt=f'{angulos[datos_angulos[i][0]]:.2f}°', border=1, align= 'C', fill = 0)
            else:
                pdf.cell(w=20, h=8, txt=f'-', border=1, align= 'C', fill = 0)
            pdf.set_fill_color(173, 216, 230)
            if((datos_angulos[i][0] in angulos) and (angulos[datos_angulos[i][0]] < (datos_angulos[i][1] - datos_angulos[i][2]))):
                pdf.cell(w=38, h=8, txt=f"{datos_angulos[i][3]}", border=1, align= 'C', fill = 1)
            else:
                pdf.cell(w=38, h=8, txt=f"{datos_angulos[i][3]}", border=1, align= 'C', fill = 0)
            if((datos_angulos[i][0] in angulos) and angulos[datos_angulos[i][0]] >= (datos_angulos[i][1] - datos_angulos[i][2]) and angulos[datos_angulos[i][0]] <= (datos_angulos[i][1] + datos_angulos[i][2])):
                pdf.cell(w=38, h=8, txt=f"{datos_angulos[i][4]}", border=1, align= 'C', fill = 1)
            else:
                pdf.cell(w=38, h=8, txt=f"{datos_angulos[i][4]}", border=1, align= 'C', fill = 0)
            if((datos_angulos[i][0] in angulos) and angulos[datos_angulos[i][0]] > (datos_angulos[i][1] + datos_angulos[i][2])):
                pdf.multi_cell(w=39, h=8, txt=f"{datos_angulos[i][5]}", border=1, align= 'C', fill = 1)
            else:
                pdf.multi_cell(w=39, h=8, txt=f"{datos_angulos[i][5]}", border=1, align= 'C', fill = 0)
        
        pdf.multi_cell(w=0, h=10, txt=f"", border=0, align= 'L', fill = 0)
        pdf.set_font('times', 'B', 12)
        pdf.multi_cell(w=0, h=15, txt=f"Datos del Doctor: ", border=0, align= 'L', fill = 0)
        pdf.set_font('times', 'B', 10)
        nombre_doctor = self.ui.input_nombreD.text() if self.ui.input_nombreD.text() else '____________________________________'
        pdf.cell(w=pdf.w/2, h=11, txt=f"Nombre: {nombre_doctor}", border=0, align= 'L', fill = 0)
        cedula = self.ui.input_cedula.text() if self.ui.input_cedula.text() else '____________________________________'
        pdf.multi_cell(w=pdf.w/2, h=11, txt=f"Cédula: {cedula}", border=0, align= 'L', fill = 0)
        current_directory = os.path.dirname(os.path.abspath(__file__))
        if(len(planos) != 0):
            pdf.add_page()
            pdf.set_font('times', 'B', 12)
            pdf.multi_cell(w=0,h=16, txt="Trazado de planos cefalométricos", border=0, align= 'C', fill = 0)
            pdf.image(f"{current_directory}/tempTrazado.png", x=10, y=25, w=190, h=231)
        pdf.output(f"{current_directory}/tempInforme.pdf")
        return pdf


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


class PDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        current_datetime = datetime.now()
        datetime_string = current_datetime.strftime("%d-%m-%Y %H:%M:%S")
        self.cell(0,10, f'Fecha y Hora: {datetime_string}', 0, 0, 'R')


def delete_file_on_exit():
        current_directory = os.path.dirname(os.path.abspath(__file__))
        if os.path.isfile(f"{current_directory}/tempInforme.pdf"):
            os.remove(f"{current_directory}/tempInforme.pdf")
        if os.path.isfile(f"{current_directory}/tempTrazado.png"):
            os.remove(f"{current_directory}/tempTrazado.png")

def main():
    app = QApplication(sys.argv)
    desktop = app.desktop()
    size_screen = desktop.screenGeometry()
    print(size_screen.width(), size_screen.height())
    
    ventana = Aplicacion(size_screen.width(), size_screen.height())
    print(os.path.dirname(os.path.abspath(__file__)))
    atexit.register(delete_file_on_exit)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()