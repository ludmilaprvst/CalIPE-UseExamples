# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 08:56:42 2022

@author: PROVOST-LUD

Script that gathers the output beta coefficients obtained with different subset
in a common table.
The results should be saved in a same output folder.
"""

import pandas as pd
# adding the CalIPE library to the path
import sys
sys.path.append('..')
sys.path.append('../CalIPE/postprocessing_fc')
# import the needed CalIPE functions
from CalIPE.postprocessing_fc import results_bootstrap_hist


#%%
path_subsets =  'Outputs/FRinstru01_subsets'
datasetlist = 'Data/Subsets/FRinstru01/dataset_list.xlsx'

#%%
outdf = results_bootstrap_hist.get_table_inoutputbeta(path_subsets)
Subsets_02 = pd.read_excel(datasetlist)
complete_table = outdf.merge(Subsets_02,
                             left_on='database',
                             right_on='Datasubsetname',
                             how='outer')
complete_table.to_excel(path_subsets + '/Summary_beta.xlsx')
