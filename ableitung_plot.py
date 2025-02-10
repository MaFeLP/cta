import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import scipy.optimize as opt
from pyscript import display


# Messdaten der Titrationskurve
#vol_naoh = np.array([0,1,2,3,4.1,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22])
#ph_wert = np.array([2.58,2.67,2.78,2.95,3.23,3.7,5.44,6.34,6.72,7.02,7.32,7.68,8.28,9.03,9.46,9.72,9.89,10.04,10.14,10.23,10.31,10.37,10.43])

# Erstellen eines feinen Wertebereichs für die Interpolation
vol_neu = np.linspace(0, 22, num=220)

# Berechnung der numerischen ersten und zweiten Ableitung
def _numerische_ableitung(funktion, x_wert, dx=1e-6):
    return (funktion(x_wert + dx) - funktion(x_wert - dx)) / (2 * dx)

def zweite_ableitung(funktion, x_wert, dx=1e-6):
    return (_numerische_ableitung(funktion, x_wert + dx) - _numerische_ableitung(funktion, x_wert - dx)) / (2 * dx)

# Nullstellen der zweiten Ableitung durch Vorzeichenwechsel finden
def _finde_nullstellen_zweite_ableitung(funktion, x_werte):
    zweite_abl_values = np.array([zweite_ableitung(funktion, x) for x in x_werte])
    nullstellen = []
    
    for i in range(len(x_werte) - 1):
        if zweite_abl_values[i] * zweite_abl_values[i + 1] < 0:  # Vorzeichenwechsel
            nullstelle = opt.brentq(lambda x: zweite_ableitung(funktion, x), x_werte[i], x_werte[i + 1])
            if 5 <= nullstelle <= 7:
                nullstellen.append(nullstelle)
    
    return nullstellen

def plot_ableitung(vol_naoh, ph_wert):
    # Interpolation der Titrationskurve
    interpol_funktion = interp1d(vol_naoh, ph_wert, kind='cubic', fill_value="extrapolate")

    # Äquivalenzpunkt als Nullstelle der zweiten Ableitung im relevanten Bereich bestimmen
    x_startwerte = np.linspace(5, 7, 220)
    x_aequivalenzpunkt = _finde_nullstellen_zweite_ableitung(interpol_funktion, x_startwerte)
    y_aequivalenzpunkt = [interpol_funktion(x) for x in x_aequivalenzpunkt] if x_aequivalenzpunkt else None
    print(x_aequivalenzpunkt)

    # Berechnung der ersten und zweiten Ableitung für den Plot
    erste_ableitung_werte = np.array([_numerische_ableitung(interpol_funktion, x) for x in vol_neu])
    zweite_ableitung_werte = np.array([zweite_ableitung(interpol_funktion, x) for x in vol_neu])

    # Plot der Titrationskurve und der Ableitungen
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    ax1.scatter(vol_naoh, ph_wert, color='blue', label='Messpunkte', marker='x', s=20,zorder=4)
    ax1.plot(vol_neu, interpol_funktion(vol_neu), color='orange', label='Interpolierte Kurve', linewidth=0.8,zorder=3)

    if x_aequivalenzpunkt is not None:
        ax1.scatter(x_aequivalenzpunkt, y_aequivalenzpunkt, color='red', label='Äquivalenzpunkt Ableitung' , marker='x', s=20,zorder=5)
    #ax1.scatter(5.6, interpol_funktion(5.6), color='red', label='Äquivalenzpunkt Händisch' , marker='_', s=80,zorder=5)
    #ax1.scatter(5.588605460588363, interpol_funktion(5.588605460588363), color='green', label='Äquivalenzpunkt Digitale Tangente' , marker='_', s=80,zorder=5)
    #ax1.scatter(5.588483683, interpol_funktion(5.588483683), color='black', label='Durchschnittlicher Äquivalenzpunkt' , marker='_', s=80,zorder=6)
    # Plotte sowohl erste als auch zweite Ableitung
    ax2.plot(vol_neu, erste_ableitung_werte, color='green', linestyle='dashed', label='1. Ableitung',zorder=2,linewidth=0.9)
    ax2.plot(vol_neu, zweite_ableitung_werte, color='purple', linestyle='dashed', label='2. Ableitung',zorder=1,linewidth=0.9)

    ax2.axhline(0, color='gray', linestyle=':', linewidth=0.5,zorder=0)

    # Achsenbeschriftung
    ax1.set_xlabel("Volumen NaOH in ml")
    ax1.set_ylabel("pH-Wert", color='black')
    ax2.set_ylabel("Ableitungen", color='black')

    ax1.axis((2, 10, 2, 7))

    # Legenden
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    # Anzeigen des Plots
    display(plt, target="#output")
