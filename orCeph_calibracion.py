import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
from orCeph_interfaz import Ui_MainWindow
from functools import partial
from fpdf import FPDF
from moduloSteiner import calcularPlanos2, calcularAngulos2

class Aplicacion(QMainWindow):
    def __init__(self, width, height):
        super().__init__()
        
        self.inicializar_gui(width, height)

    def inicializar_gui(self, width, height):
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
        self.ui.btn_verAngulos.clicked.connect(self.ui.photo.showAngulos)
        self.ui.btn_verPuntos.clicked.connect(self.ui.photo.showPuntos)
        self.ui.btn_descargarTrazado.clicked.connect(self.downloadTrazado)
        self.ui.btn_descargarInforme.clicked.connect(partial(self.crearInforme, self.ui.puntosSteiner, self.ui.planos, self.ui.angulos))
        self.show()

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
        self.ui.btn_verPuntos.setEnabled(True)
        self.ui.btn_verAngulos.setEnabled(True)
        self.ui.btn_verPlanos.setEnabled(True)
        self.ui.btn_descargarTrazado.setEnabled(True)
        #informe_pdf = self.crearInforme(self.ui.puntosSteiner, self.ui.planos, self.ui.angulos)
        self.ui.btn_descargarInforme.setEnabled(True)

    def crearInforme(self,puntos, planos, angulos):
        datos_planos = [
            'PM (Go-Gn)', 'SN', 'NA', 'NB', 'ND', 'III-AII', 'IIS-AIS', 'N-Ba', 'Po-Or', 'Pt-Gn', 'N-Gn', 'III-OMI', 'Pg\'-Prn', 
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
            ['PO-SN', 14, 1, 'Mordida abierta', 'Normal', 'Mordida cerrada'],
            ['(Go-Gn)-(S-N)', 32, 1, 'Crecimiento vertical', 'Mesofacial', 'Crecimiento horizontal'],
            ['(IIS-AIS)-(N-A)', 22, 1, 'Proinclinación Incisiva', 'Normal', 'Retroinclinación Incisiva'],
            ['(III-AII)-(N-A)', 25, 1, 'Proinclinación Incisiva', 'Normal', 'Retroinclinación Incisiva'],
            ['(III-AII)-(IIS-AIS)', 130,1, 'Protusión dentaria', 'Normal', 'Mordida cerrada'],
            ['(A-B)-(Go-Gn)', 74, 2, 'Mordida abierta', 'Normal', 'Mordida cerrada'],
            ['(IIS-AIS)-(N-B)', 22, 1, 'Vestibuloversión', 'Normal', 'Linguoversión'],
            ['(III-AII)-(N-B)', 25,1, 'Vestibulogresión', 'Normal', 'Linguogresión'],
            ['(Ar-Go)-(Go-Me)', 130, 5, 'Crecimiento vertical', 'Mesofacial', 'Crecimiento horizontal'],
            ['(ENA-ENP)-(Go-Gn)', 5,2, 'Inclinación mordida abierta', 'Normal', 'Inclinación mordida cerrada'],
            ['(Po-Or)-(Go-Gn)', 1, 6, 'Inclinación mordida cerrada', 'Normal', 'Inclinación mordida abierta']
        ]
        
        print(f'Creando PDF')
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_font('times', '', 8)
        pdf.multi_cell(w=0, h=10, txt="Planos o Segmentos cefalométricos", border=1, align= 'C', fill = 0)
        pdf.cell(w=10, h=10, txt="Número", border=1, align= 'C', fill = 0)
        pdf.cell(w=25, h=10, txt="Plano", border=1, align= 'C', fill = 0)
        pdf.cell(w=20, h=10, txt="Valor Normal", border=1, align= 'C', fill = 0)
        pdf.cell(w=20, h=10, txt="Valor Calculado", border=1, align= 'C', fill = 0)
        pdf.multi_cell(w=0,h=5, txt="Diagnostico", border=1, align= 'C', fill = 0)
        pdf.cell(w=75, h=5, txt="", border=0, align= 'C', fill = 0)
        pdf.cell(w=38, h=5, txt="Disminuido", border=1, align= 'C', fill = 0)
        pdf.cell(w=38, h=5, txt="Normal", border=1, align= 'C', fill = 0)
        pdf.multi_cell(w=39, h=5, txt="Aumentado", border=1, align= 'C', fill = 0)
        for i in range(0,13):
            pdf.cell(w=10, h=8, txt=f"{i+1}", border=1, align= 'C', fill = 0)
            pdf.cell(w=25, h=8, txt=f"{datos_planos[i]}", border=1, align= 'C', fill = 0)
            pdf.cell(w=20, h=8, txt=f"-", border=1, align= 'C', fill = 0)
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
        pdf.add_page()
        pdf.multi_cell(w=0, h=10, txt="Ángulos cefalométricos", border=1, align= 'C', fill = 0)
        pdf.cell(w=10, h=10, txt="Número", border=1, align= 'C', fill = 0)
        pdf.cell(w=25, h=10, txt="Ángulo", border=1, align= 'C', fill = 0)
        pdf.cell(w=20, h=10, txt="Valor Normal", border=1, align= 'C', fill = 0)
        pdf.cell(w=20, h=10, txt="Valor Calculado", border=1, align= 'C', fill = 0)
        pdf.multi_cell(w=0,h=5, txt="Diagnostico", border=1, align= 'C', fill = 0)
        pdf.cell(w=75, h=5, txt="", border=0, align= 'C', fill = 0)
        pdf.cell(w=38, h=5, txt="Disminuido", border=1, align= 'C', fill = 0)
        pdf.cell(w=38, h=5, txt="Normal", border=1, align= 'C', fill = 0)
        pdf.multi_cell(w=39, h=5, txt="Aumentado", border=1, align= 'C', fill = 0)
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
        filepath, _ = QFileDialog.getSaveFileName(self, 'Guardar Informe de Resultados', 'Informe de Resultados', 'PDF (*.pdf)')
        if(filepath):
            pdf.output(filepath)


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