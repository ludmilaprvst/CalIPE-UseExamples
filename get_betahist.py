# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 15:57:02 2022

@author: PROVOST-LUD
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# adding the CalIPE library to the path
import sys
sys.path.append('../CalIPE/postprocessing_fc')
# import the needed CalIPE functions
from results_att_hist import write_betahistfile



# Define the bins of the histogram:
beta_values_FR = np.arange(-3.35, -2.8, 0.1)

# Reading the FRinstru01 results:
path_subsets =  "Outputs/FRinstru01_subsets"
datasetlist = '../Data/Subsets/FRinstru/dataset_list.xlsx'
summary_FRinstru = pd.read_excel(path_subsets + '/Summary_beta.xlsx')
# Define an output name for the histrogram
outputname = "Outputs/FRinstru01_subsets/Hist_beta_FRinstru01_Subsets02.txt"
# Write the histogram file and get the histogram properties:
bin_edges_FRinstru, hist_FRinstru, normedHist_FRinstru = write_betahistfile(outputname,
                                                                            summary_FRinstru.beta.values,
                                                                            bins=np.arange(-3.4, -2.7, 0.1),
                                                                            path_subsets=path_subsets,
                                                                            datasetlist=datasetlist,
                                                                            specific_comment="  ")

# Plot the normed histogram:
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111)
ax.bar(beta_values_FR, normedHist_FRinstru, width=0.1, alpha=0.5)
# Adding some key values on the histogram as vertical lines:
ax.axvline(x=-3.298, color='b', label='Value obtained with the Frinstru01 dataset')
ax.axvline(x=summary_FRinstru.beta.mean(), ls='--', color='b',
            label='Mean value of all Fr subsets results')
ax.legend()
plt.tight_layout()
fig.savefig('Figures_articles/Fig6.png', dpi=150)
plt.show()

