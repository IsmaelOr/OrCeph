import math

# Diccionarios puntos
puntos = {
    'S':(21,32),
    'N':(15,12),
    'N\'':(13,12),
    'Or':(13,11),
    'Pr':(15,17),
    'A':(32,64),
    'A\'':(17,13),
    'B':(43,54),
    'B\'':(15,65),
    'D':(13,67),
    'Pg':(54,14),
    'Pg\'':(24,76),
    'Me':(83,4),
    'Me\'':(19,12),
    'Gn':(83,4),
    'Gn\'':(19,12),
    'Go':(97,1),
    'Go\'':(19,12),
    'III':(54,4),
    'AII':(83,4),
    'IIS':(33,3),
    'AIS':(19,12),
    'OMI':(83,4),
    'OMS':(83,4),
    'St':(83,4),
    'LS':(83,4),
    'LI':(83,4),
    'ENP':(83,4),
    'ENA':(24,8),
    'Ar':(83,4),
    'Prn':(83,4),
    'Ba':(83,4),
    'Po':(7,2),
    'Pt':(83,4),
    'Co':(83,4),
    'G':(83,4),
    'G\'':(83,4),
    'Sn':(83,4),
    'Sn\'':(83,4),
    'Tm':(83,4),
    'Tr':(83,4),
}

puntosPrueba = {
    '1':(3,6),
    '2':(7,2),

    'P1':(5,2),
    'P2':(3,6),
    'P3':(3,5),

    "P1A":(-3,1),
    "P2A":(2,5),
    "P3A":(-1,-2),

    'P1C':(1,1),
    'P2C':(3,2),
    'P3C':(1,-2),
    'P4C':(4,-3),
}

planos = {}

angulos = {}

# Funciones
def calcularDistancia(punto1, punto2):
    return math.sqrt(math.pow(punto1[0] - punto2[0],2) + math.pow(punto1[1] - punto2[1],2))

def encontrarEcuacion(punto1, punto2):
    m =(punto2[1] - punto1[1] ) / (punto2[0] - punto1[0])
    b = m * (-punto1[0]) + punto1[1]
    return m, b

def encontrarPerpendicular(m1, b1, punto1):
    m2 = -1 / m1
    b2 = m2 * (-punto1[0]) + punto1[1]
    return m2, b2

def encontrarPuntoInterseccion(m1, b1, m2, b2):
    x = (b2- b1)/(m1 - m2)
    y = m1 * x + b1
    return int(x), int(y)

#Obtiene el angulo A
def  calcularAngulo(AB, BC, CA):
    numerador = (math.pow(CA, 2) + math.pow(AB, 2) - math.pow(BC,2))
    denominador = 2 * CA * AB
    division = numerador/denominador
    radianes = math.acos(division)
    return radianes * (180)/math.pi

def pruebaAngulo():
    AB = calcularDistancia(puntosPrueba['P1A'], puntosPrueba["P2A"])
    BC = calcularDistancia(puntosPrueba['P2A'], puntosPrueba["P3A"])
    CA = calcularDistancia(puntosPrueba['P3A'], puntosPrueba["P1A"])
    print(calcularAngulo(AB,BC,CA))
 
def encontrarAngulo(punto1, punto2, punto3, punto4):
    m1, b1 = encontrarEcuacion(punto1, punto2)
    m2, b2 = encontrarEcuacion(punto3, punto4)
    x, y = encontrarPuntoInterseccion(m1, b1, m2, b2)
    distanciaAB = calcularDistancia((x,y), punto2)
    distanciaBC = calcularDistancia(punto2,punto4)
    distanciaCA = calcularDistancia((x,y), punto4)
    return calcularAngulo(distanciaAB,distanciaBC,distanciaCA)

def calcularPlanos():
    if('Gn' in puntos):
        if('Go' in puntos):
            planos['PM (Go-Gn)'] = calcularDistancia(puntos['Gn'], puntos['Go'])

        if('Pt' in puntos):
            planos['Pt-Gn'] = calcularDistancia(puntos['Pt'], puntos['Gn'])

    if('N' in puntos):
        if('S' in puntos):
            planos['SN'] = calcularDistancia(puntos['S'], puntos['N'])

        if('A' in puntos):
            planos['NA'] = calcularDistancia(puntos['N'], puntos['A'])

            if('IIS' in puntos):
                m1, b1 = encontrarEcuacion(puntos['N'],puntos['A'])
                m2, b2 = encontrarPerpendicular(m1,b1, puntos['IIS'])
                x, y = encontrarPuntoInterseccion(m1, b1, m2, b2)
                P = (x, y)
                planos['IIS-NA'] = calcularDistancia(P, puntos['IIS'])

        if('B' in puntos):
            planos['NB'] = calcularDistancia(puntos['N'], puntos['B'])
            if('III' in puntos):
                m1, b1 = encontrarEcuacion(puntos['N'],puntos['B'])
                m2, b2 = encontrarPerpendicular(m1,b1, puntos['III'])
                x, y = encontrarPuntoInterseccion(m1, b1, m2, b2)
                P = (x, y)
                planos['III-NB'] = calcularDistancia(P, puntos['III'])

            if('Pg' in puntos):
                m1, b1 = encontrarEcuacion(puntos['N'],puntos['B'])
                m2, b2 = encontrarPerpendicular(m1,b1, puntos['Pg'])
                x, y = encontrarPuntoInterseccion(m1, b1, m2, b2)
                P = (x, y)
                planos['Pg-NB'] = calcularDistancia(P, puntos['Pg'])

        if('D' in puntos):
            planos['ND'] = calcularDistancia(puntos['N'], puntos['D'])

        if('Ba' in puntos):
            planos['N-Ba'] = calcularDistancia(puntos['N'], puntos['Ba'])

        if('Gn' in puntos):
            planos['N-Gn'] = calcularDistancia(puntos['N'], puntos['Gn'])
        
    if('S' in puntos):
        if('N' in puntos):
            m1, b1 = encontrarEcuacion(puntos['S'],puntos['N'])
            if('Pg' in puntos):
                m2, b2 = encontrarPerpendicular(m1,b1, puntos['Pg'])
                x, y = encontrarPuntoInterseccion(m1, b1, m2, b2)
                L = (x, y)
                planos['Silla-L'] = calcularDistancia(L, puntos['S'])
                
            if('Co' in puntos):
                m2, b2 = encontrarPerpendicular(m1,b1, puntos['Co'])
                x, y = encontrarPuntoInterseccion(m1, b1, m2, b2)
                E = (x, y)
                planos['Silla-E'] = calcularDistancia(E, puntos['S'])
    
    if('III' in puntos):
        if('AII' in puntos):
            planos['III-AII'] = calcularDistancia(puntos['III'], puntos['AII'])
            
        if('OMI' in puntos):
            planos['III-OMI'] = calcularDistancia(puntos['III'], puntos['OMI'])

    if('IIS' in puntos):
        if('AIS' in puntos):
            planos['IIS-AIS'] = calcularDistancia(puntos['IIS'], puntos['AII'])

    if('Po' in puntos):
        if('Or' in puntos):
            planos['Po-Or'] = calcularDistancia(puntos['Po'], puntos['Or'])
    
    if('Pg\'' in puntos):
        if('Prn' in puntos):
            planos['Linea S'] = calcularDistancia(puntos['Pg\''], puntos['Prn'])
            if('LS' in puntos):
                m1, b1 = encontrarEcuacion(puntos['Pg\''],puntos['Prn'])
                m2, b2 = encontrarPerpendicular(m1,b1, puntos['LS'])
                x, y = encontrarPuntoInterseccion(m1, b1, m2, b2)
                P = (x, y)
                planos['(Pg\'-Prn)-LS'] = calcularDistancia(P, puntos['LS'])

            if('LS' in puntos):
                m1, b1 = encontrarEcuacion(puntos['Pg\''],puntos['Prn'])
                m2, b2 = encontrarPerpendicular(m1,b1, puntos['LI'])
                x, y = encontrarPuntoInterseccion(m1, b1, m2, b2)
                P = (x, y)
                planos['(Pg\'-Prn)-LI'] = calcularDistancia(P, puntos['LI'])

    print(planos)
  
def calcularPlanos2(puntos, planos, main_window):
    if(puntos['Gn'] != None):
        if(puntos['Go'] != None):
            planos['PM'] = calcularDistancia(puntos['Gn'], puntos['Go'])
            main_window.photo.drawPlano(puntos['Gn'], puntos['Go'])

        if(puntos['Pt'] != None):
            planos['Pt-Gn'] = calcularDistancia(puntos['Pt'], puntos['Gn'])
            main_window.photo.drawPlano(puntos['Pt'], puntos['Gn'])

    if(puntos['N'] != None):
        if(puntos['S'] != None):
            planos['SN'] = calcularDistancia(puntos['S'], puntos['N'])
            main_window.photo.drawPlano(puntos['S'], puntos['N'])

        if(puntos['A'] != None):
            planos['NA'] = calcularDistancia(puntos['N'], puntos['A'])
            main_window.photo.drawPlano(puntos['N'], puntos['A'])

            if(puntos['IIS'] != None):
                m1, b1 = encontrarEcuacion(puntos['N'],puntos['A'])
                m2, b2 = encontrarPerpendicular(m1,b1, puntos['IIS'])
                x, y = encontrarPuntoInterseccion(m1, b1, m2, b2)
                P = (x, y)
                planos['IIS-NA'] = calcularDistancia(P, puntos['IIS'])
                main_window.photo.drawPlano(P, puntos['IIS'])

        if(puntos['B'] != None):
            planos['NB'] = calcularDistancia(puntos['N'], puntos['B'])
            main_window.photo.drawPlano(puntos['N'], puntos['B'])
            if(puntos['III'] != None):
                m1, b1 = encontrarEcuacion(puntos['N'],puntos['B'])
                m2, b2 = encontrarPerpendicular(m1,b1, puntos['III'])
                x, y = encontrarPuntoInterseccion(m1, b1, m2, b2)
                P = (x, y)
                planos['III-NB'] = calcularDistancia(P, puntos['III'])
                main_window.photo.drawPlano(P, puntos['III'])

            if(puntos['Pg'] != None):
                m1, b1 = encontrarEcuacion(puntos['N'],puntos['B'])
                m2, b2 = encontrarPerpendicular(m1,b1, puntos['Pg'])
                x, y = encontrarPuntoInterseccion(m1, b1, m2, b2)
                P = (x, y)
                planos['Pg-NB'] = calcularDistancia(P, puntos['Pg'])
                main_window.photo.drawPlano(P, puntos['Pg'])

        if(puntos['D'] != None):
            planos['ND'] = calcularDistancia(puntos['N'], puntos['D'])
            main_window.photo.drawPlano(puntos['N'], puntos['D'])

        if(puntos['Ba'] != None):
            planos['N-Ba'] = calcularDistancia(puntos['N'], puntos['Ba'])
            main_window.photo.drawPlano(puntos['N'], puntos['Ba'])

        if(puntos['Gn'] != None):
            planos['N-Gn'] = calcularDistancia(puntos['N'], puntos['Gn'])
            main_window.photo.drawPlano(puntos['N'], puntos['Gn'])
        
    if(puntos['S'] != None):
        if(puntos['N'] != None):
            m1, b1 = encontrarEcuacion(puntos['S'],puntos['N'])
            if(puntos['Pg'] != None):
                m2, b2 = encontrarPerpendicular(m1,b1, puntos['Pg'])
                x, y = encontrarPuntoInterseccion(m1, b1, m2, b2)
                L = (x, y)
                planos['Silla-L'] = calcularDistancia(L, puntos['S'])
                main_window.photo.drawPlano(L, puntos['S'])
                
            if(puntos['Co'] != None):
                m2, b2 = encontrarPerpendicular(m1,b1, puntos['Co'])
                x, y = encontrarPuntoInterseccion(m1, b1, m2, b2)
                E = (x, y)
                planos['Silla-E'] = calcularDistancia(E, puntos['S'])
                main_window.photo.drawPlano(E, puntos['S'])
    
    if(puntos['III'] != None):
        if(puntos['AII'] != None):
            planos['III-AII'] = calcularDistancia(puntos['III'], puntos['AII'])
            main_window.photo.drawPlano(puntos['III'], puntos['AII'])
            
        if(puntos['OMI'] != None):
            planos['III-OMI'] = calcularDistancia(puntos['III'], puntos['OMI'])
            main_window.photo.drawPlano(puntos['III'], puntos['OMI'])

    if(puntos['IIS'] != None):
        if('AIS' in puntos):
            planos['IIS-AIS'] = calcularDistancia(puntos['IIS'], puntos['AII'])
            main_window.photo.drawPlano(puntos['IIS'], puntos['AII'])

    if(puntos['Po'] != None):
        if('Or' in puntos):
            planos['Po-Or'] = calcularDistancia(puntos['Po'], puntos['Or'])
            main_window.photo.drawPlano(puntos['Po'], puntos['Or'])
    
    if(puntos['Pg\''] != None):
        if(puntos['Prn'] != None):
            planos['Linea S'] = calcularDistancia(puntos['Pg\''], puntos['Prn'])
            main_window.photo.drawPlano(puntos['Pg\''], puntos['Prn'])
            if(puntos['LS'] != None):
                m1, b1 = encontrarEcuacion(puntos['Pg\''],puntos['Prn'])
                m2, b2 = encontrarPerpendicular(m1,b1, puntos['LS'])
                x, y = encontrarPuntoInterseccion(m1, b1, m2, b2)
                P = (x, y)
                planos['(Pg\' - Prn) - LS'] = calcularDistancia(P, puntos['LS'])
                main_window.photo.drawPlano(P, puntos['LS'])

            if(puntos['LS'] != None):
                m1, b1 = encontrarEcuacion(puntos['Pg\''],puntos['Prn'])
                m2, b2 = encontrarPerpendicular(m1,b1, puntos['LI'])
                x, y = encontrarPuntoInterseccion(m1, b1, m2, b2)
                P = (x, y)
                planos['(Pg\' - Prn) - LI'] = calcularDistancia(P, puntos['LI'])
                main_window.photo.drawPlano(P, puntos['LI'])

    # print(planos)
    return planos;

def calcularAngulos():
    angulosContador = 0
    if('SN' in planos):
        if('NA' in planos):
            distanciaSA = calcularDistancia(puntos['A'], puntos['S'])
            # El punto de steiner N será el punto A de la función
            angulos['SNA'] = calcularAngulo(planos['SN'], distanciaSA, planos['NA'])

            angulosContador += 1
        if('NB' in planos):
            distanciaSB = calcularDistancia(puntos['B'], puntos['S'])
            # El punto de steiner N será el punto A de la función
            angulos['SNB'] = calcularAngulo(planos['SN'], distanciaSB, planos['NB'])
            angulosContador += 1
        if('ND' in planos):
            distanciaSD = calcularDistancia(puntos['D'], puntos['S'])
            # El punto de steiner N será el punto A de la función
            angulos['SND'] = calcularAngulo(planos['SN'], distanciaSD, planos['ND'])
            angulosContador += 1
        if('III' in puntos and 'OMI' in puntos):
            angulos['PO-SN'] = encontrarAngulo(puntos['S'], puntos['N'],puntos['OMI'], puntos['III'] )
            angulosContador += 1
        if('Go' in puntos and 'Gn' in puntos):
            angulos['(Go-Gn)-(S-N)'] = encontrarAngulo(puntos['S'], puntos['N'],puntos['Go'], puntos['Gn'] )
            angulosContador += 1

    if('NA' in planos):
        if('III-AII' in planos):
            m1, b1 = encontrarEcuacion(puntos['N'], puntos['A'])
            m2, b2 = encontrarEcuacion(puntos['III'], puntos['AII'])
            x, y = encontrarPuntoInterseccion(m1, b1, m2, b2)
            punto1 = (x, y)
            punto2y = m1 * (x + .1) + b1
            punto2 = (x + .1, punto2y)

            distanciaInterseccionAII = calcularDistancia(punto1, puntos['AII'])
            distanciaAIIpunto2 =  calcularDistancia(punto2, puntos['AII'])
            distanciaInterseccionPunto2 = calcularDistancia(punto1, punto2)
            angulos['(III-AII)-(N-A)'] = calcularAngulo(distanciaInterseccionAII, distanciaAIIpunto2, distanciaInterseccionPunto2)
            angulosContador += 1
            
        if('NB' in planos):
            distanciaAB = calcularDistancia(puntos['A'], puntos['B'])
            # El punto de steiner N será el punto A de la función
            angulos['ANB'] = calcularAngulo(planos['NA'], distanciaAB, planos['NB'])
            angulosContador += 1

    if('IIS-AIS' in planos):
        if('NA' in planos):
            angulos['(IIS-AIS)-(N-A)'] = encontrarAngulo(puntos['IIS'], puntos['AIS'], puntos['A'], puntos['N'])
            angulosContador += 1
        if('NB' in planos):
            angulos['(IIS-AIS)-(N-B)'] = encontrarAngulo(puntos['IIS'], puntos['AIS'], puntos['B'], puntos['N'])
            angulosContador += 1
    
    if('III-AII' in planos):
        if('IIS-AIS' in planos):
            angulos['(III-AII)- (IIS-AIS)'] = encontrarAngulo(puntos['III'], puntos['AII'], puntos['IIS'], puntos['AIS'])
            angulosContador += 1
        if('NB' in planos):
            angulos['(III-AII)- (N-B)'] = encontrarAngulo(puntos['III'], puntos['AII'], puntos['N'], puntos['B'])
            angulosContador += 1
    if('PM (Go-Gn)' in planos):
        if('ENP' in puntos and 'ENA' in puntos):
            angulos['(ENA-ENP)-(Go-Gn)'] = encontrarAngulo(puntos['ENP'], puntos['ENA'], puntos['Go'], puntos['Gn'])
            angulosContador += 1
        if('Po-Or' in planos):
            angulos['(Po-Or)-(Go-Gn)'] = encontrarAngulo(puntos['Po'], puntos['Or'], puntos['Go'], puntos['Gn'])
            angulosContador += 1
        if('A' in puntos and 'B' in puntos):
            angulos['(A-B)-(Go-Gn)'] = encontrarAngulo(puntos['Gn'], puntos['Go'], puntos['B'], puntos['A'])
            angulosContador += 1
        
    if('Ar' in puntos and 'Go' in puntos and 'Me' in puntos):
        distanciaArGo = calcularDistancia(puntos['Go'], puntos['Ar'])
        distanciaMeAr = calcularDistancia(puntos['Me'], puntos['Ar'])
        distanciaGoMe = calcularDistancia(puntos['Go'], puntos['Me'])
        angulos['(Ar-Go)-(Go-Me)'] = calcularAngulo(distanciaArGo, distanciaMeAr, distanciaGoMe)
        angulosContador += 1
 
    print(angulos)
    print(angulosContador)
    print(len(angulos))

def calcularAngulos2(puntos,planos,angulos, main_window):
    angulosContador = 0
    if('SN' in planos):
        if('NA' in planos):
            distanciaSA = calcularDistancia(puntos['A'], puntos['S'])
            # El punto de steiner N será el punto A de la función
            angulos['SNA'] = calcularAngulo(planos['SN'], distanciaSA, planos['NA'])
            main_window.photo.drawAngulo(puntos['S'], puntos['N'], puntos['A'])
            angulosContador += 1
        if('NB' in planos):
            distanciaSB = calcularDistancia(puntos['B'], puntos['S'])
            # El punto de steiner N será el punto A de la función
            angulos['SNB'] = calcularAngulo(planos['SN'], distanciaSB, planos['NB'])
            main_window.photo.drawAngulo(puntos['S'], puntos['N'], puntos['B'])
            angulosContador += 1
        if('ND' in planos):
            distanciaSD = calcularDistancia(puntos['D'], puntos['S'])
            # El punto de steiner N será el punto A de la función
            angulos['SND'] = calcularAngulo(planos['SN'], distanciaSD, planos['ND'])
            angulosContador += 1
        if(puntos['III'] != None and puntos['OMI'] != None):
            angulos['PO-SN'] = encontrarAngulo(puntos['S'], puntos['N'],puntos['OMI'], puntos['III'] )
            angulosContador += 1
        if(puntos['Go'] != None and puntos['Gn'] != None):
            angulos['(Go-Gn)-(S-N)'] = encontrarAngulo(puntos['S'], puntos['N'],puntos['Go'], puntos['Gn'] )
            angulosContador += 1
    if('NA' in planos):
        if('NB' in planos):
            distanciaAB = calcularDistancia(puntos['A'], puntos['B'])
            # El punto de steiner N será el punto A de la función
            angulos['ANB'] = calcularAngulo(planos['NA'], distanciaAB, planos['NB'])
            angulosContador += 1

    if('IIS-AIS' in planos):
        if('NA' in planos):
            angulos['(IIS-AIS)-(N-A)'] = encontrarAngulo(puntos['IIS'], puntos['AIS'], puntos['A'], puntos['N'])
            angulosContador += 1
        if('NB' in planos):
            angulos['(IIS-AIS)-(N-B)'] = encontrarAngulo(puntos['IIS'], puntos['AIS'], puntos['B'], puntos['N'])
            angulosContador += 1
    
    if('III-AII' in planos):
        if('IIS-AIS' in planos):
            angulos['(III-AII)- (IIS-AIS)'] = encontrarAngulo(puntos['III'], puntos['AII'], puntos['IIS'], puntos['AIS'])
            angulosContador += 1
        if('NB' in planos):
            angulos['(III-AII)- (N-B)'] = encontrarAngulo(puntos['III'], puntos['AII'], puntos['N'], puntos['B'])
            angulosContador += 1

    return angulos

#Pruebas
#print(calcularDistancia(puntosPrueba['1'],puntosPrueba['2']))

#m, b = encontrarEcuacion(puntosPrueba['P1'],puntosPrueba['P2'])
#print(m, b)

#m2, b2 = encontrarPerpendicular(3, -4,puntosPrueba['P3'])
#print(m2, b2)

#print(encontrarPuntoInterseccion(3,-4,m2, b2))

#pruebaAngulo()
#print(calcularAngulo(6.4,7.6,3.6))

#print(encontrarAngulo(puntosPrueba['P1C'],puntosPrueba['P2C'],puntosPrueba['P3C'],puntosPrueba['P4C']))

calcularPlanos()
calcularAngulos()