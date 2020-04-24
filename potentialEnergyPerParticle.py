import numpy as np
from getTriangleLengths import *
from potentialEnergy import *

def potentialEnergyPerParticle(totalSpace, potentialEnergyFunction):
    """
    A function which takes take all possible purmutations of triangles within total space and then sums the energies of those purmutations and then normilizes it per particle.
    """
    
    return potentialEnergy(totalSpace, potentialEnergyFunction) / len(totalSpace)