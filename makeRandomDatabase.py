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


def makeRandomDatabase(numberOfDatapoints, numberOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCellRange=[1, 1], filename=False, giveUpdates=True, numberOfDimensions=2):
    """
    A function that generates a random database of particle configurations and their potential energies.
    
    numberOfDatapoints is the length/amount of datapoints in the final database.
    numberOfSurroundingCells is the 'depth' of the surrounding cells (in a square) so if it is two then the total grid is five by five cells large.
    potentialEnergyFunction is a function that takes a list of length 3 consisting of the lengths of the sides of a triangle of three particles.
    widthOfCellRange is a list of the the range of possible cell widths.
    filename is the name of the file the database get's exported to. The .json file extension get's added in the code itself. If the type of filename is not a string no file will be saved.
    giveUpdates is a boolean which determines if updates about the progress of the database generation get's printed.
    """
    if giveUpdates:
        print('Now generating space.')
    
    data = {'particleCoordinates':list(np.zeros((numberOfDatapoints, numberOfParticlesPerCell, numberOfDimensions))), 'widthOfCell':[], 'numberOfSurroundingCells': [], 'potentialEnergy':[]}# Initialy use a dictionary because it's easier to append to than a dataframe.
    
    for i in range(0, numberOfDatapoints):
        # Generate the required number of datapoints.
        widthOfCell = random.uniform(widthOfCellRange[0], widthOfCellRange[1])
        data['widthOfCell'].append(widthOfCell)
        data['numberOfSurroundingCells'].append(numberOfSurroundingCells)
    
    for i in range(0, numberOfDimensions):
        # Generate the particle coordinates. First all the X coordinates for each partile and datapoint and then the Y and so on.
        for j in range(0, numberOfParticlesPerCell):
            for k in range(0, numberOfDatapoints):
                data['particleCoordinates'][k][j][i] = random.uniform(0, data['widthOfCell'][k])
    
    if giveUpdates:
        # Give the user some information and estimates about the amount of calculation and time needed.
        secondsPerDatapoint = 19 * (10**-6) * numberOfCalculationsGeneration(numberOfSurroundingCells, numberOfParticlesPerCell)
        print('Done generating space.')
        print('Predicted amount of calculations:', int(numberOfDatapoints * numberOfCalculationsGeneration(numberOfSurroundingCells, numberOfParticlesPerCell)), 'for', numberOfDatapoints, 'datapoints.')
        print('Assuming 19 us per calculation, estimated time needed:', math.ceil(numberOfDatapoints * secondsPerDatapoint), 'seconds')
        startTime = time.time()
    
    for i in range(0, numberOfDatapoints):
        # Calculate the energy of each datapoint.
        otherSpace = generateSpace(data['particleCoordinates'][i], data['numberOfSurroundingCells'][i], data['widthOfCell'][i])# Generate the other space.
        data['potentialEnergy'].append(potentialEnergy(otherSpace, data['particleCoordinates'][i], potentialEnergyFunction))# Calculate the potential energy and save it to the data dictonairy.
        
        if giveUpdates:
            print(str(math.ceil(100 * (i + 1) / (numberOfDatapoints))).rjust(3, ' '), '% done, expected time left', math.ceil((numberOfDatapoints - i - 1) * secondsPerDatapoint), 'seconds,', math.ceil(time.time() - startTime), 'seconds since start.')# Inform the user of the progress.
    
    if giveUpdates:
        endTime = time.time()
        print('Done generating database. Took :', math.ceil(endTime - startTime), 'seconds, predicted', math.ceil(numberOfDatapoints * secondsPerDatapoint), 'seconds.')# Inform the user of how the procces has progressed.
    
    dataDF = pd.DataFrame(data)# Turn the data into a pandas DataFrame to make data easier to handle.
    
    if type(filename) == str:
        # If wanted save the data to a json file.
        dataDF.to_json(filename + '.json', orient='columns')
    
    return dataDF


def makeRandomDatabaseSingleQueue(q, numberOfDatapoints, numberOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCellRange, giveUpdates, numberOfDimensions=2):
    q.put(makeRandomDatabase(numberOfDatapoints, numberOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCellRange, False, giveUpdates))


def makeRandomDatabaseMultiprocessing(numberOfDatapoints, numberOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCellRange=[1, 1], filename=False, amountOfProcesses=5, numberOfDimensions=2):
    """
    A function that impliments multiprocessing for the generation of the database.
    """
    q = Queue()
    
    processes = []
    print('Using multiprocessing only the first procces gives updates')
    processes.append(Process(target = makeRandomDatabaseSingleQueue, args = (q, math.ceil(numberOfDatapoints / amountOfProcesses), numberOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCellRange, True, numberOfDimensions)))
    
    for i in range(0, amountOfProcesses - 1):
        processes.append(Process(target = makeRandomDatabaseSingleQueue, args = (q, math.ceil(numberOfDatapoints / amountOfProcesses), numberOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCellRange, False, numberOfDimensions)))
    
    for i in processes:
        i.start()
    
    dataDF = pd.concat([q.get() for i in range(0, amountOfProcesses)], ignore_index = True, sort = False)
    
    if type(filename) == str:
        # If wanted save the data to a json file.
        dataDF.to_json(filename + '.json', orient='columns')
    
    return dataDF











def makeRandomDatabaseFilter(numberOfDatapoints, numberOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCellRange=[1, 1], filename=False, giveUpdates=True, numberOfDimensions=2, numberOfWidths=100, cutoff=0.5):
    """
    A function that generates a random database of particle configurations and their potential energies.
    
    numberOfDatapoints is the length/amount of datapoints in the final database.
    numberOfSurroundingCells is the 'depth' of the surrounding cells (in a square) so if it is two then the total grid is five by five cells large.
    potentialEnergyFunction is a function that takes a list of length 3 consisting of the lengths of the sides of a triangle of three particles.
    widthOfCellRange is a list of the the range of possible cell widths.
    filename is the name of the file the database get's exported to. The .json file extension get's added in the code itself. If the type of filename is not a string no file will be saved.
    giveUpdates is a boolean which determines if updates about the progress of the database generation get's printed.
    """
    
    dataFrames = []
    totalNumberOfCalculations = numberOfWidths * math.ceil(numberOfDatapoints / (numberOfWidths))
    if giveUpdates:
        startTime = time.time()
        print('Starting generation. With', numberOfWidths, 'number of widths,', totalNumberOfCalculations, 'number of calculations (so', math.ceil(numberOfDatapoints / numberOfWidths), 'per width).')
    
    
    for loopNumber in range(numberOfWidths):
        widthOfCell = np.linspace(widthOfCellRange[0], widthOfCellRange[1], numberOfWidths)[loopNumber]# Could also use np.logspace
        
        data = {'particleCoordinates':list(np.zeros((math.ceil(numberOfDatapoints / numberOfWidths), numberOfParticlesPerCell, numberOfDimensions))), 'widthOfCell':[], 'numberOfSurroundingCells': [], 'potentialEnergy':[]}# Initialy use a dictionary because it's easier to append to than a dataframe.
        
        if giveUpdates:
            print('Generating space with width', widthOfCell)
        
        for i in range(0, math.ceil(numberOfDatapoints / numberOfWidths)):
            # Generate the required number of datapoints.
            data['widthOfCell'].append(widthOfCell)
            data['numberOfSurroundingCells'].append(numberOfSurroundingCells)
        
        for i in range(0, numberOfDimensions):
            # Generate the particle coordinates. First all the X coordinates for each partile and datapoint and then the Y and so on.
            for j in range(0, numberOfParticlesPerCell):
                for k in range(0, math.ceil(numberOfDatapoints / numberOfWidths)):
                    data['particleCoordinates'][k][j][i] = random.uniform(0, data['widthOfCell'][k])
        
        for i in range(0, math.ceil(numberOfDatapoints / numberOfWidths)):
            otherSpace = generateSpace(data['particleCoordinates'][i], data['numberOfSurroundingCells'][i], data['widthOfCell'][i])# Generate the other space.
            data['potentialEnergy'].append(potentialEnergy(otherSpace, data['particleCoordinates'][i], potentialEnergyFunction))# Calculate the potential energy and save it to the data dictonairy.
            
            if giveUpdates:
                numberOfCalculationsDone = i + 1 + loopNumber * math.ceil(numberOfDatapoints / numberOfWidths)
                print(str(math.ceil(100 * numberOfCalculationsDone / totalNumberOfCalculations)).rjust(3, ' '), '% done, expected time left', math.ceil((time.time() - startTime) * (totalNumberOfCalculations - numberOfCalculationsDone) / numberOfCalculationsDone), 'seconds,', math.ceil(time.time() - startTime), 'seconds since start.')
            
            
        dataDF = pd.DataFrame(data)# Turn the data into a pandas DataFrame to make data easier to handle.
        qHi  = dataDF['potentialEnergy'].quantile(cutoff)
        dataFiltered = dataDF[(dataDF['potentialEnergy'] < qHi)]# & (data['potentialEnergy'] > qLow)]
        dataFrames.append(dataFiltered)
        
        if giveUpdates:
            print('Width' , widthOfCell, 'done.')
            print('Filtered stats:')
            print(dataFiltered['potentialEnergy'].describe())
            print('Unfiltered stats:')
            print(dataDF['potentialEnergy'].describe())
        
    if giveUpdates:
        endTime = time.time()
        print('Done generating database. Took :', math.ceil(endTime - startTime), 'seconds.')# Inform the user of how the procces has progressed.
    
    
    finalDataFrame = pd.concat(dataFrames, ignore_index = True, sort = False)
    
    if type(filename) == str:
        # If wanted save the data to a json file.
        finalDataFrame.to_json(filename + '.json', orient='columns')
    
    return finalDataFrame


def makeRandomDatabaseFilterSingleQueue(q, numberOfDatapoints, numberOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCellRange, giveUpdates, numberOfDimensions, numberOfWidths, cutoff):
    q.put(makeRandomDatabaseFilter(numberOfDatapoints, numberOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCellRange, False, giveUpdates, numberOfDimensions, numberOfWidths, cutoff))


def makeRandomDatabaseFilterMultiprocessing(numberOfDatapoints, numberOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCellRange=[1, 1], filename=False, amountOfProcesses=5, numberOfDimensions=2, numberOfWidths=100, cutoff=0.5):
    """
    A function that impliments multiprocessing for the generation of the database.
    """
    q = Queue()
    
    processes = []
    print('Using multiprocessing only the first procces gives updates')
    processes.append(Process(target = makeRandomDatabaseFilterSingleQueue, args = (q, math.ceil(numberOfDatapoints / amountOfProcesses), numberOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCellRange, True, numberOfDimensions, numberOfWidths, cutoff)))
    
    for i in range(0, amountOfProcesses - 1):
        processes.append(Process(target = makeRandomDatabaseFilterSingleQueue, args = (q, math.ceil(numberOfDatapoints / amountOfProcesses), numberOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCellRange, False, numberOfDimensions, numberOfWidths, cutoff)))
    
    for i in processes:
        i.start()
    
    dataDF = pd.concat([q.get() for i in range(0, amountOfProcesses)], ignore_index = True, sort = False)
    
    if type(filename) == str:
        # If wanted save the data to a json file.
        dataDF.to_json(filename + '.json', orient='columns')
    
    return dataDF














def makeRandomDatabaseMinimum(numberOfDatapoints, numberOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCellRange=[1, 1], filename=False, giveUpdates=True, numberOfDimensions=2, numberOfWidths=100, cutoff=0.5, amountOfEpochs=4, maxDeltaPerEpoch=0.01, descentNumberOfSurroundingCells=2):
    """
    A function that generates a random database of particle configurations and their potential energies.
    
    numberOfDatapoints is the length/amount of datapoints in the final database.
    numberOfSurroundingCells is the 'depth' of the surrounding cells (in a square) so if it is two then the total grid is five by five cells large.
    potentialEnergyFunction is a function that takes a list of length 3 consisting of the lengths of the sides of a triangle of three particles.
    widthOfCellRange is a list of the the range of possible cell widths.
    filename is the name of the file the database get's exported to. The .json file extension get's added in the code itself. If the type of filename is not a string no file will be saved.
    giveUpdates is a boolean which determines if updates about the progress of the database generation get's printed.
    """
    
    dataFrames = []
    totalNumberOfCalculations = numberOfWidths * math.ceil(numberOfDatapoints / (numberOfWidths))
    if giveUpdates:
        startTime = time.time()
        print('Starting generation. With', numberOfWidths, 'number of widths,', totalNumberOfCalculations, 'number of calculations (so', math.ceil(numberOfDatapoints / numberOfWidths), 'per width).')
    
    
    for loopNumber in range(numberOfWidths):
        widthOfCell = np.linspace(widthOfCellRange[0], widthOfCellRange[1], numberOfWidths)[loopNumber]# Could also use np.logspace
        
        data = {'particleCoordinates':list(np.zeros((math.ceil(numberOfDatapoints / numberOfWidths), numberOfParticlesPerCell, numberOfDimensions))), 'widthOfCell':[], 'numberOfSurroundingCells': [], 'potentialEnergy':[]}# Initialy use a dictionary because it's easier to append to than a dataframe.
        
        if giveUpdates:
            print('Generating space with width', widthOfCell)
        
        for i in range(0, math.ceil(numberOfDatapoints / numberOfWidths)):
            # Generate the required number of datapoints.
            data['widthOfCell'].append(widthOfCell)
            data['numberOfSurroundingCells'].append(numberOfSurroundingCells)
        
        for i in range(0, numberOfDimensions):
            # Generate the particle coordinates. First all the X coordinates for each partile and datapoint and then the Y and so on.
            for j in range(0, numberOfParticlesPerCell):
                for k in range(0, math.ceil(numberOfDatapoints / numberOfWidths)):
                    data['particleCoordinates'][k][j][i] = random.uniform(0, data['widthOfCell'][k])
        
        for i in range(0, math.ceil(numberOfDatapoints / numberOfWidths)):
            
            for j in range(amountOfEpochs):
                # The monte carlo part in which diffrent
                for particleNumber in range(len(data['particleCoordinates'][i])):
                    newCoordinates = np.copy(data['particleCoordinates'][i])
                    #newCoordinates[particleNumber] = newCoordinates[particleNumber] + np.array([maxDeltaPerEpoch * random.uniform(-1, 1) for a in range(0, numberOfDimensions)])
                    direction = random.randint(0, numberOfDimensions - 1)
                    newCoordinates[particleNumber][direction] = newCoordinates[particleNumber][direction] + maxDeltaPerEpoch * random.uniform(-1, 1)
                    
                    oldOtherSpace = generateSpace(data['particleCoordinates'][i], descentNumberOfSurroundingCells, data['widthOfCell'][i])
                    oldPotentialEnergy = potentialEnergy(oldOtherSpace, data['particleCoordinates'][i], potentialEnergyFunction)
                    
                    newOtherSpace = generateSpace(newCoordinates, descentNumberOfSurroundingCells, data['widthOfCell'][i])
                    newPotentialEnergy = potentialEnergy(oldOtherSpace, newCoordinates, potentialEnergyFunction)
                    
                    if newPotentialEnergy <= oldPotentialEnergy:
                        data['particleCoordinates'][i] = newCoordinates
                    
                    if giveUpdates:
                        numberOfCalculationsDone = i + 1 + loopNumber * math.ceil(numberOfDatapoints / numberOfWidths)
                        print(str(math.ceil(100 * numberOfCalculationsDone / totalNumberOfCalculations)).rjust(3, ' '), '% done, expected time left', math.ceil((time.time() - startTime) * (totalNumberOfCalculations - numberOfCalculationsDone) / numberOfCalculationsDone), 'seconds,', math.ceil(time.time() - startTime), 'seconds since start, on width of cell', widthOfCell, 'datapoint', i + 1, 'out of', 1 + math.ceil(numberOfDatapoints / numberOfWidths), 'epoch', j + 1, 'particle', particleNumber, 'a lower energy was found:', newPotentialEnergy <= oldPotentialEnergy)
            
            
            otherSpace = generateSpace(data['particleCoordinates'][i], data['numberOfSurroundingCells'][i], data['widthOfCell'][i])# Generate the other space.
            data['potentialEnergy'].append(potentialEnergy(otherSpace, data['particleCoordinates'][i], potentialEnergyFunction))# Calculate the potential energy and save it to the data dictonairy.
            
            
            
        dataDF = pd.DataFrame(data)# Turn the data into a pandas DataFrame to make data easier to handle.
        qHi  = dataDF['potentialEnergy'].quantile(cutoff)
        dataFiltered = dataDF[(dataDF['potentialEnergy'] < qHi)]# & (data['potentialEnergy'] > qLow)]
        dataFrames.append(dataFiltered)
        
        if giveUpdates:
            print('Width' , widthOfCell, 'done.')
            print('Filtered stats:')
            print(dataFiltered['potentialEnergy'].describe())
            print('Unfiltered stats:')
            print(dataDF['potentialEnergy'].describe())
        
    if giveUpdates:
        endTime = time.time()
        print('Done generating database. Took :', math.ceil(endTime - startTime), 'seconds.')# Inform the user of how the procces has progressed.
    
    
    finalDataFrame = pd.concat(dataFrames, ignore_index = True, sort = False)
    
    if type(filename) == str:
        # If wanted save the data to a json file.
        finalDataFrame.to_json(filename + '.json', orient='columns')
    
    return finalDataFrame


def makeRandomDatabaseMinimumSingleQueue(q, numberOfDatapoints, numberOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCellRange, giveUpdates, numberOfDimensions, numberOfWidths, cutoff, amountOfEpochs, maxDeltaPerEpoch, descentNumberOfSurroundingCells):
    q.put(makeRandomDatabaseMinimum(numberOfDatapoints, numberOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCellRange, False, giveUpdates, numberOfDimensions, numberOfWidths, cutoff, amountOfEpochs, maxDeltaPerEpoch, descentNumberOfSurroundingCells))


def makeRandomDatabaseMinimumMultiprocessing(numberOfDatapoints, numberOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCellRange=[1, 1], filename=False, amountOfProcesses=5, numberOfDimensions=2, numberOfWidths=100, cutoff=0.5, amountOfEpochs=4, maxDeltaPerEpoch=0.01, descentNumberOfSurroundingCells=2):
    """
    A function that impliments multiprocessing for the generation of the database.
    """
    q = Queue()
    
    processes = []
    print('Using multiprocessing only the first procces gives updates')
    processes.append(Process(target = makeRandomDatabaseMinimumSingleQueue, args = (q, math.ceil(numberOfDatapoints / amountOfProcesses), numberOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCellRange, True, numberOfDimensions, numberOfWidths, cutoff, amountOfEpochs, maxDeltaPerEpoch, descentNumberOfSurroundingCells)))
    
    for i in range(0, amountOfProcesses - 1):
        processes.append(Process(target = makeRandomDatabaseMinimumSingleQueue, args = (q, math.ceil(numberOfDatapoints / amountOfProcesses), numberOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCellRange, False, numberOfDimensions, numberOfWidths, cutoff, amountOfEpochs, maxDeltaPerEpoch, descentNumberOfSurroundingCells)))
    
    for i in processes:
        i.start()
    
    dataDF = pd.concat([q.get() for i in range(0, amountOfProcesses)], ignore_index = True, sort = False)
    
    if type(filename) == str:
        # If wanted save the data to a json file.
        dataDF.to_json(filename + '.json', orient='columns')
    
    return dataDF











