import math
import random

#Flugrichtungsvektor
def flugvektor(pos):
    start_list = [[1, 230, 304], [2, 344, 99], [3, 122, 593], [4, 23, 215], [5, 412, 376]]
    ziel_list = [[1, 345, 212], [2, 356, 123], [3, 432, 348], [4, 3465, 234], [5, 500, 2123]]
    x = int(ziel_list[int(pos[1])][1]) - int(start_list[int(pos[0]) ][1])
    y = int(ziel_list[int(pos[1])][2]) - int(start_list[int(pos[0])][2])
    flugvektor = [x, y]

    return flugvektor


#Abstand Position und Loch
def entfernung(pos):
    x = flugvektor(pos)[0]
    y = flugvektor(pos)[1]
    entfernung = int(math.sqrt( ((x**2) + (y**2)) ))

    return entfernung


#Abschlaggeschwindigkeit des Balls
def flugGeschwindigkeit(entfernung, gamma):
    #Geschwindigkeit des Balls die bei gamma nötig ist das Loch zu erreichen
    flugGeschwindigkeit = math.sqrt( (entfernung * 9.81 / math.sin((2*gamma))) )

    return flugGeschwindigkeit


#Windparameter (Windgeschwindigkeit und Richtung) (zufällig generiert)
def windParameter():
    #Windgeschwindigkeit von 0 bis 30 m/s
    staerke = random.random() * 30 
    #8 Windrichtungen in 45° Schritten
    richtung = random.randint(0,7) *45

    windParameter = {"richtung": richtung, "staerke": staerke}

    return windParameter


#Winkel zwischen Wind und Flugrichtung
def winkelDiff(pos, windRichtung):
    #Über die Vektoren von Wind(wx, wy) und Flugbahn(fx, fy)
    #Wind:
    wx = math.cos(math.radians(windRichtung))
    wy = math.sin(math.radians(windRichtung))
    #Fulgbahn:
    fx = flugvektor(pos)[0]
    fy = flugvektor(pos)[1]

    winkelDiff = math.acos((wx*fx + wy*fy) / (math.sqrt(((wx**2) + (wy**2))) * math.sqrt(((fx**2) + (fy**2)))))
    
    return winkelDiff


#Winkelabweichung der Flugbahn
def ablenkwinkel(pos, gamma):
    abstand = entfernung(pos)
    wind = windParameter()
    v = flugGeschwindigkeit(abstand, gamma)

    #Winkel zwischen Flugbahn und Wind
    winkel = winkelDiff(pos, wind['richtung'])
    if winkel > (math.pi/2):
        winkel = math.pi - winkel
    #Kraft gegen den Ball (0.5*Formkonstante*Oberfläche*Dichteluft*(wind*winkel))
    windkraft = 0.5 * 0.45 * 0.00143 * 1.29 * (wind['staerke']*math.sin(winkel))
    #Zeit in der Luft
    flugzeit = abstand / v
    #Beschleunigung, die durch den Wind auf den Ball wirkt
    beschleunigung = windkraft / 0.046
    #Ablenkung durch die Beschleunigung über die Zeit
    ablenkung = (beschleunigung / 2) * (flugzeit**2)
    #Winkel durch die Ablenkung von der Bahn
    ablenkwinkel = math.atan(ablenkung / abstand)

    ergebnis = {"ablenkwinkel": ablenkwinkel, "beschleunigung": beschleunigung}
    return ergebnis


def berechne(pos, gamma):
    #Abstand zwischen Position und Loch
    abstand = entfernung(pos)  
    #Abschlaggeschwindigkeit abhängig von Entfernung und Steigwinkel
    v = flugGeschwindigkeit(abstand, gamma)
    #Beschleunigung und Winkel in z-Richtung durch den Wind
    ablenkung = ablenkwinkel(pos, gamma)
    korrekturWinkel = ablenkung['ablenkwinkel']
    zBeschleunigung = ablenkung['beschleunigung']

    y_werte = []
    x_werte = []
    z_werte = []
    i= 0

    for i in range(abstand):
        y_werte.append( math.tan(gamma) * i - 9.81 / (2 * v**2.0 * (math.cos(gamma))**2.0 ) * i**2.0 )
        z_werte.append( math.tan(korrekturWinkel) * i - zBeschleunigung / (2 * v**2.0 * (math.cos(korrekturWinkel))**2.0 ) * i**2.0 )
        x_werte.append(i)

    werte = {"x": x_werte, "y": y_werte, "z": z_werte}
   
    return werte
