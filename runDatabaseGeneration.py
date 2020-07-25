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


def main():
    # General settings for each method.
    numberOfDatapoints = 50000
    numberOfParticlesPerCell = 4
    numberOfDimensions = 3
    potentialEnergyFunction = potentialEnergyPerSet# Set the potential energy function of the data base as a function.
    widthOfCell = [5, 5]# The width of a singe cell.
    numberOfWidths = 1
    depthOfSurroundingCells = 3
    relaxationDepthOfSurroundingCells = 1
    amountOfEpochs = 40
    maxDeltaPerEpoch = 0.1
    cutoff = 0.9
    filename = 'DatabaseMin_1Width5_50k_0.9Cutt_40epochs_0.1max_3ds_1dsDecent_4particles_2D'# Name of the file in which the data will be stored, set to a boolean if you don't want to store the data.
    
    
    amountOfProcesses = False
    while (not (type(amountOfProcesses) == int)):
        # Keeps asking the user for the amountOfProcesses until it is a int.
        amountOfProcesses = int(input('How many processes should start? (int): '))
    
    data = makeRandomDatabaseMinimumMultiprocessing(math.ceil(numberOfDatapoints / cutoff), depthOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCell, filename, amountOfProcesses, numberOfDimensions, numberOfWidths, cutoff, amountOfEpochs, maxDeltaPerEpoch, relaxationDepthOfSurroundingCells)
    #data = makeRandomDatabaseMinimum(numberOfDatapoints, depthOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCell, filename, True, numberOfDimensions, numberOfWidths, cutoff, amountOfEpochs, maxDeltaPerEpoch, relaxationDepthOfSurroundingCells)
    
    
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
    #bins = [5**i for i in range(math.floor(math.log(max(min(x), 10**-30)) / math.log(5)) - 4, 26)]
    
    # Make the percentile plot.
    fig, ax = plt.subplots(figsize=(8, 8))
    sortedX = np.sort(x) + 1.01 * abs(min(x))
    ax.plot([100*i/len(x) for i in range(0, len(x))], sortedX)
    ax.set_xlim(0, 100)
    ax.set_yscale('log')
    ax.set_title(filename + '\n Plot of the energy per particle for each percentile with offset' + str(1.01 * abs(min(x))) + '.')
    ax.set_ylabel('Energy per particle (E/Ec)')
    ax.set_xlabel('Percentile')
    plt.show()
    
    # Making a plot by width of cell
    if numberOfWidths>1:
        tempData = dataFiltered.copy()
        tempOfsett = 1.01 * min(tempData['potentialEnergy'])
        tempData['potentialEnergy'] = tempData['potentialEnergy'] - tempOfsett
        medianData = tempData.groupby('widthOfCell').describe(percentiles=[0.05, 0.5, 0.95])
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.plot(medianData.index, medianData['potentialEnergy']['5%'])
        ax.plot(medianData.index, medianData['potentialEnergy']['50%'])
        ax.plot(medianData.index, medianData['potentialEnergy']['95%'])
        plt.legend(['5%', '50%', '95%'])
        ax.set_yscale('log')
        ax.set_title(filename + '\n Plot of the energy per particle for each width of cell with offset of ' + str(tempOfsett) + '.')
        ax.set_ylabel('Energy per particle (E/Ec)')
        ax.set_xlabel('Width of cell (r/Rc)')
        plt.show()
    
    # Make the normal historgram.
    qLow = data['potentialEnergy'].quantile(0.01)
    qHi  = data['potentialEnergy'].quantile(0.99)
    dataFiltered = data[(data['potentialEnergy'] < qHi) & (data['potentialEnergy'] > qLow)]
    x = dataFiltered['potentialEnergy']
    numBins = 1000
    
    fig, ax = plt.subplots(figsize=(8, 8))
    n, bins, patches = ax.hist(x, numBins, facecolor='blue', alpha=0.5)
    ax.set_title(filename + '\n Histogram of distribution of energy per particle.')
    ax.set_xlabel('Energy per particle (E/Ec)')
    ax.set_ylabel('Count')
    plt.show()

    amountToPlot = min([10, numberOfDatapoints])
    if input('Want to plot ' + str(amountToPlot) + ' lattices? (Y/N): ').lower() == 'y':
        # Plotting the lattices if wanted.
        for loop in range(0, amountToPlot):
            i = random.randint(0, numberOfDatapoints - 1)
            print('Plotting datapoint ', i, ' with energy ', data['potentialEnergy'][i])
            plotLatticeFromDataFrame(data, i)

if __name__=='__main__':
    main()