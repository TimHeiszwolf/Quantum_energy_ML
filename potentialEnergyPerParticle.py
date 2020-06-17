import numpy as np
from getTriangleLengths import *
from potentialEnergy import *


def potentialEnergyPerParticle(otherSpace, atoms, potentialEnergyFunction):
    """
    A function which takes take all possible purmutations of triangles within total space which has at least one praticle in the basis cell and then sums the energies of those purmutations and then normilizes it per particle.
    """
    return potentialEnergy(otherSpace, atoms, potentialEnergyFunction) / len(atoms)#len(atoms)#(len(otherSpace) + len(atoms))