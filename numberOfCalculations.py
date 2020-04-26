def numberOfCalculations(numberOfSurroundingCells, numberOfParticlesPerCell = 4):
    """
    Calculates the number of triangles/calculations needed to calculate the potential energy of a system. Can be used to predict calculation time.
    """
    x = numberOfSurroundingCells
    y = numberOfParticlesPerCell
    
    numberOfCalculations = (1/6) * y * (2 - 3 * y + 12 * x * (1 + x) * (-1 + y) * y + y**2 + 12 * x * (1 + x) * y * (-1 + 4 * x * y + 4 * y * x**2))
    
    return numberOfCalculations