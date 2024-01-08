# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 15:45:24 2023

@author: PROVOST-LUD
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import sys
sys.path.append('..')
sys.path.append('../CalIPE/postprocessing_fc')

from postprocessing_Kovbeta import readBetaFile

def function(X, a1, b):
    mags = X
    return a1+mags*b


path_subsets_FR =  'Outputs/FRinstru01/Beta'
runname_basedb_FR = 'FRinstru01_ROBS_wIStdI_evtUni_betaini30'



beta_FR = readBetaFile(path_subsets_FR + '/betaFinal_' + runname_basedb_FR + '.txt')[0]


obsbin_FR = pd.read_csv(path_subsets_FR + '/obsbinEnd_' + runname_basedb_FR + '.csv', sep=';')


obsbin_FR.loc[:, 'Hypo'] = obsbin_FR.apply(lambda row : np.sqrt(row['Depi']**2+row['Depth']**2), axis=1)
obsbin_FR.loc[:, 'I-att'] = obsbin_FR['I'] - beta_FR*np.log10(obsbin_FR['Hypo'])



# Regression with common slope
all_res = obsbin_FR['I-att'].values
all_sigma = obsbin_FR['StdI'].values
all_mag = obsbin_FR['Mag'].values

X = all_mag
out, sigma = curve_fit(function, X, all_res, sigma=all_sigma)
print('Results common slope:')
print('C1 FRinstru / C2')
print(out[0], out[1])
C1_FR = out[0]
C2 = out[1]
mag_plot = np.arange(3, 7.5, 0.5)

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111)
ax.scatter(obsbin_FR.Mag.values, obsbin_FR['I-att'].values, label='FRinstru01')
ax.plot(mag_plot, C1_FR + C2*mag_plot, label='Result of the regression')

ax.set_xlabel('Magnitude Mw')
ax.set_ylabel(r'$I-\beta log10(Hypo)$')
ax.grid(which='both')
ax.legend()
fig.savefig('Figures_articles/Fig7.png', dpi=150)
