from fpdf import FPDF
from datetime import datetime


analisis_esqueletico = [
    ['SNA', 82, 2, 'Prognatismo', 'Normal', 'Retrognatismo'],
    ['(ENA-ENP)-(Go-Gn)', 5, 2, 'Inclinación mordida abierta', 'Normal', 'Inclinación mordida cerrada'],
    ['SNB', 80, 2, 'Prognatismo', 'Normal', 'Retrognatismo'],
    ['SND', 77, 2, 'Progenismo', 'Normal', 'Retrogenismo'],
    ['Silla-L', 51, 2, 'Posición adelatanda mandíbula', 'Ortognático', 'Posición atrasada mandíbula'],
    ['Silla-E', 22, 2, 'Posición atrasada del condílo', 'Ortognática', 'Posición adelantada del cóndilo'],
    ['(Ar-Go)-(Go-Me)', 125, 5, 'Crecimiento vertical', 'Mesofacial', 'Crecimiento horizontal'],
    ['(Go-Gn)-(S-N)', 32, 2, 'Crecimiento vertical', 'Mesofacial', 'Crecimiento horizontal'],
    ['ANB', 2, 2, 'Clase III', 'Clase I', 'Clase II'],
    ['(A-B)-(Go-Gn)', 74, 2, 'Mordida abierta', 'Normal', 'Mordida cerrada']
]

analisis_dental = [
    ['(IIS-AIS)-(S-N)', 104, 2, 'Vestibuloversión', 'Normal', 'Linguoversión'],
    ['(IIS-AIS)-(N-A)', 22, 2, 'Proinclinación incisiva', 'Normal', 'Retroinclinación incisiva'],
    ['IIS-NA', 4, 1, 'Retrusión del incisivo superior', 'Posición normal', 'Protrusión del incisivo superior'],
    ['(III-AII)-(N-B)', 25, 2, 'Vestibulogresión', 'Normal', 'Linguogresión'],
    ['III-NB', 4, 1, 'Retrusión del incisivo inferior', 'Posición normal', 'Protrusión del incisivo inferior'],
    ['PO-SN', 14, 2, 'Mordida abierta', 'Normal', 'Mordida cerrada'],
    ['(III-AII)-(IIS-AIS)', 130,5, 'Protusión dentaria', 'Normal', 'Mordida cerrada'],
    ['Pg-(NB)', 4, 1, 'Sínfisis mandibular retruida', 'Sínfisis normal', 'Sínfisis mandibular protruida']
]

analisis_tejidos = [
    ['(Pg\'-Prn)-LI', 'Linea S (LI)',0, 1, 'Retroquelia', 'Normal', 'Proquelia'],
    ['(Pg\'-Prn)-LS', 'Linea S (LS)',0, 1, 'Retroquelia', 'Normal', 'Proquelia']
]

analisis_facial = [
    ['Tr-G', 'G-Sn', 'Sn-Me', 'N-Me', 'N-Sn', 'Sn-Me','Sn-St', 'St-Me', 'Sn-Me', 'LS-LI'],
    ['', '', '', '100%', '43%', '57%', '1/3', '2/3', '3/3', '3mm±1']
]


class PDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        current_datetime = datetime.now()
        datetime_string = current_datetime.strftime("%d-%m-%Y %H:%M:%S")
        self.cell(0,10, f'Fecha y Hora: {datetime_string}', 0, 0, 'R')

pdf = PDF(orientation='P', unit='mm', format='A4')
# PORTADA
pdf.add_page()
pdf.set_font('times', 'B', 10)
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
    pdf.cell(w=20, h=altura, txt=f"", border=1, align= 'C', fill = 0)
    pdf.cell(w=38, h=altura, txt=f"{analisis_esqueletico[i][3]}", border=1, align= 'C', fill = 0)
    pdf.cell(w=23, h=altura, txt=f"{analisis_esqueletico[i][4]}", border=1, align= 'C', fill = 0)
    pdf.multi_cell(w=39, h=altura, txt=f"{analisis_esqueletico[i][5]}", border=1, align= 'C', fill = 0)
pdf.set_xy(x,y1+10)
pdf.multi_cell(w=25, h=5, txt="Posición y tamaño mandibular", border=0, align= 'C', fill = 0)
pdf.set_xy(x,y1)
pdf.multi_cell(w=25, h=30, txt="", border=1, align= 'C', fill = 0)
pdf.multi_cell(w=25, h=5, txt="Relación sagital maxilomandibular", border=1, align= 'C', fill = 0)
pdf.multi_cell(w=25, h=5, txt="Posición vertical maxilomandibular", border=1, align= 'C', fill = 0)

pdf.multi_cell(w=0, h=5, txt="", border=0, fill=0)

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
    pdf.cell(w=20, h=altura, txt=f"", border=1, align= 'C', fill = 0)
    pdf.cell(w=38, h=altura, txt=f"{analisis_dental[i][3]}", border=1, align= 'C', fill = 0)
    pdf.cell(w=23, h=altura, txt=f"{analisis_dental[i][4]}", border=1, align= 'C', fill = 0)
    pdf.multi_cell(w=39, h=altura, txt=f"{analisis_dental[i][5]}", border=1, align= 'C', fill = 0)
pdf.set_xy(x,y1)
pdf.multi_cell(w=25, h=15, txt="", border=1, align= 'C', fill = 0)

pdf.set_xy(x,y+5)
pdf.multi_cell(w=25, h=5, txt="Incisivos con respecto a bases óseas", border=0, align= 'C', fill = 0)

pdf.set_xy(x,y1+2.5)
pdf.multi_cell(w=25, h=5, txt="Relación dentaria mentón óseo", border=0, align= 'C', fill = 0)

pdf.set_xy(x,y1+15)

pdf.multi_cell(w=0, h=5, txt="", border=0, fill=0)

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
    pdf.cell(w=20, h=altura, txt=f"", border=1, align= 'C', fill = 0)
    pdf.cell(w=38, h=altura, txt=f"{analisis_tejidos[i][4]}", border=1, align= 'C', fill = 0)
    pdf.cell(w=23, h=altura, txt=f"{analisis_tejidos[i][5]}", border=1, align= 'C', fill = 0)
    pdf.multi_cell(w=39, h=altura, txt=f"{analisis_tejidos[i][6]}", border=1, align= 'C', fill = 0)

pdf.multi_cell(w=0, h=5, txt="", border=0, fill=0)

## Analisis facial

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
    pdf.multi_cell(w=20, h=5, txt=f"", border=1, align= 'C', fill = 0)

pdf.set_xy(x+90, y)
pdf.cell(w=50, h=15, txt=f"Simétrico", border=1, align= 'C', fill = 0)
pdf.multi_cell(w=50, h=15, txt=f"Asimétrico", border=1, align= 'C', fill = 0)

pdf.set_x(x+90)
pdf.cell(w=33, h=15, txt=f"Los tercios coinciden", border=1, align= 'C', fill = 0)
pdf.multi_cell(w=33, h=5, txt=f"El tercio superior esta aumentado y el inferior disminuido", border=1, align= 'C', fill = 0)
pdf.set_xy(x+156, pdf.get_y()-15)
pdf.multi_cell(w=34, h=5, txt=f"El tercio superior esta disminuido y el inferior aumentado", border=1, align= 'C', fill = 0)

pdf.set_x(x+90)
pdf.cell(w=33, h=15, txt=f"Los tercios coinciden", border=1, align= 'C', fill = 0)
pdf.multi_cell(w=33, h=5, txt=f"El tercio superior esta aumentado y el inferior disminuido", border=1, align= 'C', fill = 0)
pdf.set_xy(x+156, pdf.get_y()-15)
pdf.multi_cell(w=34, h=5, txt=f"El tercio superior esta disminuido y el inferior aumentado", border=1, align= 'C', fill = 0)

pdf.set_x(x+90)
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




pdf.output("tempInforme.pdf")