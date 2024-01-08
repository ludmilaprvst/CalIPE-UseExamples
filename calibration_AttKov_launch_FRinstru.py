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
    import os
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
# Import the needed function from the CalIPE library
from attKov_onedataset import Kovbeta_onedataset, Kovbetagamma_onedataset
from create_subsets import same_values_2array


# Input datafile names
obsdata_name = 'Data/Obs_FRextended.txt'
evtcalib_folder = 'Data/'
evtdata_name = 'FRinstru01.txt'
subset_folder = ''
regiondata_name = ''

# Output folder
outputfolder = 'Outputs/FRinstru01/BetaGamma'

# Option of intensity binning (ROBS, RAVG, RP50 or RP84)
binning_type = 'ROBS'
# Choice of the weighting schemes
ponderation_list = ['IStdI_evtUni']
# Inversion of the gamma coefficient. If False, gamma is supposed equal to 0
option_gamma = True

# Initialization of the inverted coefficients
liste_beta_ini = [-3.0]
liste_gamma_ini = [-0.001]



# subset_folder isan empty string, so only the base database will be used
# to invert the attenuation coefficient
complete_subset = evtcalib_folder + evtdata_name
# Browse the weighting schemes:
for ponderation in ponderation_list:
    print(ponderation)
    print(complete_subset)
    # Inversion of beta and gamma coefficients
    if option_gamma:
        Kovbetagamma_onedataset(complete_subset, obsdata_name, outputfolder,
                                liste_beta_ini, liste_gamma_ini, ponderation,
                                binning_type, regiondata_name,
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
