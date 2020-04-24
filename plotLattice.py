import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)

def plotLattice(totalSpace, widthOfCell = 1.0, plotBorders = True):
    """
    
    """
    
    toPlot = [[totalSpace[j][i] for j in range(len(totalSpace))] for i in range(len(totalSpace[0]))] # Transposing totalSpace such that the toPlot[0] are all the x coordinates, toPlot[1] are the y coordinates, etc.
    
    
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(x=toPlot[0], y=toPlot[1], marker='o', c='r')
    ax.set_title('Position of partiles ')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    
    ax.set_xlim((0 - min(toPlot[0])%widthOfCell) + min(toPlot[0]), (widthOfCell - max(toPlot[0])%widthOfCell) + max(toPlot[0]))
    ax.set_ylim((0 - min(toPlot[1])%widthOfCell) + min(toPlot[1]), (widthOfCell - max(toPlot[1])%widthOfCell) + max(toPlot[1]))
    
    
    if plotBorders:
        
        ax.xaxis.set_major_locator(MultipleLocator(widthOfCell))
        ax.yaxis.set_major_locator(MultipleLocator(widthOfCell))
        ax.xaxis.set_minor_locator(AutoMinorLocator(5))
        ax.yaxis.set_minor_locator(AutoMinorLocator(5))
    
        ax.grid(which='both')
        ax.grid(which='minor', alpha=0.2)
    
    plt.show()
