def numberOfCalculationsGeneration(numberOfSurroundingCells, numberOfParticlesPerCell = 4):
    """
    Calculates the number of triangles/calculations needed to calculate the potential energy of a system. Can be used to predict calculation time.
    """
    x = numberOfSurroundingCells
    y = numberOfParticlesPerCell
    
    #numberOfCalculations = (1/6) * (1 + 2 * x)**2 * y * (2 - 3 * (1 + 2 * x)**2 * y + (1 + 2 * x)**4 * y**2) # Calculation with all triangles
    numberOfCalculations = (1/6) * y * (2 - 3 * y + 12 * x * (1 + x) * (-1 + y) * y + y**2 + 12 * x * (1 + x) * y * (-1 + 4 * x * y + 4 * y * x**2)) # Calculation with only one particle in the main cell.
    
    return numberOfCalculations