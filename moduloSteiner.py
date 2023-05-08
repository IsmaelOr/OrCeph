import math

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
    return x, y

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
    'Go':(83,4),
    'Go\'':(19,12),
    'III':(54,4),
    'AII':(83,4),
    'IIS':(83,4),
    'AIS':(19,12),
    'OMI':(83,4),
    'OMS':(83,4),
    'St':(83,4),
    'LS':(83,4),
    'LI':(83,4),
    'ENP':(83,4),
    'ENA':(83,4),
    'Ar':(83,4),
    'Prn':(83,4),
    'Ba':(83,4),
    'Po':(83,4),
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
    "P3A":(-1,-2)
}

planos = {}

angulos = {}

def calcularPlanos():
    planosContador = 0
    
    if('Gn' in puntos):
        if('Go' in puntos):
            planos['PM'] = calcularDistancia(puntos['Gn'], puntos['Go'])
            planosContador  += 1

        if('Pt' in puntos):
            planos['Pt-Gn'] = calcularDistancia(puntos['Pt'], puntos['Gn'])
            planosContador  += 1

    if('N' in puntos):
        if('S' in puntos):
            planos['SN'] = calcularDistancia(puntos['S'], puntos['N'])
            planosContador  += 1

        if('A' in puntos):
            planos['NA'] = calcularDistancia(puntos['N'], puntos['A'])
            planosContador  += 1

            if('IIS' in puntos):
                m1, b1 = encontrarEcuacion(puntos['N'],puntos['A'])
                m2, b2 = encontrarPerpendicular(m1,b1, puntos['IIS'])
                x, y = encontrarPuntoInterseccion(m1, b1, m2, b2)
                P = (x, y)
                planos['IIS-NA'] = calcularDistancia(P, puntos['IIS'])
                planosContador  += 1

        if('B' in puntos):
            distancia = calcularDistancia(puntos['N'], puntos['B'])
            planos['NB'] = distancia
            planosContador  += 1
            if('III' in puntos):
                m1, b1 = encontrarEcuacion(puntos['N'],puntos['B'])
                m2, b2 = encontrarPerpendicular(m1,b1, puntos['III'])
                x, y = encontrarPuntoInterseccion(m1, b1, m2, b2)
                P = (x, y)
                planos['III-NB'] = calcularDistancia(P, puntos['III'])
                planosContador  += 1

            if('Pg' in puntos):
                m1, b1 = encontrarEcuacion(puntos['N'],puntos['B'])
                m2, b2 = encontrarPerpendicular(m1,b1, puntos['Pg'])
                x, y = encontrarPuntoInterseccion(m1, b1, m2, b2)
                P = (x, y)
                planos['Pg-NB'] = calcularDistancia(P, puntos['Pg'])
                planosContador  += 1

        if('D' in puntos):
            planos['ND'] = calcularDistancia(puntos['N'], puntos['D'])
            planosContador  += 1

        if('Ba' in puntos):
            planos['N-Ba'] = calcularDistancia(puntos['N'], puntos['Ba'])
            planosContador  += 1

        if('Gn' in puntos):
            planos['N-Gn'] = calcularDistancia(puntos['N'], puntos['Gn'])
            planosContador  += 1
        
    if('S' in puntos):
        if('N' in puntos):
            m1, b1 = encontrarEcuacion(puntos['S'],puntos['N'])
            if('Pg' in puntos):
                m2, b2 = encontrarPerpendicular(m1,b1, puntos['Pg'])
                x, y = encontrarPuntoInterseccion(m1, b1, m2, b2)
                L = (x, y)
                planos['Silla-L'] = calcularDistancia(L, puntos['S'])
                planosContador  += 1
                
            if('Co' in puntos):
                m2, b2 = encontrarPerpendicular(m1,b1, puntos['Co'])
                x, y = encontrarPuntoInterseccion(m1, b1, m2, b2)
                E = (x, y)
                planos['Silla-E'] = calcularDistancia(E, puntos['S'])
                planosContador  += 1
    
    if('III' in puntos):
        if('AII' in puntos):
            planos['III-AII'] = calcularDistancia(puntos['III'], puntos['AII'])
            planosContador  += 1
            
        if('OMI' in puntos):
            planos['III-OMI'] = calcularDistancia(puntos['III'], puntos['OMI'])
            planosContador  += 1

    if('IIS' in puntos):
        if('AIS' in puntos):
            planos['IIS-AIS'] = calcularDistancia(puntos['IIS'], puntos['AII'])
            planosContador  += 1

    if('Po' in puntos):
        if('Or' in puntos):
            planos['Po-Or'] = calcularDistancia(puntos['Po'], puntos['Or'])
            planosContador  += 1
    
    if('Pg\'' in puntos):
        if('Prn' in puntos):
            planos['Linea S'] = calcularDistancia(puntos['Pg\''], puntos['Prn'])
            planosContador  += 1
            if('LS' in puntos):
                m1, b1 = encontrarEcuacion(puntos['Pg\''],puntos['Prn'])
                m2, b2 = encontrarPerpendicular(m1,b1, puntos['LS'])
                x, y = encontrarPuntoInterseccion(m1, b1, m2, b2)
                P = (x, y)
                planos['(Pg\' - Prn) - LS'] = calcularDistancia(P, puntos['LS'])
                planosContador  += 1

            if('LS' in puntos):
                m1, b1 = encontrarEcuacion(puntos['Pg\''],puntos['Prn'])
                m2, b2 = encontrarPerpendicular(m1,b1, puntos['LI'])
                x, y = encontrarPuntoInterseccion(m1, b1, m2, b2)
                P = (x, y)
                planos['(Pg\' - Prn) - LI'] = calcularDistancia(P, puntos['LI'])
                planosContador  += 1

    print(planos)
    print(len(planos))
    print(planosContador)

def calcularAngulos():
    if('SN' in planos):
        if('NA' in planos):
            if('S' in puntos):
                distanciaSA = calcularDistancia(puntos['A'], puntos['S'])
                # El punto de steiner N será el punto A de la función
                angulos['SNA'] = calcularAngulo(planos['SN'], distanciaSA, planos['NA'])


#Pruebas
#print(calcularDistancia(puntosPrueba['1'],puntosPrueba['2']))

#m, b = encontrarEcuacion(puntosPrueba['P1'],puntosPrueba['P2'])
#print(m, b)

#m2, b2 = encontrarPerpendicular(3, -4,puntosPrueba['P3'])
#print(m2, b2)

#print(encontrarPuntoInterseccion(3,-4,m2, b2))

#pruebaAngulo()
#print(calcularAngulo(6.4,7.6,3.6))


calcularPlanos()