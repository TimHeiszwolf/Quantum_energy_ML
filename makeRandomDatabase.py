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


def makeRandomDatabase(numberOfDatapoints, numberOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCell, filename = False):
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
        particles = [np.array([random.uniform(0, widthOfCell), random.uniform(0, widthOfCell)]) for j in range(0, numberOfParticlesPerCell)]# Make a randomised basis cell of the correct size.
        otherSpace = generateSpace(particles, numberOfSurroundingCells, widthOfCell)# Generate the other space.
        data['particleCoordinates'].append(particles)
        data['widthOfCell'].append(widthOfCell)
        data['numberOfSurroundingCells'].append(numberOfSurroundingCells)
        data['potentialEnergy'].append(potentialEnergy(otherSpace, particles, potentialEnergyFunction))# Calculate the potential energy and save it to the data dictonairy.
        
        print(str(math.ceil(100 * (i + 1) / (numberOfDatapoints ))).rjust(3, ' '), '% done, time left', math.ceil((numberOfDatapoints - i - 1) * secondsPerDatapoint), 'seconds.')# Inform the user of the progress.
    
    endTime = time.time()
    print('Done generating database. Took :', math.ceil(endTime - startTime), 'seconds, predicted', math.ceil(numberOfDatapoints * secondsPerDatapoint), 'seconds.')# Inform the user of how the procces has progressed.
    
    dataDF = pd.DataFrame(data)# Turn the data into a pandas DataFrame to make data easier to handle.
    
    if type(filename) == str:
        # If wanted save the data to a json file.
        dataDF.to_json(filename + '.json', orient='columns')
    
    return dataDF

