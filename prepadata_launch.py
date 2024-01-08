# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 11:50:57 2021

@author: PROVOST-LUD
"""
import sys
sys.path.append('../CalIPE/calib_fc')
sys.path.append('../CalIPE/postprocessing_fc')

from prepa_data import fichier_input
import EvtIntensityObject as eio
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, NullFormatter, LogLocator

# FR-instru
obsdata_name = '../../Application_QUakeMD/Data/Obs2017_felt_QIobsD.txt'
evtdata_name = '../../Application_QUakeMD/Data/Evt_vd41300_all_epiEDF.txt'
#obsdata_name = '../../Application_QUakeMD/Data/Obs2017.txt'
# evtdata_name = '../../Application_QUakeMD/Data/Evt2017_okformatQUakeMD.txt'

depth = 7.3
Ic = 3
obsdata = pd.read_csv(obsdata_name, sep=';')
evtdata = pd.read_csv(evtdata_name, sep=';')
fichiers = fichier_input(obsdata, evtdata)
data = eio.Evt(fichiers)
data.build(1100041)
data.Binning_Obs(depth, Ic, 'RF50')
print(data.ObsBinn)
"""
# EDF 860004 (1711) - ROBS depth = 8.6
I_edf = np.array([5, 5.5, 6, 7, 7.5])
hypo_edf = np.array([87.9, 55, 30.8, 13, 11.9])
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111)
hypo_obs = np.sqrt(8.6**2 + data.Obsevid.Depi.values**2)
ax.semilogx(hypo_obs, data.Obsevid.Iobs.values, '.', color='Gray',
            label="Points individuels d'intensité")
ax.semilogx(data.ObsBinn.Hypo.values, data.ObsBinn.I.values, 'd',
            color='Orange', ms=12,
            label=u"Isoésites IRSN (méthode ROBS)")
ax.semilogx(hypo_edf, I_edf, 'd', color='DodgerBlue',
            label=u"Isoésites EDF (méthode ROBS)")

ax.legend()
ax.set_xlabel(u"Distance hypocentrale [km]")
ax.set_ylabel(u"Intensité macrosismique [MSK64]")
ax.set_title("Séisme de Loudun (1711) - Profondeur de 8,6 km")
ax.grid(which='both')
ax.xaxis.set_major_formatter(ScalarFormatter())
locmaj = LogLocator(base=10.0, subs=(0.1, 0.2, 0.5, 1, 2, 5, 10 ))
ax.xaxis.set_major_locator(locmaj)
ax.xaxis.set_minor_formatter(NullFormatter())
"""