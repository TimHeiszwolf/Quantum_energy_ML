import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import math
from multiprocessing import Process, Queue


def prepareDatabseForMachineLearning(data, orderOfMatrix, filename = False, giveUpdates = True):
    """
    A function which takes a generated dataframe and prepares it for machine learning by making the proximity matrices and calculating their eigenvalues.
    
    data is the dataframe (as generated by makeRandomDatabase) for which the eigenvalues of the proximity matrices should be calculated.
    orderOfMatrix is a list of the 'order' (power to which the relative distance is taken) for each proximity matrix.
    filename is the name of the file the database get's exported to. The .json file extension get's added in the code itself. If the type of filename is not a string no file will be saved.
    giveUpdates is a boolean which determines if updates about the progress of the database preperation get's printed.
    
    """
    
    timeStart = time.time()
    data = data.reset_index()
    numberOfDatapoints = len(data['particleCoordinates'])
    eigenvalues = []
    
    for a in range(0, numberOfDatapoints):
        # Loop trough each datapoint
        coordinates = data['particleCoordinates'][a]
        widthOfCell = data['widthOfCell'][a]
        numberOfSurroundingCells = data['numberOfSurroundingCells'][a]
        
        eigenvaluesRow = []
        
        for order in orderOfMatrix:
            matrix = np.zeros((len(coordinates), len(coordinates)))
            
            for i in range(0, len(coordinates)):
                for j in range(i, len(coordinates)):
                    # Loop trough all matrix elements and define their proximity.
                    sumOfProximity = 0
                    
                    for x in range(-numberOfSurroundingCells, numberOfSurroundingCells + 1):
                        for y in range(-numberOfSurroundingCells, numberOfSurroundingCells + 1):
                            # Run trough all 'mirror images'.
                            if i == j and x == 0 and y == 0:
                                # Prevent self-proximity with the same particle.
                                continue
                            
                            vectorA = coordinates[i]
                            vectorB = coordinates[j] + np.array([x * widthOfCell, y * widthOfCell])
                            differenceVector = vectorA - vectorB
                            
                            sumOfProximity = sumOfProximity + math.pow(differenceVector.dot(differenceVector), (order/2))
                        
                    matrix[i][j] = sumOfProximity
            
            for i in range(0, len(coordinates)):
                for j in range(0, i):
                    # Since the matrix is symetric make sure that you don't do the same calculation twice.
                    matrix[i][j] = matrix[j][i]
            
            eigenvalue, eigenVector = np.linalg.eig(matrix)
            [eigenvaluesRow.append(i) for i in eigenvalue]
            #eigenvaluesRow.append(eigenvalue)
        
        eigenvalues.append(eigenvaluesRow)
        
        if giveUpdates:
            expectedTimeLeft = (numberOfDatapoints - 1 - a) / ((a + 1) / (time.time() - timeStart))
            print(str(math.ceil(100 * (a + 1) / (numberOfDatapoints))).rjust(3, ' '), '% done, expected time left', math.ceil(expectedTimeLeft), 'seconds,', math.ceil(time.time() - timeStart), 'seconds since start.')
    
    data['eigenvalues'] = eigenvalues
    
    if type(filename) == str:
        # If wanted save the data to a json file.
        dataDF.to_json(filename + '.json', orient='columns')
    
    return data


def prepareDatabseForMachineLearningSingleQueue(q, data, orderOfMatrix, giveUpdates):
    q.put(prepareDatabseForMachineLearning(data, orderOfMatrix, False, giveUpdates))


def prepareDatabseForMachineLearningMultiprocessing(data, orderOfMatrix, filename = False, amountOfProcesses = 5):
    """
    A function which impliments multiprocessing for the prepareDatabseForMachineLearning function.
    """
    q = Queue()
    processes = []
    splitData = np.array_split(data, amountOfProcesses)
    print('Using multiprocessing only the first procces gives updates')
    
    processes.append(Process(target = prepareDatabseForMachineLearningSingleQueue, args = (q, splitData[0], orderOfMatrix, True)))
    
    for i in range(1, amountOfProcesses):
        processes.append(Process(target = prepareDatabseForMachineLearningSingleQueue, args = (q, splitData[i], orderOfMatrix, False)))
        
    for i in processes:
        i.start()
    
    dataDF = pd.concat([q.get() for i in range(0, amountOfProcesses)], ignore_index = True, sort = False)
    
    if type(filename) == str:
        # If wanted save the data to a json file.
        dataDF.to_json(filename + '.json', orient='columns')
    
    return dataDF