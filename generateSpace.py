import numpy as np


def generateSpace(coordinatesOfParticles, depthOfSurroundingCells, widthOfCell = 1.0, withoutBasisCell = True):
    """
    Generates the entire space based on the size of one cell.
    
    coordinatesOfParticles is are the coordinates of the particles in the cell. This variable is an array of numpy arrays (vectors).
    numberOfSurroundingCells is the number of cells surrounding the origin cell. So if it is 4 than the total space will be 9 by 9 cells.
    widthOfCell is the width/size of the cell. So if it is 1.0 than the cell has dimension 1.0x1.0 [length units]^2.
    
    >>> atoms = [np.array([0.3, 0.5]), np.array([0.9, 0.9]), np.array([0.6, 0.4]), np.array([0.5, 0.2])]
    >>> generateSpace(atoms, 1, 1.0, 2, False)
    [array([-0.7, -0.5]), array([-0.1, -0.1]), array([-0.4, -0.6]), array([-0.5, -0.8]), array([ 0.3, -0.5]), array([ 0.9, -0.1]), array([ 0.6, -0.6]), array([ 0.5, -0.8]), array([ 1.3, -0.5]), array([ 1.9, -0.1]), array([ 1.6, -0.6]), array([ 1.5, -0.8]), array([-0.7,  0.5]), array([-0.1,  0.9]), array([-0.4,  0.4]), array([-0.5,  0.2]), array([0.3, 0.5]), array([0.9, 0.9]), array([0.6, 0.4]), array([0.5, 0.2]), array([1.3, 0.5]), array([1.9, 0.9]), array([1.6, 0.4]), array([1.5, 0.2]), array([-0.7,  1.5]), array([-0.1,  1.9]), array([-0.4,  1.4]), array([-0.5,  1.2]), array([0.3, 1.5]), array([0.9, 1.9]), array([0.6, 1.4]), array([0.5, 1.2]), array([1.3, 1.5]), array([1.9, 1.9]), array([1.6, 1.4]), array([1.5, 1.2])]
    
    >>> atoms = [np.array([0.3, 0.5]), np.array([0.9, 0.9]), np.array([0.6, 0.4]), np.array([0.5, 0.2])]
    >>> generateSpace(atoms, 1, 1.0)
    [array([-0.7, -0.5]), array([-0.1, -0.1]), array([-0.4, -0.6]), array([-0.5, -0.8]), array([ 0.3, -0.5]), array([ 0.9, -0.1]), array([ 0.6, -0.6]), array([ 0.5, -0.8]), array([ 1.3, -0.5]), array([ 1.9, -0.1]), array([ 1.6, -0.6]), array([ 1.5, -0.8]), array([-0.7,  0.5]), array([-0.1,  0.9]), array([-0.4,  0.4]), array([-0.5,  0.2]), array([1.3, 0.5]), array([1.9, 0.9]), array([1.6, 0.4]), array([1.5, 0.2]), array([-0.7,  1.5]), array([-0.1,  1.9]), array([-0.4,  1.4]), array([-0.5,  1.2]), array([0.3, 1.5]), array([0.9, 1.9]), array([0.6, 1.4]), array([0.5, 1.2]), array([1.3, 1.5]), array([1.9, 1.9]), array([1.6, 1.4]), array([1.5, 1.2])]
    """
    totalSpace = []# The array in which all the atoms (their coordinates) will be placed).
    
    dimension = len(coordinatesOfParticles[0])
    
    cellCoordinates = [-depthOfSurroundingCells for i in range(dimension)]
    
    while True:#cellCoordinates[len(cellCoordinates) - 1]<=depthOfSurroundingCells:
        
        for i in range(len(cellCoordinates)):
            if cellCoordinates[i]>depthOfSurroundingCells:
                # If a cellCoordinate is large then the depth of the surrounding cells then make it minimal again and increase the next coordinate by one. Thus you will loop trough each possible permutation.
                cellCoordinates[i + 1] = cellCoordinates[i + 1] + 1
                cellCoordinates[i] = -depthOfSurroundingCells
        
        if not (withoutBasisCell and sum([0==cellCoordinate for cellCoordinate in cellCoordinates])==dimension):
            # If the basis cell shouldn't be included but all the cellCoordinates are zero then don't add particles this loop.
            for particle in coordinatesOfParticles:
                totalSpace.append(particle + np.array([widthOfCell * cellCoordinate for cellCoordinate in cellCoordinates]))
        
        if sum(cellCoordinates)==dimension*depthOfSurroundingCells:
            # If all cell coordinates are maximal the sum of it should be the dimension times the depth of surrounding cells and then the while loop should be stopped.
            break
        
        cellCoordinates[0] = cellCoordinates[0] + 1# Iterate the first cell coordinate.
    
    return totalSpace
    
    """
    for cellCoordinateX in range(-depthOfSurroundingCells, depthOfSurroundingCells + 1):
        for cellCoordinateY in range(-depthOfSurroundingCells, depthOfSurroundingCells + 1):
            # Runs trough all cell coordinates.
            
            if withoutBasisCell and cellCoordinateX == 0 and cellCoordinateY == 0:
                continue
            else:
                for particle in coordinatesOfParticles:
                    # Populates all cells with the with the particles in the basis cell.
                    totalSpace.append(particle + np.array([cellCoordinateX * widthOfCell, cellCoordinateY * widthOfCell]))
    """



if __name__ == "__main__":
    import doctest
    doctest.testmod()
