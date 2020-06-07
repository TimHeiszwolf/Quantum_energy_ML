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
    # General settings for each method.
    numberOfDatapoints = 25000
    numberOfSurroundingCells = 2
    numberOfParticlesPerCell = 4
    numberOfDimensions = 2
    potentialEnergyFunction = potentialEnergyPerTrio# Set the potential energy function of the data base as a function.
    widthOfCell = [2, 20]# The width of a singe cell.
    filename = 'databaseFilter_cut0.5_widths73_Width2-20_data25k_CirCirHighO_2sur'# Name of the file in which the data will be stored, set to a boolean if you don't want to store the data.
    
    # Settings filter and minimum method
    cutoff = 0.5
    numberOfWidths = 73
    
    # Settings minimum method
    amountOfEpochs = 30
    maxDeltaPerEpoch = 0.1
    descentNumberOfSurroundingCells = 1
    
    amountOfProcesses = False
    while (not (type(amountOfProcesses) == int)):
        # Keeps asking the user for the amountOfProcesses until it is a int.
        amountOfProcesses = int(input('How many processes should start? (int): '))
    
    typeOfProcces = 'none'
    while (not (typeOfProcces == 'filter' or typeOfProcces == 'random' or typeOfProcces == 'minimum')):
        # Keeps asking the user for the amountOfProcesses until it is a int.
        typeOfProcces = input('Which method? (Filter/Random/Minimum): ').lower()
    
    if typeOfProcces == 'filter':
        data = makeRandomDatabaseFilterMultiprocessing(math.ceil(numberOfDatapoints / cutoff), numberOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCell, filename, amountOfProcesses, numberOfDimensions, numberOfWidths, cutoff)
    elif typeOfProcces == 'random':
        data = makeRandomDatabaseMultiprocessing(numberOfDatapoints, numberOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCell, filename, amountOfProcesses, numberOfDimensions)
    elif typeOfProcces == 'minimum':
        data = makeRandomDatabaseMinimumMultiprocessing(numberOfDatapoints, numberOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCell, filename, amountOfProcesses, numberOfDimensions, numberOfWidths, cutoff, amountOfEpochs, maxDeltaPerEpoch, descentNumberOfSurroundingCells)
        #data = makeRandomDatabaseMinimum(numberOfDatapoints, numberOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCell, filename, True, numberOfDimensions, numberOfWidths, cutoff, amountOfEpochs, maxDeltaPerEpoch, descentNumberOfSurroundingCells)
    else:
        print('You did something wrong, you should be able to see this print.')
    
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
    
    # Making a plot by width of cell
    if typeOfProcces == 'minimum' or typeOfProcces == 'filter':
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
        ax.set_title('Plot of the energy per particle for each width of cell with offset of ' + str(tempOfsett) + '.')
        ax.set_ylabel('Energy per particle')
        ax.set_xlabel('Width of cell')
        plt.show()
    
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
        for loop in range(0, amountToPlot):
            i = random.randint(0, numberOfDatapoints - 1)
            print('Plotting datapoint ', i, ' with energy ', data['potentialEnergy'][i])
            plotLatticeFromDataFrame(data, i)

if __name__=='__main__':
    main()