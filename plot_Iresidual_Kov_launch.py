# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 08:56:42 2022

@author: PROVOST-LUD

Script that plot the intensity residual of the inversion result of the first
part of the two-steps inversion 
"""
import matplotlib.pyplot as plt
# adding the CalIPE library to the path
import sys
sys.path.append('..')
sys.path.append('../CalIPE/postprocessing_fc')
# import the needed CalIPE functions
from CalIPE.postprocessing_fc.postprocessing_Kovbeta import plot_dIMag, plot_dII0, plot_dIH
from CalIPE.postprocessing_fc.postprocessing_Kovbeta import plot_dI_Depi, plot_dI_Iobs


#%% Inputs
# path to the inversion output results
path_subsets =  'Outputs/FRinstru01/Beta'
# Base name of the targeted inversion result
runname_basedb = 'FRinstru01_ROBS_wdevt-uni_betaini30'

#%% Plot the figure

figbdb_resMI0 = plt.figure(figsize=(10, 8))
ax_resM = figbdb_resMI0.add_subplot(223)
ax_resI0= figbdb_resMI0.add_subplot(224)
plot_dIMag(runname_basedb, path_subsets, ax_resM, color='#1f77b4')
plot_dII0(runname_basedb, path_subsets, ax_resI0, color='#1f77b4')
ax_resM.grid(which='both')
ax_resM.legend()
ax_resI0.grid(which='both')
ax_resI0.legend()
ax_resI0.text(2, -1.25, '(c)', fontsize=15)
ax_resM.text(2.8, -1.25, '(d)', fontsize=15)
ax_resM.set_ylim([-1, 1])
ax_resM.set_xlim([3, 5.5])
ax_resI0.set_ylim([-1, 1])
ax_resI0.set_xlim([3, 9])

ax_resDepi = figbdb_resMI0.add_subplot(221)
ax_resI= figbdb_resMI0.add_subplot(222)
plot_dI_Depi(runname_basedb,
             path_subsets, ax_resDepi, evthighlight='None',)
plot_dI_Iobs(runname_basedb, path_subsets, ax_resI, evthighlight='None')
ax_resDepi.grid(which='both')
ax_resI.grid(which='both')
ax_resDepi.text(-20, -1.25, '(a)', fontsize=15)
ax_resI.text(1, -1.25, '(b)', fontsize=15)
ax_resDepi.set_ylim([-1, 1])
ax_resDepi.set_xlim([0, 160])
ax_resI.set_ylim([-1, 1])
ax_resI.set_xlim([2, 9])
ax_resI.legend()
ax_resDepi.legend()
plt.tight_layout()
#figbdb_resMI0.savefig('FRinstru01_basedb_WEdI.png', dpi=150)

figbdb_resH = plt.figure(figsize=(8, 6))
ax_resH = figbdb_resH.add_subplot(111)
plot_dIH(runname_basedb, path_subsets, ax_resH, color='#1f77b4')
ax_resH.grid(which='both')
ax_resH.legend()
#figbdb_resH.savefig('FRinstru01_basedb_WEdI_H.png', dpi=150)