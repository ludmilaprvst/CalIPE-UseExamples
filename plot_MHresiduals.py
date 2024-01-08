# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 11:50:59 2023

@author: PROVOST-LUD

This read results of the QUake-MD tool (Provost and Scotti, 2020). 
Some function are introduced in this script and not in the CalIPE package
because the script do not use CalIPE outputs.
"""
import pandas as pd
import matplotlib.pyplot as plt




def filter_by_IPE(outputfile, C1):
    """
    Filter the classical_result_IPE outputfile of QUake-MD by the value of C1 coefficient
    of the IPE

    Parameters
    ----------
    outputfile : pandas.DataFrame
        the content of the classical_result_IPE outputfile of QUake-MD.
    C1 : float
        value of C1 coefficient of the targeted IPE.

    Returns
    -------
    pandas.DataFrame
        lines of the input DataFrame for whoch the C1 coefficient is equal to
        the second input.

    """
    
    return outputfile[outputfile.C1==C1]

def attribute_MHinstru(outputfile, ref):
    """
    Merge two DataFrame based on the earthquake ID.

    Parameters
    ----------
    outputfile : pandas.DataFrame
        DataFrame which columns that contains the earthquake ID is called 'NumEvt'.
    ref : pandas.DataFrame
        DataFrame which columns that contains the earthquake ID is called 'EVID'.

    Returns
    -------
    pandas.DataFrame
        Merged DatFrame.

    """
    
    return outputfile.merge(ref, left_on='NumEvt', right_on='EVID')

def plot_refig(results_calib, results_test, outname):
    """
    Plot the comparison between the macroseismic estimates of depth and magnitude
    made by QUake-MD and the instrumental depth and magnitude.

    Parameters
    ----------
    results_calib : pandas.DataFrame
        Results of the application of QUake-MD on the calibration dataset FRinstru01
        merged with the instrumental estimates of depth and magnitude.
    results_test : pandas.DataFrame
        Results of the application of QUake-MD on the test dataset FRTest01 merged
        with the instrumental estimates of depth and magnitude..
    outname : str
        path and name of the saved figure.

    Returns
    -------
    None.

    """
     
    fig = plt.figure (figsize=(8, 6))
    axM = fig.add_subplot(211)
    axH = fig.add_subplot(212)
    dM_calib = results_calib.Mag_y - results_calib.Mag_x
    dM_test = results_test.Mw - results_test.Mag
    axM.scatter(results_calib.Mag_y, dM_calib, label='Calibration dataset')
    axM.scatter(results_test.Mw, dM_test, label='Test dataset')
    axM.axhline(y=dM_calib.mean(), lw=2, color='tab:blue',
                )
    axM.axhline(y=dM_calib.mean() + dM_calib.std(), ls='--', color='tab:blue',
                )
    axM.axhline(y=dM_calib.mean() - dM_calib.std(), ls='--', color='tab:blue',
                )
    axM.axhline(y=dM_test.mean(), lw=2, ls='-', color='tab:orange',
                )
    axM.axhline(y=dM_test.mean() + dM_test.std(), ls='--', color='tab:orange',
               )
    axM.axhline(y=dM_test.mean() - dM_test.std(), ls='--', color='tab:orange',
                )
    axM.set_xlabel('Instrumental magnitude Mw')
    axM.set_ylabel('Instrumental mag. - Predicted mag.')
    axM.grid(which='both')
    axM.set_ylim([-1, 1])
    axM.legend()

    dH_calib = results_calib.Depth - results_calib.H
    axH.scatter(results_calib.Depth, dH_calib)
    axH.axhline(y=dH_calib.mean(), lw=2, color='tab:blue', label='Mean of the residuals')
    axH.axhline(y=dH_calib.mean() + dH_calib.std(), ls='--', color='tab:blue',
                label='mean +/- std')
    axH.axhline(y=dH_calib.mean() - dH_calib.std(), ls='--', color='tab:blue',
                )
    axH.set_xlabel('Instrumental depth [km]')
    axH.set_ylabel('Instrumental depth - depth')
    axH.grid(which='both')
    axH.set_ylim([-15, 15])
    axH.legend()
    plt.tight_layout()
    fig.savefig(outname, dpi=150)

# Read the instrumental information    
ref_calib = pd.read_csv('Data/FRinstru01.txt', sep=';')
ref_test = pd.read_csv('Data/Testdataset.txt', sep=';')
mag_test = pd.read_excel('../Data/Test_dataset.xlsx')
# Read the QUake-MD outputs
QuakeMD_calib = pd.read_csv('Quake-MD_outputs_rapide/All_IPEs_classical_results_calibEQ.txt', sep=',')
QuakeMD_test = pd.read_csv('Quake-MD_outputs_rapide/All_IPEs_classical_results_testEQ.txt', sep=',')

# C1 value of the IPE tested
oneStepC1_IPE_tested = 1.60443 # C1 of the one-step strategy IPE tested
twoStepC1_IPE_tested = 2.34826 # C1 of the two-steps strategy IPE tested
# Filtering the output file by IPE for the one-step IPE
results_calib_oneStep = filter_by_IPE(QuakeMD_calib, oneStepC1_IPE_tested)
results_test_oneStep = filter_by_IPE(QuakeMD_test, oneStepC1_IPE_tested)
# merging with the instrumental information for the one-step IPE
results_calib_oneStep =  attribute_MHinstru(results_calib_oneStep, ref_calib)
results_test_oneStep =  attribute_MHinstru(results_test_oneStep, ref_test)
# plot the firgure 12 for the for the one-step IPE
plot_refig(results_calib_oneStep, results_test_oneStep, 'Figures_articles/Mresidual_onestep.png')
# Filtering the output file by IPE for the two-steps IPE
results_calib_twoStep = filter_by_IPE(QuakeMD_calib, twoStepC1_IPE_tested)
results_test_twoStep = filter_by_IPE(QuakeMD_test, twoStepC1_IPE_tested)
# merging with the instrumental information for the two-steps IPE
results_calib_twoStep =  attribute_MHinstru(results_calib_twoStep, ref_calib)
results_test_twoStep =  attribute_MHinstru(results_test_twoStep, ref_test)
# plot the firgure 9 for the for the two-steps IPE
plot_refig(results_calib_twoStep, results_test_twoStep, 'Figures_articles/Mresidual_twostep.png')


