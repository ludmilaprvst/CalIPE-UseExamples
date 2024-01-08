# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 11:43:48 2021

@author: PROVOST-LUD
"""
import pandas as pd
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
# import the needed CalIPE functions
from create_subsets import create_liste_subset, filter_by_nevt, check_duplicate, create_basicdb_criteria
from create_subsets import create_subsets



"""
Create a table with the metadata used to create the subsets.
Excel file can be created/modified manually.
To do it, decomment lines 37 to 42. Warning : it will replace the
subset_criteria_FRinstru01.xlsx file of this example folder. The original file
is saved on the github repository
"""
basic_db_name = 'Data/FRinstru01.txt'
obsdata_name = 'Data/Obs_FRextended.txt'
subset_folder = 'Data/Subsets'
criteria = create_basicdb_criteria(basic_db_name, obsdata_name,
                            binning_type='ROBS',
                            outputfolder=subset_folder,
                            regiondata_name='',
                            ponderation='IStdI_evtUni',
                            )

#%% FRinstru
"""
Create the subsets based on the criteria stored in the criteria DataFrame.
For this example, an additional column QH, representing the quality of instrumental
depth estimates, is manually added.
"""
# Read the modified criteria excel file:
criteria = pd.read_excel('Data/Subsets/subset_criteria_FRinstru01.xlsx')
# Creating the different susbset lists and the associated criteria used to define
# the subsets:
global_liste, criteres = create_liste_subset(criteria,
                                             year_inf=[1980],
                                             year_sup=[2020, 2006],
                                             QH=[['A','B'], ['A']],
                                             NClass=[2, 3, 4, 5, 6],
                                             Nobs=[10, 50, 100, 200],
                                             Dc=[10, 25, 50, 100])
print(len(global_liste))
# Ensure that the minimal number of events in each susbet list is equal to 10. 
#◙ Subsets with less than 10 events are removed:
new_liste_nmin, new_critere_nmin = filter_by_nevt(global_liste, criteres, nmin=10)
print(len(new_liste_nmin))
# Checking if duplicated subsets exists:
new_liste, new_critere = check_duplicate(new_liste_nmin, new_critere_nmin)
print(len(new_liste))
# Creating the .csv files with each created subsets:
create_subsets(new_liste, new_critere, basic_db_name, folder=subset_folder)

