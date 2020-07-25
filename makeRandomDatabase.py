import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import random
import math
from multiprocessing import Process, Queue

from generateSpace import *
from plotLattice import *
from potentialEnergy import *
from numberOfCalculations import *


def makeRandomDatabaseMinimum(numberOfDatapoints, depthOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCellRange=[1, 1], filename=False, giveUpdates=True, numberOfDimensions=2, numberOfWidths=100, cutoff=0.5, amountOfScans=40, maxDeltaPerEpoch=0.01, descentdepthOfSurroundingCells=2):
    """
    A function that generates a random database of particle configurations and their potential energies.
    
    numberOfDatapoints is the length/amount of datapoints in the final database.
    depthOfSurroundingCells is the 'depth' of the surrounding cells (in a square) so if it is two then the total grid is five by five cells large.
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
        # For each width of the cell repeat the procces.
        widthOfCell = np.linspace(widthOfCellRange[0], widthOfCellRange[1], numberOfWidths)[loopNumber]# Could also use np.logspace
        
        data = {'particleCoordinates':list(np.zeros((math.ceil(numberOfDatapoints / numberOfWidths), numberOfParticlesPerCell, numberOfDimensions))), 'widthOfCell':[], 'depthOfSurroundingCells': [], 'potentialEnergy':[]}# Initialy use a dictionary because it's easier to append to than a dataframe.
        
        if giveUpdates:
            print('Generating space with width', widthOfCell)
        
        for i in range(0, math.ceil(numberOfDatapoints / numberOfWidths)):
            # Generate the required number of datapoints.
            data['widthOfCell'].append(widthOfCell)
            data['depthOfSurroundingCells'].append(depthOfSurroundingCells)
        
        for i in range(0, numberOfDimensions):
            # Generate the particle coordinates. First all the X coordinates for each partile and datapoint and then the Y and so on.
            for j in range(0, numberOfParticlesPerCell):
                for k in range(0, math.ceil(numberOfDatapoints / numberOfWidths)):
                    data['particleCoordinates'][k][j][i] = random.uniform(0, data['widthOfCell'][k])
        
        totalAcceptedRateLastTen = []
        
        for i in range(0, math.ceil(numberOfDatapoints / numberOfWidths)):
            # Next for each datapoint to be generated (in this cell width) the potential energy is refined (with the relaxation procces) and calculated.
            oldOtherSpace = generateSpace(data['particleCoordinates'][i], descentdepthOfSurroundingCells, data['widthOfCell'][i])
            oldPotentialEnergy = potentialEnergyPerParticle(oldOtherSpace, data['particleCoordinates'][i], potentialEnergyFunction)
            
            changeAccepted = []
            
            for j in range(amountOfScans):
                # The relaxation procces.
                
                for particleNumber in range(len(data['particleCoordinates'][i])):
                    # Loop trough all particles.
                    newCoordinates = np.copy(data['particleCoordinates'][i])
                    newCoordinates[particleNumber] = newCoordinates[particleNumber] + np.array([maxDeltaPerEpoch * random.uniform(-1, 1) for a in range(0, numberOfDimensions)])# Move the particle a random amount in a random direction.
                    #direction = random.randint(0, numberOfDimensions - 1)
                    #newCoordinates[particleNumber][direction] = newCoordinates[particleNumber][direction] + maxDeltaPerEpoch * random.uniform(-1, 1)
                    
                    for k in range(len(newCoordinates[particleNumber])):
                        # Make sure the particle stays in the unit cell.
                        if newCoordinates[particleNumber][k] < 0:
                            newCoordinates[particleNumber][k] = newCoordinates[particleNumber][k] +  data['widthOfCell'][i]
                        elif newCoordinates[particleNumber][k] > data['widthOfCell'][i]:
                            newCoordinates[particleNumber][k] = newCoordinates[particleNumber][k] -  data['widthOfCell'][i]
                    
                    newOtherSpace = generateSpace(newCoordinates, descentdepthOfSurroundingCells, data['widthOfCell'][i])
                    newPotentialEnergy = potentialEnergyPerParticle(oldOtherSpace, newCoordinates, potentialEnergyFunction)
                    
                    if newPotentialEnergy <= oldPotentialEnergy:
                        # Accept (or reject) the change in position depending on wheter the new potential energy is higher or lower.
                        data['particleCoordinates'][i] = newCoordinates
                        oldPotentialEnergy = newPotentialEnergy
                        changeAccepted.append(1)
                    else:
                        changeAccepted.append(0)
                    
                    """
                    if giveUpdates:
                        numberOfCalculationsDone = i + 1 + loopNumber * math.ceil(numberOfDatapoints / numberOfWidths)
                        print(str(math.ceil(100 * numberOfCalculationsDone / totalNumberOfCalculations)).rjust(3, ' '), '% done, expected time left', math.ceil((time.time() - startTime) * (totalNumberOfCalculations - numberOfCalculationsDone) / numberOfCalculationsDone), 'seconds,', math.ceil(time.time() - startTime), 'seconds since start, on width of cell', widthOfCell, 'datapoint', i + 1, 'out of', 1 + math.ceil(numberOfDatapoints / numberOfWidths), 'epoch', j + 1, 'particle', particleNumber, 'a lower energy was found:', newPotentialEnergy <= oldPotentialEnergy)
                    #"""
            
            totalAcceptedRateLastTen.append([100 * changeAccepted[-temp - 1] for temp in range(10)])
            
            if giveUpdates:
                numberOfCalculationsDone = i + 1 + loopNumber * math.ceil(numberOfDatapoints / numberOfWidths)
                print(str(math.ceil(100 * numberOfCalculationsDone / totalNumberOfCalculations)).rjust(3, ' '), '% done, expected time left', math.ceil((time.time() - startTime) * (totalNumberOfCalculations - numberOfCalculationsDone) / numberOfCalculationsDone), 'seconds,', math.ceil(time.time() - startTime), 'seconds since start, on width of cell', widthOfCell, 'datapoint', i + 1, 'out of', str(math.ceil(numberOfDatapoints / numberOfWidths)) + ', the acceptance rate of the first 16 was:', 100 * np.mean([changeAccepted[temp] for temp in range(16)]), '%', 'the acceptance rate of the last 16 was:', 100 * np.mean([changeAccepted[-temp - 1] for temp in range(16)]), '%')
            
            otherSpace = generateSpace(data['particleCoordinates'][i], data['depthOfSurroundingCells'][i], data['widthOfCell'][i])# Generate the other space.
            data['potentialEnergy'].append(potentialEnergyPerParticle(otherSpace, data['particleCoordinates'][i], potentialEnergyFunction))# Calculate the potential energy and save it to the data dictonairy.
            
        dataDF = pd.DataFrame(data)# Turn the data into a pandas DataFrame to make data easier to handle.
        qHi  = dataDF['potentialEnergy'].quantile(cutoff)# Cutt off the higher energies of the database.
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
        print('Done generating database. Took :', math.ceil(endTime - startTime), 'seconds. Average acceptance rate of last 10 epochs out of', amountOfScans,'epochs was:', np.mean(totalAcceptedRateLastTen), '+-', np.std(totalAcceptedRateLastTen)/np.sqrt(len(totalAcceptedRateLastTen)), '%.')# Inform the user of how the procces has progressed.
    
    finalDataFrame = pd.concat(dataFrames, ignore_index = True, sort = False)
    
    if type(filename) == str:
        # If wanted save the data to a json file.
        finalDataFrame.to_json(filename + '.json', orient='columns')
    
    return finalDataFrame


def makeRandomDatabaseMinimumSingleQueue(q, numberOfDatapoints, depthOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCellRange, giveUpdates, numberOfDimensions, numberOfWidths, cutoff, amountOfScans, maxDeltaPerEpoch, descentdepthOfSurroundingCells):
    q.put(makeRandomDatabaseMinimum(numberOfDatapoints, depthOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCellRange, False, giveUpdates, numberOfDimensions, numberOfWidths, cutoff, amountOfScans, maxDeltaPerEpoch, descentdepthOfSurroundingCells))


def makeRandomDatabaseMinimumMultiprocessing(numberOfDatapoints, depthOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCellRange=[1, 1], filename=False, amountOfProcesses=5, numberOfDimensions=2, numberOfWidths=100, cutoff=0.5, amountOfScans=4, maxDeltaPerEpoch=0.01, descentdepthOfSurroundingCells=2):
    """
    A function that impliments multiprocessing for the generation of the database.
    """
    q = Queue()
    
    processes = []
    print('Using multiprocessing only the first procces gives updates')
    processes.append(Process(target = makeRandomDatabaseMinimumSingleQueue, args = (q, math.ceil(numberOfDatapoints / amountOfProcesses), depthOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCellRange, True, numberOfDimensions, numberOfWidths, cutoff, amountOfScans, maxDeltaPerEpoch, descentdepthOfSurroundingCells)))
    
    for i in range(0, amountOfProcesses - 1):
        processes.append(Process(target = makeRandomDatabaseMinimumSingleQueue, args = (q, math.ceil(numberOfDatapoints / amountOfProcesses), depthOfSurroundingCells, numberOfParticlesPerCell, potentialEnergyFunction, widthOfCellRange, False, numberOfDimensions, numberOfWidths, cutoff, amountOfScans, maxDeltaPerEpoch, descentdepthOfSurroundingCells)))
    
    for i in processes:
        i.start()
    
    dataDF = pd.concat([q.get() for i in range(0, amountOfProcesses)], ignore_index = True, sort = False)
    
    if type(filename) == str:
        # If wanted save the data to a json file.
        dataDF.to_json(filename + '.json', orient='columns')
    
    return dataDF











