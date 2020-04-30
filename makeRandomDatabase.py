import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import random
import math

from generateSpace import *
from plotLattice import *
from getTriangleLengths import *
from potentialEnergyPerTrio import *
from potentialEnergy import *
from potentialEnergyPerParticle import *
from numberOfCalculations import *


def makeRandomDatabase(numberOfDatapoints, numberOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCellRange = [1, 1], filename = False):
    """
    A function that generates a random database of particle configurations and their potential energies.
    
    """
    
    secondsPerDatapoint = 15 * (10**-6) * numberOfCalculations(numberOfSurroundingCells, numberOfParticlesPerCell)
    print('Predicted amount of calculations:', int(numberOfDatapoints * numberOfCalculations(numberOfSurroundingCells, numberOfParticlesPerCell)))
    print('Assuming 15 us per calculation, estimated time needed:', math.ceil(numberOfDatapoints * secondsPerDatapoint), 'seconds')
    # Give the user some information and estimates about the amount of calculation and time needed.
    
    startTime = time.time()
    
    data = {'particleCoordinates': [],'widthOfCell':[] , 'numberOfSurroundingCells': [], 'potentialEnergy':[]}
    
    for i in range(0, numberOfDatapoints):
        # Generate the required number of datapoints.
        widthOfCell = random.uniform(widthOfCellRange[0], widthOfCellRange[1])
        particles = [np.array([random.uniform(0, widthOfCell), random.uniform(0, widthOfCell)]) for j in range(0, numberOfParticlesPerCell)]# Make a randomised basis cell of the correct size.
        otherSpace = generateSpace(particles, numberOfSurroundingCells, widthOfCell)# Generate the other space.
        data['particleCoordinates'].append(particles)
        data['widthOfCell'].append(widthOfCell)
        data['numberOfSurroundingCells'].append(numberOfSurroundingCells)
        data['potentialEnergy'].append(potentialEnergy(otherSpace, particles, potentialEnergyFunction))# Calculate the potential energy and save it to the data dictonairy.
        
        print(str(math.ceil(100 * (i + 1) / (numberOfDatapoints ))).rjust(3, ' '), '% done, time left', math.ceil((numberOfDatapoints - i - 1) * secondsPerDatapoint), 'seconds,', math.ceil(time.time() - startTime), 'seconds since start.')# Inform the user of the progress.
    
    endTime = time.time()
    print('Done generating database. Took :', math.ceil(endTime - startTime), 'seconds, predicted', math.ceil(numberOfDatapoints * secondsPerDatapoint), 'seconds.')# Inform the user of how the procces has progressed.
    
    dataDF = pd.DataFrame(data)# Turn the data into a pandas DataFrame to make data easier to handle.
    
    if type(filename) == str:
        # If wanted save the data to a json file.
        dataDF.to_json(filename + '.json', orient='columns')
    
    return dataDF

numberOfDatapoints = 1000
numberOfSurroundingCells = 4
numberOfParticlesPerCell = 4
potentialEnergyFunction = potentialEnergyPerTrio# Set the potential energy function of the data base as a function
widthOfCell = [0.5, 100]# The width of a singe cell.
filename = 'test2'# Name of the file in which the data will be stored, set to a boolean if you don't want to store the data.

data = makeRandomDatabase(numberOfDatapoints, numberOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCell, filename)

qLow = data['potentialEnergy'].quantile(0)
qHi  = data['potentialEnergy'].quantile(0.80)

dataFiltered = data[(data['potentialEnergy'] < qHi) & (data['potentialEnergy'] > qLow)]

x = dataFiltered['potentialEnergy']
num_bins = 100

fig, ax = plt.subplots(figsize=(8, 8))
#ax.set_xlim([0, 10**19])
#ax.set_xscale('log')
n, bins, patches = ax.hist(x, num_bins, facecolor='blue', alpha=0.5)
plt.show()

amountToPlot = min([10, numberOfDatapoints])
if input('Want to plot ' + str(amountToPlot) + ' lattices? (Y/N)').lower() == 'y':
    for i in range(0, amountToPlot):
        print('Plotting datapoint ', i, ' with energy ', data['potentialEnergy'][i])
        plotLatticeFromDataFrame(data, i)