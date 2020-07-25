import numpy as np

def potentialEnergy(otherSpace, particles, potentialEnergyFunction):
    """
    A function which takes take all possible purmutations of triangles within total space which has at least one praticle in the basis cell and then sums the energies of those purmutations.
    
    otherSpace is a list of vectors of coordinates of particles in outside the basis cell.
    particles is a list of vectors of coordinates of particles in the basis cell.
    potentialEnergyFunction is a function which takes the lengths of the triangles and produces a energy.
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
                potentialEnergyTotal = potentialEnergyTotal + (3/4) * potentialEnergyFunction(lengths)#Factor 6?#(3/4) * 
    
    for i in range(0, len(particles)):
        for j in range(0, len(particles)):#i + 1
            for k in range(0, len(otherSpace)):
                if i==j:
                    continue
                # Every possible triangle with two particles in the basis cell.
                lengths = getLengths([particles[i], particles[j], otherSpace[k]])
                potentialEnergyTotal = potentialEnergyTotal + (3/4) * potentialEnergyFunction(lengths)# Factor 6?#(3/4) * 
    
    for i in range(0, len(particles)):
        for j in range(0, len(particles)):#i + 1
            for k in range(0, len(particles)):#j + 1
                if i==j or j==k or i==k:
                    continue
                # Every possible triangle within the basis cell.
                lengths = getLengths([particles[i], particles[j], particles[k]])
                #print('Tri', (3/4) * potentialEnergyFunction(lengths))
                potentialEnergyTotal = potentialEnergyTotal + (3/4) * potentialEnergyFunction(lengths)# Factor 6?#(3/4) * 
    
    #"""
    for i in range(0, len(particles)):
        for j in range(0, len(particles)):#i + 1
            if i==j:
                continue
            
            lengths = getLengths([particles[i], particles[j]])
            #print('Duo',  (1/4) * potentialEnergyFunction(lengths))
            potentialEnergyTotal = potentialEnergyTotal + (1/4) * potentialEnergyFunction(lengths)# Factor 2?#(1/4) * 
    
    for i in range(0, len(particles)):
        for j in range(0, len(otherSpace)):#i + 1
            #if i==j:
            #    continue
            
            lengths = getLengths([particles[i], otherSpace[j]])
            potentialEnergyTotal = potentialEnergyTotal + (1/4) * potentialEnergyFunction(lengths)# Factor 2?#(1/4) * 
    
    #"""
    
    return potentialEnergyTotal


def getLengths(vectors):
    """
    Gets the lengths of the sides of the triangles based on the vectors pointing towards each of the vertices.
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
    The (simplified) potential energy based on the lengths of the sides of a triangle (a, b and c). See the report for details.
    """
    n = 6
    R = 2 * Rc
    
    #a = Mc * lengths[0] / (3 * Rc)
    #b = Mc * lengths[1] / (3 * Rc)
    #c = Mc * lengths[2] / (3 * Rc)
    
    semiCircumference = np.mean([length / Rc for length in lengths])#a + b + c
    #s = (a + b + c) / 2
    #area2Triangle = s * (s - a) * (s - b) * (s - c)
    
    if semiCircumference >= R:
        return 0.0
    else:
        longRangePotential = -2 * (1 / (semiCircumference**n) - 1 / (R**n))
        shortRangePotential = (1 / (semiCircumference**(2 * n)) - 1 / (R**(2 * n)))
        correction = -(2 * n / (R**(n + 1))) * (1 - 1/(R**n)) * (semiCircumference - R)
        
        return E0 * (shortRangePotential + longRangePotential + correction)