import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
from generateSpace import *


def plotLattice(totalSpace, widthOfCell = 1.0, plotBorders = True):
    """
    Plots the lattice/space in a scatter graph with the grid as cell borders.
    
    totalSpace is are the coordinates of the particles in the space. This variable is an array of numpy arrays (vectors).
    widthOfCell is the width/size of the cell. So if it is 1.0 than the cell has dimension 1.0x1.0 [length units]^2
    plotBorders is a boolean representing wether or not borders of the cells are plotted.
    """
    toPlot = [[totalSpace[j][i] for j in range(len(totalSpace))] for i in range(len(totalSpace[0]))] # Transposing totalSpace such that the toPlot[0] are all the x coordinates, toPlot[1] are the y coordinates, etc.
    
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(x=toPlot[0], y=toPlot[1], marker='o', c='r')
    ax.set_title('Position of particles.')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    
    ax.set_xlim((0 - min(toPlot[0])%widthOfCell) + min(toPlot[0]), (widthOfCell - max(toPlot[0])%widthOfCell) + max(toPlot[0]))
    ax.set_ylim((0 - min(toPlot[1])%widthOfCell) + min(toPlot[1]), (widthOfCell - max(toPlot[1])%widthOfCell) + max(toPlot[1]))
    
    
    if plotBorders:
        # Add a grid which represents the borders of the cell if wanted.
        ax.xaxis.set_major_locator(MultipleLocator(widthOfCell))
        ax.yaxis.set_major_locator(MultipleLocator(widthOfCell))
        ax.xaxis.set_minor_locator(AutoMinorLocator(5))
        ax.yaxis.set_minor_locator(AutoMinorLocator(5))
    
        ax.grid(which='both')
        ax.grid(which='minor', alpha=0.2)
    
    plt.show()
    
    return ax


def plotLatticeFromDataFrame(dataFrame, indexNumber, plotBorders = True):
    """
    Plots the lattice/space in a scatter graph with the grid as cell borders.
    
    dataFrame is the pandas DataFrame containing all the data (of the entire database).
    indexNumber is the number of the index from the pandas DataFrame which yu want to plot.
    plotBorders is a boolean representing wether or not borders of the cells are plotted.
    """
    space = generateSpace(dataFrame['particleCoordinates'][indexNumber], dataFrame['numberOfSurroundingCells'][indexNumber], dataFrame['widthOfCell'][indexNumber], False)
    return plotLattice(space, dataFrame['widthOfCell'][indexNumber], plotBorders)