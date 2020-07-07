import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
import time
import random
import math
from multiprocessing import Process, Queue

from generateSpace import *
from plotLattice import *
from potentialEnergy import *
from numberOfCalculations import *
from makeRandomDatabase import *
from prepareDatabaseForMachineLearning import*


def main():
    filename = 'databasemin_cut0.9_widths1_5-5_25k_3-1_epoch40_maxDelta0.1_AdjustedPotential_M2M3'#'databaseModLen_min_cut0.90_widths86_Width1.5-10_3-1sur_epoch30_maxDelta0.1_R20_M2M3'# The name of the file which you want to prepare for machine learning.
    orderOfMatrix = [-2, -3]# The order of the matrices you want to make.
    R0p = 20
    
    data = pd.read_json(filename + '.json', orient='columns')
    data['particleCoordinates'] = data['particleCoordinates'].apply(np.array)
    
    amountOfProcesses = False
    while (not (type(amountOfProcesses) == int)):
        # Keeps asking the user for the amountOfProcesses until it is a int.
        amountOfProcesses = int(input('How many processes should start? (int): '))
    
    data = prepareDatabseForMachineLearningMultiprocessing(data, orderOfMatrix, R0p, filename + 'Prepared', amountOfProcesses)
    
    print('\nDone preparing database now analysing.\n')
    print(data.head(), '\n')
    print(data.describe())

if __name__=='__main__':
    main()