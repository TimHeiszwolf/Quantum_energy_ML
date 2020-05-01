import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
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


def makeRandomDatabase(numberOfDatapoints, numberOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCellRange = [1, 1], filename = False, giveUpdates = True):
    """
    A function that generates a random database of particle configurations and their potential energies.
    
    """
    if giveUpdates:
        # Give the user some information and estimates about the amount of calculation and time needed.
        secondsPerDatapoint = 15 * (10**-6) * numberOfCalculations(numberOfSurroundingCells, numberOfParticlesPerCell)
        print('Predicted amount of calculations:', int(numberOfDatapoints * numberOfCalculations(numberOfSurroundingCells, numberOfParticlesPerCell)), 'for ', numberOfDatapoints, 'datapoints.')
        print('Assuming 15 us per calculation, estimated time needed:', math.ceil(numberOfDatapoints * secondsPerDatapoint), 'seconds')
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
        
        if giveUpdates:
            print(str(math.ceil(100 * (i + 1) / (numberOfDatapoints ))).rjust(3, ' '), '% done, time left', math.ceil((numberOfDatapoints - i - 1) * secondsPerDatapoint), 'seconds,', math.ceil(time.time() - startTime), 'seconds since start.')# Inform the user of the progress.
    
    if giveUpdates:
        endTime = time.time()
        print('Done generating database. Took :', math.ceil(endTime - startTime), 'seconds, predicted', math.ceil(numberOfDatapoints * secondsPerDatapoint), 'seconds.')# Inform the user of how the procces has progressed.
    
    dataDF = pd.DataFrame(data)# Turn the data into a pandas DataFrame to make data easier to handle.
    
    if type(filename) == str:
        # If wanted save the data to a json file.
        dataDF.to_json(filename + '.json', orient='columns')
    
    return dataDF


def makeRandomDatabaseSingleQueue(q, numberOfDatapoints, numberOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCellRange, giveUpdates):
    q.put(makeRandomDatabase(numberOfDatapoints, numberOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCellRange, False, giveUpdates))


def makeRandomDatabaseMultiprocessing(numberOfDatapoints, numberOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCellRange = [1, 1], filename = False, amountOfProcesses = 4):
    """
    A function that impliments multiprocessing for the generation of the database.
    """
    #https://stackoverflow.com/questions/1182315/python-multicore-processing#1182350
    q = Queue()
    
    processes = []
    print('Using multiprocessing only the first procces gives updates')
    processes.append(Process(target = makeRandomDatabaseSingleQueue, args = (q, math.ceil(numberOfDatapoints / amountOfProcesses), numberOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCellRange, True)))
    for i in range(0, amountOfProcesses - 1):
        processes.append(Process(target = makeRandomDatabaseSingleQueue, args = (q, math.ceil(numberOfDatapoints / amountOfProcesses), numberOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCellRange, False)))
    
    for i in processes:
        i.start()
    time.sleep(5)
    
    dataDF =pd.concat([q.get() for i in range(0, amountOfProcesses)], ignore_index=True, sort =False)
    
    if type(filename) == str:
        # If wanted save the data to a json file.
        dataDF.to_json(filename + '.json', orient='columns')
    
    return dataDF
