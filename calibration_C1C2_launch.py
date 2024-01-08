# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 09:27:38 2021

@author: PROVOST-LUD

Script that launch the inversion of the C1 and C2 coefficients, knowing the value
of the attenuation coefficients.
Equation used:
    I = C1 + C2.M + beta.log10(Hypo) + gamma.Hypo
"""
import numpy as np
import pandas as pd
# Fixing a basemap bug
try:
    from mpl_toolkits.basemap import pyproj
except KeyError:
    import os
    import conda
    conda_file_dir = conda.__file__
    conda_dir = conda_file_dir.split('lib')[0]
    proj_lib = os.path.join(os.path.join(conda_dir, 'Library\share'), 'proj')
    os.environ["PROJ_LIB"] = proj_lib
# adding the CalIPE library to the path
import sys
sys.path.append('../CalIPE/calib_fc')
sys.path.append('../CalIPE/postprocessing_fc')
# import the needed CalIPE functions
from combinaison_calib import calib_C1C2, calib_C1C2H
from prepa_data import prepare_input4calibration, add_I0as_datapoint, evt_weights
from write_outputs import write_IPEfile4QUakeMD


#%% Input 
# Evt and Obs datafile names
obsdata_nameFR = 'Data/Obs_FRextended.txt'
evtcalib_folderFR = 'Data/'
evtdata_nameFR = 'FRinstru01.txt'


# File name of the beta distribution used in this application.
#  Gamma is considered equal to 0.
beta_distrib_nameFR = "Outputs/FRinstru01_subsets/Hist_beta_FRinstru01_Subsets02.txt"
# Reading the beta distribution
beta_dataFR = pd.read_csv(beta_distrib_nameFR, sep=';', header=3)
beta_dataFR = beta_dataFR[beta_dataFR.Probability!=0]

# Needed to launch the preparation of the data. Equal to '' when no regionalization
# is considered
regiondata_name = ''

# Option of intensity binning (ROBS, RAVG, RP50 or RP84)
binning_type = 'ROBS'
# Option of inversion of depth chosen
invDepth_option = True
# Option of adding epicentral intensity in the inversion chosen
addI0 = True
# Weighting schemes chosen and their associated weights
ponderation_list = ['IStdI_evtStdM_gMclass', 'IStdI_evtUni']
poids_ponderation = [0.5, 0.5]

#%% Outputs fileand folder names
outputfolder = 'Outputs/IPEs'
outname = 'FR_TwoStep_gamma0'

#%% Preparation of the data
nom_evt_completFR = evtcalib_folderFR + '/' + evtdata_nameFR
obsbin_plus = prepare_input4calibration(obsdata_nameFR, nom_evt_completFR,
                                        ponderation_list[0],
                                        regiondata_name, binning_type)
obsbin_plus = obsbin_plus.astype({'EVID': 'string'})

# Adding or not the epicentral intensity in the inversion according the chosen option
liste_evt = np.unique(obsbin_plus.EVID.values)
if addI0:
    obsbin_plus = add_I0as_datapoint(obsbin_plus, liste_evt)
    obsbin_plus.sort_values(by=['EVID', 'I'], inplace=True)

# Complete the obsbin dataframe with the attenuation coefficient gamma chosen equal to 0 
obsbin_plus.loc[:, 'gamma'] = 0
# Initialization of the output DataFrame
compt = 0
coeffs = pd.DataFrame(columns=['C1', 'C2', 'beta_FR', 'proba', 'ponderation', 'C1_std', 'C2_std'])
#%% Inversion part
# Browsing the explored beta values 
for indFR, rowFR in beta_dataFR.iterrows():
    beta_FR = rowFR['Beta value']
    proba_FR = rowFR['Probability']
    print(beta_FR, proba_FR)
    # Complete the obsbin dataframe with the attenuation coefficient beta explored
    obsbin_plus.loc[:, 'beta'] = beta_FR
   # Browsing the chosen weighting schemes
    for ponderation, wp in zip(ponderation_list, poids_ponderation):
        # Applying the explored weighting scheme
        obsbin_plus = evt_weights(obsbin_plus, ponderation)
        # Option with inversion of depth along the C1 and C2 coefficients
        if invDepth_option:
            # This function need columns beta and gamma in obsbin_plus
            # Inversion of C1, C2 and depth 
            ObsBin_plus, resC1regC2 = calib_C1C2H(liste_evt, obsbin_plus, NmaxIter=50)
            # Get the covariance matrix and the standard deviation of the inversion ouputs
            pcov = resC1regC2[1]
            std = np.sqrt(np.diag(pcov))
            # Storing the output coeffcients and their standard deviation into
            # a DataFrame
            coeffs.loc[compt, :] = [resC1regC2[0][0], resC1regC2[0][1], beta_FR,
                                    proba_FR*wp, ponderation, std[0], std[1]]
            compt += 1
            # Printing the results
            print('C1', 'C2')
            print(resC1regC2[0][0], resC1regC2[0][1])
            
        # Option without inversion of depth along the C1 and C2 coefficients
        else:
            # This function need columns beta and gamma in obsbin_plus
            # Inversion of C1, C2
            ObsBin_plus, resC1regC2 = calib_C1C2(liste_evt, obsbin_plus, NmaxIter=50)
            # Get the covariance matrix and the standard deviation of the inversion ouputs
            pcov = resC1regC2[1]
            std = np.sqrt(np.diag(pcov)) 
            # Storing the output coeffcients and their standard deviation into
            # a DataFrame
            coeffs.loc[compt, :] = [resC1regC2[0][0], resC1regC2[0][1],beta_FR,
                                    proba_FR*wp, ponderation, std[0], std[1]]
            compt += 1
            print('C1', 'C2')
            print(resC1regC2[0][0], resC1regC2[0][1])
        # Saving the inversion outputs and the data used for the inversion   
        ObsBin_plus.loc[:, 'C2'] = resC1regC2[0][1]
        ObsBin_plus.loc[:, 'C1'] = resC1regC2[0][0]
        ObsBin_plus.to_csv(outputfolder + '/'+outname+'/Obsbin_'+ "{:03d}".format(compt)+'.csv')

print(coeffs)
# Saving the results of the inversion in a synthetic table
coeffs.to_csv(outputfolder+'/TwoStepcomplete_table.csv')
coeffs.loc[:, 'gamma'] = 0
# Saving the results of the inversion into an IPE file compatible with QUake-MD
write_IPEfile4QUakeMD(coeffs, outputfolder + '/TwoSteps_FRinstru01_IPEs',
                      comments='No comments', C1_col='C1', C2_col='C2',
                      beta_col='beta_FR', gamma_col='gamma')
