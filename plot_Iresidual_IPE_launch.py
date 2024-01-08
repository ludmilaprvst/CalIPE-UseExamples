# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 14:55:54 2023

@author: PROVOST-LUD
"""
import matplotlib.pyplot as plt
# adding the CalIPE library to the path
import sys
sys.path.append('..')
sys.path.append('../CalIPE/postprocessing_fc')
# import the needed CalIPE functions
import CalIPE.postprocessing_fc.postprocessing_IPEs as ppI



#%% Figure 9
# Input filename and path
outputname = 'Obsbin_001.csv'
path = 'Outputs/IPEs/FR_TwoStep_gamma0'
# Computing the residuals
obsbin = ppI.compute_WEresiduals(outputname, path)
# Plot the figure and save it
fig = plt.figure(figsize=(8, 8))
ax_depi = fig.add_subplot(311)
ax_dI = fig.add_subplot(312)
ax_mag = fig.add_subplot(313)
ppI.plot_dI_Depi(outputname, path, ax_depi, fig, evthighlight='None', plot_I0data=False, color_on='None')
ppI.plot_dI_I(outputname, path, ax_dI, fig, evthighlight='None', plot_I0data=False, color_on='None')
ppI.plot_BEresiduals_Mag(outputname, path, ax_mag, fig, evthighlight='None', plot_I0data=True, color_on='None')
ax_depi.legend(loc=3)
ax_dI.legend()
ax_mag.legend()
ax_mag.set_ylim([-1, 1])
plt.tight_layout()
#fig.savefig('Figures_articles/Fig9.png', dpi=150)

#%% Figure 12
# Input filename and path
outputname = 'Obsbin_001.csv'
path = 'Outputs/IPEs/FR_OneStep_gamma0'
# Computing the residuals
obsbin = ppI.compute_WEresiduals(outputname, path)
# Plot the figure and save it
fig = plt.figure(figsize=(8, 8))
ax_depi = fig.add_subplot(311)
ax_dI = fig.add_subplot(312)
ax_mag = fig.add_subplot(313)
ppI.plot_dI_Depi(outputname, path, ax_depi, fig, evthighlight='None', plot_I0data=False, color_on='None')
ppI.plot_dI_I(outputname, path, ax_dI, fig, evthighlight='None', plot_I0data=False, color_on='None')
ppI.plot_BEresiduals_Mag(outputname, path, ax_mag, fig, evthighlight='None', plot_I0data=True, color_on='None')
ax_depi.legend(loc=3)
ax_dI.legend()
ax_mag.legend()
ax_mag.set_ylim([-1, 1])
plt.tight_layout()
#fig.savefig('Figures_articles/Fig12.png', dpi=150)

