import numpy as np

def potentialEnergy(otherSpace, particles, potentialEnergyFunction):
    """
    A function which takes take all possible purmutations of triangles within total space which has at least one praticle in the basis cell and then sums the energies of those purmutations.
    
    otherSpace is a list of vectors of coordinates of particles in outside the basis cell.
    particles is a list of vectors of coordinates of particles in the basis cell.
    potentialEnergyFunction is a function which takes the lengths of the triangles and produces a energy.
    
    >>> from generateSpace import *
    >>> atoms = [5 * np.array([0.3, 0.5]), 5 * np.array([0.9, 0.9]), 5 * np.array([0.6, 0.4]), 5 * np.array([0.5, 0.2])]
    >>> potentialEnergy([], atoms, potentialEnergyPerTrio)
    7.102489039238343
    
    >>> totalSpace = generateSpace(atoms, 0, 5.0)
    >>> potentialEnergy(totalSpace, atoms, potentialEnergyPerTrio) == potentialEnergy([], atoms, potentialEnergyPerTrio)
    True
    
    >>> totalSpace = generateSpace(atoms, 1, 5.0, False)
    >>> potentialEnergy([], totalSpace, potentialEnergyPerTrio)
    1818.4362042439122
    
    >>> totalSpace = generateSpace(atoms, 3, 5.0, False)
    >>> potentialEnergy([], totalSpace, potentialEnergyPerTrio)
    58164.66261472509
    
    >>> totalSpace = generateSpace(atoms, 1, 5.0)
    >>> potentialEnergy(totalSpace, atoms, potentialEnergyPerTrio)
    394.0349356721719
    
    >>> totalSpace = generateSpace(atoms, 3, 5.0)
    >>> potentialEnergy(totalSpace, atoms, potentialEnergyPerTrio)
    2367.6318905377134
    """
    potentialEnergyTotal = 0
    
    """
    for i in range(0, len(otherSpace)):
        for j in range(i + 1, len(otherSpace)):
            for k in range(j + 1, len(otherSpace)):
                # Every possible triangle outside the basis cell.
                lengths = getLengths([otherSpace[i], otherSpace[j], otherSpace[k]])
                potentialEnergyTotal = potentialEnergyTotal + potentialEnergyFunction(lengths)
    #"""
    
    for i in range(0, len(particles)):
        for j in range(0, len(otherSpace)):
            for k in range(0, len(otherSpace)):#j + 1
                if j==k:
                    continue
                # Every possible triangle with one particle in the basis cell.
                lengths = getLengths([particles[i], otherSpace[j], otherSpace[k]])
                potentialEnergyTotal = potentialEnergyTotal + (3/12) * potentialEnergyFunction(lengths)/6#Factor 6?#(3/4) * 
    
    for i in range(0, len(particles)):
        for j in range(0, len(particles)):#i + 1
            for k in range(0, len(otherSpace)):
                if i==j:
                    continue
                # Every possible triangle with two particles in the basis cell.
                lengths = getLengths([particles[i], particles[j], otherSpace[k]])
                potentialEnergyTotal = potentialEnergyTotal + (3/12) * potentialEnergyFunction(lengths)/6# Factor 6?#(3/4) * 
    
    for i in range(0, len(particles)):
        for j in range(0, len(particles)):#i + 1
            for k in range(0, len(particles)):#j + 1
                if i==j or j==k or i==k:
                    continue
                # Every possible triangle within the basis cell.
                lengths = getLengths([particles[i], particles[j], particles[k]])
                #print('Tri', (6/12) * potentialEnergyFunction(lengths)/6)
                potentialEnergyTotal = potentialEnergyTotal + (3/12) * potentialEnergyFunction(lengths)/6# Factor 6?#(3/4) * 
    
    #"""
    for i in range(0, len(particles)):
        for j in range(0, len(particles)):#i + 1
            if i==j:
                continue
            
            lengths = getLengths([particles[i], particles[j]])
            #print('Duo', (6/12) * potentialEnergyFunction(lengths)/2)
            potentialEnergyTotal = potentialEnergyTotal + (3/12) * potentialEnergyFunction(lengths)/2# Factor 2?#(1/4) * 
    
    for i in range(0, len(particles)):
        for j in range(0, len(otherSpace)):#i + 1
            #if i==j:
            #    continue
            
            lengths = getLengths([particles[i], otherSpace[j]])
            potentialEnergyTotal = potentialEnergyTotal + (3/12) * potentialEnergyFunction(lengths)/2# Factor 2?#(1/4) * 
    
    #"""
    
    return potentialEnergyTotal

def getLengths(vectors):
    """
    Gets the lengths of the sides of the triangles based on the vectors pointing towards each of the vertices.
    
    >>> getTriangleLengths([np.array([1,1]), np.array([2,-5]) ,np.array([0.4,3]]))
    [6.082762530298219, 2.08806130178211, 8.158431221748456]
    """
    lengths = []
    
    for i in range(0, len(vectors)):
        for j in range(i + 1, len(vectors)):
            differenceVector = vectors[i] - vectors[j]
            lengths.append(np.sqrt(differenceVector.dot(differenceVector)))
    
    return lengths


def potentialEnergyPerParticle(otherSpace, atoms, potentialEnergyFunction):
    """
    A function which takes take all possible purmutations of triangles within total space which has at least one praticle in the basis cell and then sums the energies of those purmutations and then normilizes it per particle.
    """
    return potentialEnergy(otherSpace, atoms, potentialEnergyFunction) / len(atoms)#len(atoms)#(len(otherSpace) + len(atoms))



def potentialEnergyPerSet(lengths, E0=1, Rc=1):
    """
    The (simplified) potential energy based on the lengths of the sides of a triangle (a, b and c).
    
    >>> potentialEnergyPerTrio([20, 20, 20])
    0.0
    
    >>> potentialEnergyPerTrio([0.1, 0.6, 1])
    1383087510.7362177
    
    >>> potentialEnergyPerTrio([0.01, 0.006, 0.001])
    1.3830891814439465e+25
    
    >>> potentialEnergyPerTrio([0.7211102550927979, 0.36055512754639896, 0.8062257748298549])
    47801.621030097835
    
    >>> potentialEnergyPerTrio([1, 1, 1])
    -13.83088344325057
    """
    Mc = 1
    A0 = 1
    n = 6
    R = 2 * Rc
    
    #a = Mc * lengths[0] / (3 * Rc)
    #b = Mc * lengths[1] / (3 * Rc)
    #c = Mc * lengths[2] / (3 * Rc)
    
    semiCircumference = np.mean([Mc * length / Rc for length in lengths])#a + b + c
    #s = (a + b + c) / 2
    #area2Triangle = s * (s - a) * (s - b) * (s - c)
    
    if semiCircumference >= R:
        return 0.0
    else:
        longRangePotential = -2 * (1 / (semiCircumference**n) - 1 / (R**n))
        shortRangePotential = (1 / (semiCircumference**(2 * n)) - 1 / (R**(2 * n)))
        correction = -(2 * n / (R**(n + 1))) * (1 - 1/(R**n)) * (semiCircumference - R)
        
        return E0 * A0 * (shortRangePotential + longRangePotential + correction)






if __name__ == "__main__":
    import doctest
    doctest.testmod()
