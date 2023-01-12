import math

def berechne(pos):
    start_list = [[1, 230, 304], [2, 344, 99], [3, 122, 593], [4, 23, 215], [5, 412, 376]]
    ziel_list = [[1, 345, 212], [2, 356, 123], [3, 432, 348], [4, 3465, 234], [5, 500, 2123]]
    x = int(ziel_list[int(pos[1])][1]) - int(start_list[int(pos[0]) ][1])
    y = int(ziel_list[int(pos[1])][2]) - int(start_list[int(pos[0])][2])
    entfernung = int(math.sqrt( ((x**2) + (y**2)) ))
    print('Entfernung',entfernung)
    y_werte = []
    x_werte = []
    i= 0
    gamma = math.pi / 6
    v =math.sqrt( (entfernung * 9.81 / math.sin((2*gamma))) )
    print('Geschw.:', v )
    for i in range(entfernung):
        y_werte.append( math.tan(gamma) * i - 9.81 / (2 * v**2.0 * (math.cos(gamma))**2.0 ) * i**2.0 )
        x_werte.append(i)

    werte = []
    werte = werte.append(x_werte)
    werte = werte.append(y_werte)
    print(werte)
    return werte
    