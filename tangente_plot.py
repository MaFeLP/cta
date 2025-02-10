import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import scipy.optimize as opt
from pyscript import display

# Messdaten der Titrationskurve (Volumen NaOH in ml vs. pH-Wert)
#vol_naoh = np.array([0,1,2,3,4.1,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22])
#ph_wert = np.array([2.58,2.67,2.78,2.95,3.23,3.7,5.44,6.34,6.72,7.02,7.32,7.68,8.28,9.03,9.46,9.72,9.89,10.04,10.14,10.23,10.31,10.37,10.43])

#############################################################################
# Berechnung der numerischen Ableitung
def _numerische_ableitung(funktion, x_wert, dx=1e-9):
    """Berechnet die numerische Ableitung von funktion an der Stelle x_wert."""
    return (funktion(x_wert + dx) - funktion(x_wert - dx)) / (2 * dx)


# Funktion zum Finden der x-Werte, an denen die Ableitung f'(x) = 1 ist
def _finde_x_bei_steigung_eins(funktion, x_werte):
    """Findet die x-Werte im Bereich 5 ml bis 7 ml, an denen die Ableitung 1 beträgt."""

    def gleichung(x):
        return _numerische_ableitung(funktion, x) - 1

    nullstellen = []
    for startwert in x_werte:
        loesung = opt.fsolve(gleichung, startwert)[0]

        # Nur Werte im relevanten Bereich behalten (5 ml - 7 ml)
        if 4 <= loesung <= 8:
            # Rundung auf 4 Nachkommastellen, um doppelte Werte zu vermeiden
            loesung = round(loesung, 5)
            if loesung not in nullstellen:
                nullstellen.append(loesung)
    return np.array(nullstellen)


def plot_tangente(vol_naoh, ph_wert):
    # Interpolation der Titrationskurve
    interpol_funktion = interp1d(vol_naoh, ph_wert, kind='cubic', fill_value="extrapolate")

    # Erstellen eines feinen Wertebereichs für die Interpolation
    vol_neu = np.linspace(0, 22, num=1000)

    # x-Werte finden, bei denen die Ableitung 1 beträgt
    x_steigung_eins = _finde_x_bei_steigung_eins(interpol_funktion, vol_naoh)
    print("x-Werte mit Steigung 1:", x_steigung_eins)

    ##############################################################################
    # Punkte für die Tangentenberechnung

    punkt_tangente_1 = np.array([x_steigung_eins[0], interpol_funktion(x_steigung_eins[0])])
    punkt_tangente_2 = np.array([x_steigung_eins[-1], interpol_funktion(x_steigung_eins[-1])])

    # Parameter für die Tangentengleichung
    steigung = 1  # Steigung der Tangenten (45°)

    def tangente(x, x_tangentenpunkt, y_tangentenpunkt):
        return steigung * (x - x_tangentenpunkt) + y_tangentenpunkt

    # Bestimmung des Äquivalenzpunkts als Schnittpunkt der mittleren Tangente mit der Titrationskurve
    def finde_aequivalenzpunkt(funktion, x_startwert):
        def differenz(x):
            return funktion(x) - tangente(x, (punkt_tangente_1[0] + punkt_tangente_2[0]) / 2, (punkt_tangente_1[1] + punkt_tangente_2[1]) / 2)
        return opt.fsolve(differenz, x_startwert)[0]

    aequivalenzpunkt_x = finde_aequivalenzpunkt(interpol_funktion, np.mean(x_steigung_eins))
    aequivalenzpunkt_y = interpol_funktion(aequivalenzpunkt_x)
    aequivalenzpunkt = np.array([aequivalenzpunkt_x, aequivalenzpunkt_y])
    aequx=int(aequivalenzpunkt_x)
    # x-Werte für die Darstellung der Tangenten
    x_tangentenwerte = np.linspace(0, 22, 100)
    print(aequivalenzpunkt_x )
    y_mittlere_tangente = tangente(x_tangentenwerte, aequivalenzpunkt[0], aequivalenzpunkt[1])
    y_tangente_1 = tangente(x_tangentenwerte, punkt_tangente_1[0], punkt_tangente_1[1])
    y_tangente_2 = tangente(x_tangentenwerte, punkt_tangente_2[0], punkt_tangente_2[1])

    ##############################################################################
    # Plot der Titrationskurve mit Tangenten und Äquivalenzpunkt

    fig, ax = plt.subplots()

    # Messpunkte darstellen
    plt.scatter(vol_naoh, ph_wert, color='blue', label='Messpunkte', marker='x', zorder=1, s=20)
    plt.scatter(aequivalenzpunkt[0], aequivalenzpunkt[1], color='red', label='Äquivalenzpunkt bei 5,589 ml', marker='x', zorder=3, s=20)

    # Interpolierte Titrationskurve
    plt.plot(vol_neu, interpol_funktion(vol_neu), color='orange', label='Interpolierte Kurve', linewidth=0.8,zorder=0)

    # Tangenten darstellen
    plt.plot(x_tangentenwerte, y_mittlere_tangente, color='red', linestyle=':', label='Mittlere Gerade', linewidth=0.6,zorder=0)
    plt.plot(x_tangentenwerte, y_tangente_1, color='black', linestyle=':', label='Tangenten bei 45°', linewidth=0.6,zorder=0)
    plt.plot(x_tangentenwerte, y_tangente_2, color='black', linestyle=':', linewidth=0.6,zorder=0)

    # Achsenbeschriftungen
    plt.xlabel("Volumen NaOH in ml")
    plt.ylabel("pH-Wert")
    plt.axis((0, 10,2, 10))

    # Legende und Titel anzeigen
    plt.legend()
    display(plt, target="#output")

