# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 17:00:59 2023

@author: PROVOST-LUD
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


path_subsets_FR =  'Outputs/FRinstru01_subsets'
complete_table_FR = pd.read_excel(path_subsets_FR + '/Summary_beta.xlsx')
path_subsets_IT =  'Outputs/ITinstru_subsets'
complete_table_IT = pd.read_excel(path_subsets_IT + '/Summary_beta.xlsx')
bins = np.arange(-4.75, -2.8, 0.1)

#%% Plot the histogram figure
fig = plt.figure(figsize=(12, 6))
ax_FR = fig.add_subplot(121)
ax_IT = fig.add_subplot(122)

ax_FR.hist(complete_table_FR.beta.values, bins=bins, alpha=0.5)
ax_FR.text(-4.25, -1, '(a)', fontsize=14)
ax_FR.grid(which='both')
ax_FR.set_xlabel(r'$\beta $ $coefficient$ $value$')
ax_FR.set_ylabel('Normalized number of occurence')
ax_FR.axvline(x=-3.3, color='Navy', ls='--', lw=2, label='Value obtained with the FRinstru01 dataset')
ax_FR.axvline(x=complete_table_FR.beta.mean(), color='Navy', label=r'Mean $\beta$ value for all FR subsets')
locs = ax_FR.get_yticks() 
ax_FR.set_yticks(locs, np.round(locs/len(complete_table_FR.beta.values),3))
ax_FR.legend(loc=2)
ax_FR.set_xlim(-4, -2.5)


ax_IT.hist(complete_table_IT.beta.values, bins=bins, alpha=0.5, color='tab:orange')
ax_IT.axvline(x=-4.33, color='OrangeRed', ls='--', lw=2, label='Value obtained with the ITinstru01 dataset')
ax_IT.text(-4.95, 0, '(b)', fontsize=14)
ax_IT.axvline(x=complete_table_IT.beta.mean(), color='OrangeRed', label=r'Mean $\beta$ value for all IT subsets')
ax_IT.grid(which='both')
ax_IT.set_xlabel(r'$\beta $ $coefficient$ $value$')
ax_IT.set_ylabel('Normalized number of occurence')
locs = ax_IT.get_yticks() 
ax_IT.set_yticks(locs,np.round(locs/len(complete_table_IT.beta.values),3))
ax_IT.legend(loc=1)
ax_IT.set_xlim(-4.75, -3.5)

fig.savefig('Fig5.png', dpi=150)
#%% Saving the histograms
hist_FR, bins_FR = np.histogram(complete_table_FR.beta.values, bins=bins)
hist_IT, bins_IT = np.histogram(complete_table_IT.beta.values, bins=bins)
hist_FR = hist_FR/len(complete_table_FR)
hist_IT = hist_IT/len(complete_table_IT)

milieu =  bins_FR[:-1]+0.1/2
milieu = np.around(milieu, decimals=2)
output_FR = pd.DataFrame({'beta':milieu, 'Probability':hist_FR})
output_FR = output_FR[output_FR['Probability']!=0]
output_FR.loc[:, 'Probability'] = output_FR.Probability/output_FR.Probability.sum()
output_FR.to_csv(path_subsets_FR + '/hist_beta.csv', index=False)

milieu =  bins_IT[:-1]+0.1/2
milieu = np.around(milieu, decimals=2)
output_IT = pd.DataFrame({'beta':milieu, 'Probability':hist_IT})
output_IT = output_IT[output_IT['Probability']!=0]
output_IT.loc[:, 'Probability'] = output_IT.Probability/output_IT.Probability.sum()
output_IT.to_csv(path_subsets_IT + '/hist_beta.csv', index=False)