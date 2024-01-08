# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 09:27:38 2021

@author: PROVOST-LUD
"""
import numpy as np
import pandas as pd
import sys
from pathlib import Path
# adding the CalIPE library to the path
sys.path.append('../CalIPE/calib_fc')
sys.path.append('../CalIPE/postprocessing_fc')
# import the needed CalIPE functions
from combinaison_calib import calib_C1C2betaH
from prepa_data import prepare_input4calibration, evt_weights, add_I0as_datapoint
from write_outputs import write_IPEfile4QUakeMD

#%% Inputs
# Name and path of the input files
obsdata_name = 'Data/Obs_FRextended.txt'
evtdata_name = 'FRinstru01.txt'
evtcalib_folder = 'Data/'
# Needed to launch the preparation of the data. Equal to '' when no regionalization
# is considered
regiondata_name = ''

# Option of intensity binning (ROBS, RAVG, RP50 or RP84)
binning_type = 'ROBS'
# Weighting schemes chosen and their associated weights
ponderation_list = ['IStdI_evtStdM_gMclass']
poids_ponderation = [1.0]
# Option of adding epicentral intensity in the inversion chosen
addI0 = True

#%% Outputs
# Output names and folder
outname = 'OneStep_gFRinstru01_amma0'
outputfolder = 'Outputs/IPEs'
# Creating the output folder if not exist
Path(outputfolder+'/'+outname).mkdir(parents=True, exist_ok=True)

#%% Preparation of the data
nom_evt_complet = evtcalib_folder + '/' + evtdata_name
obsbin_plus = prepare_input4calibration(obsdata_name, nom_evt_complet,
                                        ponderation_list[0],
                                        regiondata_name, binning_type)
# Adding or not the epicentral intensity in the inversion according the chosen option
liste_evt = np.unique(obsbin_plus.EVID.values)
if addI0:
    obsbin_plus = add_I0as_datapoint(obsbin_plus, liste_evt)
    obsbin_plus.sort_values(by=['EVID', 'I'], inplace=True)

# The different initial values explored
beta_liste = [-2.5, -3, -3.5]
C1_liste = [1.5, 2, 2.5]
C2_liste = [1.5]
# Initialization of the output DataFrame
output_df = pd.DataFrame(columns=['beta_ini', 'C1_ini', 'C2_ini', 'ponderation',
                                  'C1', 'C2', 'beta','std_C1', 'std_C2',
                                  'std_beta', 'gamma', 'proba'])
ind = 0
# Borwsing the different initial values and weighting schemes
for beta in beta_liste:
    print(beta)
    for C1 in C1_liste:
        print(C1)
        for C2 in C2_liste:
            print(C2)
            for ponderation, wp in zip(ponderation_list, poids_ponderation):
                print(ponderation)
                obsbin_plus = evt_weights(obsbin_plus, ponderation)

                # Inversion with gamma considered equal to 0
                # Inversion of C1, C2, beta and depth 
                ObsBin_plus, result = calib_C1C2betaH(liste_evt, obsbin_plus,
                                                           C1, C2, beta,
                                                           NmaxIter=100)
                # Get the covariance matrix and the standard deviation of the inversion ouputs
                pcov = result[1]
                std = np.sqrt(np.diag(pcov))
                # Storing the output coeffcients and their standard deviation into
                # a DataFrame
                output_df.loc[ind, :] = [beta, C1, C2, ponderation, result[0][0], result[0][1], result[0][2],
                                         std[0], std[1], std[2], 0, 1/(len(beta_liste)*len(C1_liste)*len(C2_liste)*len(ponderation_list))]
                ObsBin_plus.loc[:, 'C1'] = result[0][0]
                ObsBin_plus.loc[:, 'C2'] = result[0][1]
                ObsBin_plus.loc[:, 'beta'] = result[0][2]
                ObsBin_plus.loc[:, 'gamma'] = 0
                # Saving the inversion outputs and the data used for the inversion
                ObsBin_plus.to_csv(outputfolder + '/'+outname+'/Obsbin_'+ "{:03d}".format(ind)+'.csv')
                ind += 1
                print("C1, C2, beta")
                print(result[0][:3])
                print(result[1][:3])
# Saving the results of the inversion in a synthetic table
output_df.to_csv('Outputs/IPEs/OneStep_completeresult.csv')
# Saving the results of the inversion into an IPE file compatible with QUake-MD      
write_IPEfile4QUakeMD(output_df, outputfolder + '/' + outname +'_IPEs', 
                      comments='No comments', C1_col='C1', C2_col='C2', 
                      beta_col='beta', gamma_col='gamma')
