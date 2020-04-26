import numpy as np
from getTriangleLengths import *

def potentialEnergy(otherSpace, particles, potentialEnergyFunction):
    """
    A function which takes take all possible purmutations of triangles within total space which has at least one praticle in the basis cell and then sums the energies of those purmutations.
    
    otherSpace is a list of vectors of coordinates of particles in outside the basis cell
    particles is a list of vectors of coordinates of particles in the basis cell
    potentialEnergyFunction is a function which takes the lengths of the triangles and produces a energy.
    
    >>> from potentialEnergyPerTrio import *
    >>> from generateSpace import *
    >>> atoms = [np.array([0.3, 0.5]), np.array([0.9, 0.9]), np.array([0.6, 0.4]), np.array([0.5, 0.2])]
    >>> potentialEnergy([], atoms, potentialEnergyPerTrio)
    2441605.1812992394
    
    >>> totalSpace = generateSpace(atoms, 0, 1.0)
    >>> potentialEnergy(totalSpace, atoms, potentialEnergyPerTrio) == potentialEnergy([], atoms, potentialEnergyPerTrio)
    True
    
    >>> totalSpace = generateSpace(atoms, 1, 1.0, False)
    >>> potentialEnergy([], totalSpace, potentialEnergyPerTrio)
    88870702.37461296
    
    >>> totalSpace = generateSpace(atoms, 3, 1.0, False)
    >>> potentialEnergy([], totalSpace, potentialEnergyPerTrio)
    1926302668.3391948
    
    >>> totalSpace = generateSpace(atoms, 1, 1.0)
    >>> potentialEnergy(totalSpace, atoms, potentialEnergyPerTrio)
    19070318.37682746
    
    >>> totalSpace = generateSpace(atoms, 3, 1.0)
    >>> potentialEnergy(totalSpace, atoms, potentialEnergyPerTrio)
    78355980.97411288
    """
    
    potentialEnergyTotal = 0# np.sum(np.sum(np.sum([[[potentialEnergyFunction(getTriangleLengths(totalSpace[i], totalSpace[j], totalSpace[k])) for k in range(j + 1, len(totalSpace))] for j in range(i + 1, len(totalSpace))] for i in range(0, len(totalSpace))])))# This is the old method.
    
    for i in range(0, len(particles)):
        for j in range(0, len(otherSpace)):
            for k in range(j + 1, len(otherSpace)):
                # Every possible triangle with one particle in the basis cell.
                lengths = getTriangleLengths(particles[i], otherSpace[j], otherSpace[k])
                potentialEnergyTotal = potentialEnergyTotal + potentialEnergyFunction(lengths)
    
    for i in range(0, len(particles)):
        for j in range(i + 1, len(particles)):
            for k in range(0, len(otherSpace)):
                # Every possible triangle with two particles in the basis cell
                lengths = getTriangleLengths(particles[i], particles[j], otherSpace[k])
                potentialEnergyTotal = potentialEnergyTotal + potentialEnergyFunction(lengths)
    
    for i in range(0, len(particles)):
        for j in range(i + 1, len(particles)):
            for k in range(j + 1, len(particles)):
                # Every possible triangle within the basis cell.
                lengths = getTriangleLengths(particles[i], particles[j], particles[k])
                potentialEnergyTotal = potentialEnergyTotal + potentialEnergyFunction(lengths)
    
    return potentialEnergyTotal


if __name__ == "__main__":
    import doctest
    doctest.testmod()