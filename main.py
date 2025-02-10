from pyscript import document
import numpy as np

from ableitung_plot import plot_ableitung
from tangente_plot import plot_tangente

def tangente(event):
    vol_naoh = []
    ph_wert = []
    
    for node in document.querySelectorAll('section.input table tbody tr'):
        vol_naoh.append(float(node.children[0].children[0].value))
        ph_wert.append(float(node.children[1].children[0].value))

    plot_tangente(np.array(vol_naoh), np.array(ph_wert))

def ableitung(event):
    vol_naoh = []
    ph_wert = []

    for node in document.querySelectorAll('section.input table tbody tr'):
        vol_naoh.append(float(node.children[0].children[0].value))
        ph_wert.append(float(node.children[1].children[0].value))

    plot_ableitung(np.array(vol_naoh), np.array(ph_wert))
