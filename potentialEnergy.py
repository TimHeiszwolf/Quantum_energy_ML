import numpy as np
from getTriangleLengths import *

def potentialEnergy(totalSpace, potentialEnergyFunction):
    """
    A function which takes take all possible purmutations of triangles within total space and then sums the energies of those purmutations.
    
    >>> from potentialEnergyPerTrio import *
    >>> atoms = [np.array([0.3, 0.5]), np.array([0.9, 0.9]), np.array([0.6, 0.4]), np.array([0.5, 0.2])]
    >>> potentialEnergy(atoms, potentialEnergyPerTrio)
    2441605.1812992394
    
    >>> from generateSpace import *
    >>> totalSpace = generateSpace(atoms, 1, 1.0)
    >>> potentialEnergy(totalSpace, potentialEnergyPerTrio)
    88870702.37461296
    
    >>> totalSpace = generateSpace(atoms, 3, 1.0)
    >>> potentialEnergy(totalSpace, potentialEnergyPerTrio)
    1926302668.3391948
    
    """
    
    potentialEnergyTotal = 0# np.sum(np.sum(np.sum([[[potentialEnergyFunction(getTriangleLengths(totalSpace[i], totalSpace[j], totalSpace[k])) for k in range(j + 1, len(totalSpace))] for j in range(i + 1, len(totalSpace))] for i in range(0, len(totalSpace))])))
    
    for i in range(0, len(totalSpace)):
        for j in range(i + 1, len(totalSpace)):
            for k in range(j + 1, len(totalSpace)):
                
                lengths = getTriangleLengths(totalSpace[i], totalSpace[j], totalSpace[k])
                potentialEnergyTotal = potentialEnergyTotal + potentialEnergyFunction(lengths)
                #print('Particle ' + str(i) + ', ' + str(j) + ' and ' + str(k) + ' with lengths ', lengths, ' and potential energy ', potentialEnergyFunction(lengths))
    
    return potentialEnergyTotal


if __name__ == "__main__":
    import doctest
    doctest.testmod()