import numpy as np

def generateSpace(coordinatesOfParticles, numberOfSurroundingCells = 4, widthOfCell = 1.0):
    """
    Generates the entire space based on the size of one cell.
    
    coordinatesOfParticles is are the coordinates of the particles in the cell. This variable is an array of numpy arrays (vectors).
    numberOfSurroundingCells is the number of cells surrounding the origin cell. So if it is 4 than the total space will be 9 by 9 cells.
    widthOfCell is the width/size of the cell. So if it is 1.0 than the cell has dimension 1.0x1.0 [length units]^2
    
    >>> atoms = [np.array([0.3, 0.5]), np.array([0.9, 0.9]), np.array([0.6, 0.4]), np.array([0.5, 0.2])]
    >>> generateSpace(atoms, 1, 1.0)
    [array([-0.7, -0.5]), array([-0.1, -0.1]), array([-0.4, -0.6]), array([-0.5, -0.8]), array([-0.7,  0.5]), array([-0.1,  0.9]), array([-0.4,  0.4]), array([-0.5,  0.2]), array([-0.7,  1.5]), array([-0.1,  1.9]), array([-0.4,  1.4]), array([-0.5,  1.2]), array([ 0.3, -0.5]), array([ 0.9, -0.1]), array([ 0.6, -0.6]), array([ 0.5, -0.8]), array([0.3, 0.5]), array([0.9, 0.9]), array([0.6, 0.4]), array([0.5, 0.2]), array([0.3, 1.5]), array([0.9, 1.9]), array([0.6, 1.4]), array([0.5, 1.2]), array([ 1.3, -0.5]), array([ 1.9, -0.1]), array([ 1.6, -0.6]), array([ 1.5, -0.8]), array([1.3, 0.5]), array([1.9, 0.9]), array([1.6, 0.4]), array([1.5, 0.2]), array([1.3, 1.5]), array([1.9, 1.9]), array([1.6, 1.4]), array([1.5, 1.2])]
    
    """
    
    totalSpace = []# The array in which all the atoms (their coordinates) will be placed).
    
    for cellCoordinateX in range(-numberOfSurroundingCells, numberOfSurroundingCells + 1):
        for cellCoordinateY in range(-numberOfSurroundingCells, numberOfSurroundingCells + 1):
            # Runs trough all cell coordinates.
            for particle in coordinatesOfParticles:
                # Populates all cells with the with the particles in the basis cell.
                totalSpace.append(particle + np.array([cellCoordinateX * widthOfCell, cellCoordinateY * widthOfCell]))
    
    return totalSpace



if __name__ == "__main__":
    import doctest
    doctest.testmod()
