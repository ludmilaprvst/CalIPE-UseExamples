# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 11:50:57 2021

@author: PROVOST-LUD
"""
import numpy as np
import pandas as pd
import os
# Fixing a basemap bug
try:
    from mpl_toolkits.basemap import pyproj
except KeyError:
    import conda
    conda_file_dir = conda.__file__
    conda_dir = conda_file_dir.split('lib')[0]
    # To adapt to the Anaconda/python installation
    proj_lib = os.path.join(os.path.join(conda_dir, 'Library\share'), 'proj')
    os.environ["PROJ_LIB"] = proj_lib


# adding the CalIPE library to the path
import sys
sys.path.append('../CalIPE/calib_fc')
sys.path.append('../CalIPE/postprocessing_fc')
from attKov_onedataset import Kovbeta_onedataset, Kovbetagamma_onedataset
from create_subsets import same_values_2array


# Input file and folder names:
obsdata_name = 'Data/Obs_FRextended.txt'
evtcalib_folder = 'Data/'
evtdata_name = 'FRinstru01.txt'
subset_folder = 'Data/Subsets/FRinstru01'
regiondata_name = ''
# Give an existing folder to store the outputs: 
outputfolder = 'Outputs/FRinstru01_subsets'
# Option of intensity binning (ROBS, RAVG, RP50 or RP84)
binning_type = 'ROBS'
# Choice of the weighting schemes
ponderation_list = ['IStdI_evtUni']
# Inversion of the gamma coefficient. If False, gamma is supposed equal to 0
option_gamma = False
# Initialization of the inverted coefficients
liste_beta_ini = [-2.0, -3.0, -4.0,]
liste_gamma_ini = [0, -0.01, -0.001]


if not subset_folder == '':
    # Read the list of subsets:
    liste_subset = pd.read_excel(subset_folder +'/dataset_list.xlsx')
    liste_subset = liste_subset.Datasubsetname.values
    # Adding the base dataset used to define the subsets in the subset list:
    liste_subset = np.insert(liste_subset, 0, evtdata_name)
    # Browse all the subset list:
    for subset in liste_subset:
        # Define the path to the evt file of the browsed subset
        if subset == evtdata_name:
            complete_subset = evtcalib_folder + subset
        else:
            complete_subset = subset_folder + '/' + subset + '.csv'
        print(complete_subset)
        if not os.path.isfile(complete_subset):
            print('No ' + complete_subset + ' exists')
        else:
            # If the path is correct and the subset exist:
            # Check if the browsed subset is the same dataset as the base dataset
            # (sanity check, to avoid duplicates):
            basedataset = pd.read_csv(evtcalib_folder + evtdata_name, sep=';')
            subsetdataset = pd.read_csv(complete_subset, sep=';')
            same = same_values_2array(basedataset.EVID.values, subsetdataset.EVID.values)
            if same and complete_subset!= evtcalib_folder + evtdata_name:
                # If the browsed subset is the same dataset as the base dataset,
                # the algorithm will move to the next subset in the subset list:
                print(subset + ' has the same events as the base database')
                continue
            print(subset)
            # Browse the weighting schemes:
            for ponderation in ponderation_list:
                print(ponderation)
                # Inversion of beta and gamma coefficients
                if option_gamma:
                    Kovbetagamma_onedataset(complete_subset, obsdata_name, 
                                            outputfolder=outputfolder,
                                            liste_beta_ini=liste_beta_ini,
                                            liste_gamma_ini=liste_gamma_ini,
                                            ponderation=ponderation,
                                            binning_type=binning_type,
                                            regiondata_name=regiondata_name,
                                            NminIter=3, NmaxIter=100)
                # Inversion of beta coefficient, gamma is supposed equal to 0
                else:
                    Kovbeta_onedataset(complete_subset, obsdata_name,
                                       outputfolder=outputfolder,
                                       liste_beta_ini=liste_beta_ini,
                                       ponderation=ponderation,
                                       binning_type=binning_type,
                                       regiondata_name=regiondata_name,
                                       NminIter=3, NmaxIter=100)
else:
    print('Please enter the folder where the evt subset files are stored')
