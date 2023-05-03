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

# Diccionarios puntos
puntosSteiner = {
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
    'P3':(3,5)
}

def calcularPlanos():
    planosContador = 0
    planos = {}
    if('Gn' in puntosSteiner):
        if('Go' in puntosSteiner):
            distancia = calcularDistancia(puntosSteiner['Gn'], puntosSteiner['Go'])
            planos['PM'] = distancia
            planosContador  += 1

        if('Pt' in puntosSteiner):
            distancia = calcularDistancia(puntosSteiner['Pt'], puntosSteiner['Gn'])
            planos['Pt-Gn'] = distancia
            planosContador  += 1

    if('N' in puntosSteiner):
        if('S' in puntosSteiner):
            distancia = calcularDistancia(puntosSteiner['S'], puntosSteiner['N'])
            planos['SN'] = distancia
            planosContador  += 1

        if('A' in puntosSteiner):
            distancia = calcularDistancia(puntosSteiner['N'], puntosSteiner['A'])
            planos['NA'] = distancia
            planosContador  += 1

        if('B' in puntosSteiner):
            distancia = calcularDistancia(puntosSteiner['N'], puntosSteiner['B'])
            planos['NB'] = distancia
            planosContador  += 1

        if('D' in puntosSteiner):
            distancia = calcularDistancia(puntosSteiner['N'], puntosSteiner['D'])
            planos['ND'] = distancia
            planosContador  += 1

        if('Ba' in puntosSteiner):
            distancia = calcularDistancia(puntosSteiner['N'], puntosSteiner['Ba'])
            planos['N-Ba'] = distancia
            planosContador  += 1

        if('Gn' in puntosSteiner):
            distancia = calcularDistancia(puntosSteiner['N'], puntosSteiner['Gn'])
            planos['N-Gn'] = distancia
            planosContador  += 1

    if('S' in puntosSteiner):
        if('N' in puntosSteiner):
            m1, b1 = encontrarEcuacion(puntosSteiner['S'],puntosSteiner['N'])
            if('Pg' in puntosSteiner):
                m2, b2 = encontrarPerpendicular(m1,b1, puntosSteiner['Pg'])
                x, y = encontrarPuntoInterseccion(m1, b1, m2, b2)
                L = (x, y)
                distancia = calcularDistancia(L, puntosSteiner['S'])
                planos['Silla-L'] = distancia
                planosContador  += 1
                
            if('Co' in puntosSteiner):
                m2, b2 = encontrarPerpendicular(m1,b1, puntosSteiner['Co'])
                x, y = encontrarPuntoInterseccion(m1, b1, m2, b2)
                E = (x, y)
                distancia = calcularDistancia(E, puntosSteiner['S'])
                planos['Silla-E'] = distancia
                planosContador  += 1

    if('III' in puntosSteiner):
        if('AII' in puntosSteiner):
            distancia = calcularDistancia(puntosSteiner['III'], puntosSteiner['AII'])
            planos['III-AII'] = distancia
            planosContador  += 1
            
        if('OMI' in puntosSteiner):
            distancia = calcularDistancia(puntosSteiner['III'], puntosSteiner['OMI'])
            planos['III-OMI'] = distancia
            planosContador  += 1

    if('IIS' in puntosSteiner):
        if('AIS' in puntosSteiner):
            distancia = calcularDistancia(puntosSteiner['IIS'], puntosSteiner['AII'])
            planos['IIS-AIS'] = distancia
            planosContador  += 1

    if('Po' in puntosSteiner):
        if('Or' in puntosSteiner):
            distancia = calcularDistancia(puntosSteiner['Po'], puntosSteiner['Or'])
            planos['Po-Or'] = distancia
            planosContador  += 1
    
    if('Pg\'' in puntosSteiner):
        if('Sn\'' in puntosSteiner):
            distancia = calcularDistancia(puntosSteiner['Pg\''], puntosSteiner['Sn\''])
            planos['Linea S'] = distancia
            planosContador  += 1

    print(planos)
    print(len(planos))
    print(planosContador)

#Pruebas
#print(calcularDistancia(puntosPrueba['1'],puntosPrueba['2']))

#m, b = encontrarEcuacion(puntosPrueba['P1'],puntosPrueba['P2'])
#print(m, b)

#m2, b2 = encontrarPerpendicular(3, -4,puntosPrueba['P3'])
#print(m2, b2)

#print(encontrarPuntoInterseccion(3,-4,m2, b2))

calcularPlanos()