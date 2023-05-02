import math

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
    'Tr':(83,4)
}

puntosPrueba = {
    '1':(3,6),
    '2':(7,2)
}


def calcularDistancias():
    puntos = 0
    distancias = {
    }
    if('Gn' in puntosSteiner):
        if('Go' in puntosSteiner):
            distancia = calcularDistancia('Gn', 'Go')
            puntosSteiner['PM'] = distancia
            puntos  += 1

        if('Pt' in puntosSteiner):
            distancia = calcularDistancia('Pt', 'Gn')
            puntosSteiner['Pt-Gn'] = distancia
            puntos  += 1

    if('N' in puntosSteiner):
        if('S' in puntosSteiner):
            distancia = calcularDistancia('Pt', 'Gn')
            puntosSteiner['Pt-Gn'] = distancia
            print('SN')
            puntos  += 1

        if('A' in puntosSteiner):
            print('NA')
            puntos  += 1

        if('B' in puntosSteiner):
            print('NB')
            puntos  += 1

        if('D' in puntosSteiner):
            print('ND')
            puntos  += 1

        if('Ba' in puntosSteiner):
            print('N-Ba')
            puntos  += 1

        if('Gn' in puntosSteiner):
            print('N-Gn')
            puntos  += 1


    #Estos falta por entender
    if('S' in puntosSteiner):
        if('L' in puntosSteiner):
            print("Silla-L")
            puntos  += 1

        if('E' in puntosSteiner):
            print("Silla-E")
            puntos  += 1

    if('III' in puntosSteiner):
        if('AII' in puntosSteiner):
            print("III-AII")
            puntos  += 1

        if('OMI' in puntosSteiner):
            print("III-OMI")
            puntos  += 1
    print(puntos)

def calcularDistancia(punto1, punto2):
    return math.sqrt(math.pow(puntosSteiner[punto1][0] - puntosSteiner[punto2][0],2) + math.pow(puntosSteiner[punto1][1] - puntosSteiner[punto2][1],2))

calcularDistancias()

print(calcularDistancia('A','B'))