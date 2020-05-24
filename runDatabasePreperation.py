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
from getTriangleLengths import *
from potentialEnergyPerTrio import *
from potentialEnergy import *
from potentialEnergyPerParticle import *
from numberOfCalculations import *
from makeRandomDatabase import *
from prepareDatabaseForMachineLearning import*


def main():
    filename = 'CombinedDataR500M1M2M3'# The name of the file which you want to prepare for machine learning.
    orderOfMatrix = [-1, -2, -3]# The order of the matrices you want to make.
    R0 = 500
    
    data = pd.read_json(filename + '.json', orient='columns')
    data['particleCoordinates'] = data['particleCoordinates'].apply(np.array)
    
    if input('Do you want to use multiprocessing? (Y/N): ').lower()=='y':
        # Asks the user if multiprocessing is wanted.
        amountOfProcesses = False
        while (not (type(amountOfProcesses) == int)):
            # Keeps asking the user for the amountOfProcesses until it is a int.
            amountOfProcesses = int(input('How many processes should start? (int): '))
            
        print('Starting multiprocessing.')
        data = prepareDatabseForMachineLearningMultiprocessing(data, orderOfMatrix, R0, filename + 'Prepared', amountOfProcesses)
    else:
        print('Starting singleprocessing.')
        data = prepareDatabseForMachineLearning(data, orderOfMatrix, R0, filename + 'Prepared')
    
    print('\nDone preparing database now analysing.\n')
    print(data.head(), '\n')
    print(data.describe())

if __name__=='__main__':
    main()