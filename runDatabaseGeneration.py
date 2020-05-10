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


def main():
    numberOfDatapoints =  20000
    numberOfSurroundingCells = 4
    numberOfParticlesPerCell = 4
    potentialEnergyFunction = potentialEnergyPerTrio# Set the potential energy function of the data base as a function.
    widthOfCell = [1, 50]# The width of a singe cell.
    filename = 'database10_20k'# Name of the file in which the data will be stored, set to a boolean if you don't want to store the data.
    
    if input('Do you want to use multiprocessing? (Y/N): ').lower()=='y':
        # Asks the user if multiprocessing is wanted.
        amountOfProcesses = False
        while (not (type(amountOfProcesses) == int)):
            # Keeps asking the user for the amountOfProcesses until it is a int.
            amountOfProcesses = int(input('How many processes should start? (int): '))
            
        print('Starting multiprocessing.')
        data = makeRandomDatabaseMultiprocessing(numberOfDatapoints, numberOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCell, filename, amountOfProcesses)
    else:
        print('Starting singleprocessing.')
        data = makeRandomDatabase(numberOfDatapoints, numberOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCell, filename)
    
    print('\n Done generating database now analysing \n')
    print(data.head(), '\n')
    print(data.describe())
    print('\n Now plotting historgrams \n')
    
    ## The code below is for plotting diagrams.
    # Filter the data for the percentile plot.
    qLow = data['potentialEnergy'].quantile(0.01)
    qHi  = data['potentialEnergy'].quantile(0.99)
    dataFiltered = data[(data['potentialEnergy'] < qHi) & (data['potentialEnergy'] > qLow)]
    x = dataFiltered['potentialEnergy']
    bins = [5**i for i in range(math.floor(math.log(max(min(x), 10**-30)) / math.log(5)) - 4, 26)]
    
    # Make the percentile plot.
    fig, ax = plt.subplots(figsize=(8, 8))
    sortedX = np.sort(x) + 1.01 * abs(min(x))
    ax.plot([100*i/len(x) for i in range(0, len(x))], sortedX)# LEOTOJGIOPHJNEIONPGENIOKGHNOIKEGINOLKGENKJLEGKINLOGENKLGELKNGLNIK
    ax.set_xlim(0, 100)
    ax.set_yscale('log')
    ax.set_title('Plot of the energy per particle for each percentile.')
    ax.set_ylabel('Energy per particle')
    ax.set_xlabel('Percentile')
    plt.show()
    
    # Filter the data for the normal historgram.
    qLow = data['potentialEnergy'].quantile(0.10)
    qHi  = data['potentialEnergy'].quantile(0.90)
    dataFiltered = data[(data['potentialEnergy'] < qHi) & (data['potentialEnergy'] > qLow)]
    x = dataFiltered['potentialEnergy']
    numBins = 1000
    
    # Make the normal historgram.
    fig, ax = plt.subplots(figsize=(8, 8))
    n, bins, patches = ax.hist(x, numBins, facecolor='blue', alpha=0.5)
    ax.set_title('Histogram of distribution of energy per particle.')
    ax.set_xlabel('Energy per particle')
    ax.set_ylabel('Count')
    plt.show()

    amountToPlot = min([10, numberOfDatapoints])
    if input('Want to plot ' + str(amountToPlot) + ' lattices? (Y/N): ').lower() == 'y':
        # Plotting the lattices if wanted.
        for i in range(0, amountToPlot):
            print('Plotting datapoint ', i, ' with energy ', data['potentialEnergy'][i])
            plotLatticeFromDataFrame(data, i)

if __name__=='__main__':
    main()