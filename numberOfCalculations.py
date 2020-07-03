def numberOfCalculationsGeneration(numberOfSurroundingCells, numberOfParticlesPerCell = 4):
    """
    Calculates the number of triangles/calculations needed to calculate the potential energy of a system. Can be used to predict calculation time.
    """
    x = numberOfSurroundingCells
    y = numberOfParticlesPerCell
    
    #numberOfCalculations = (1/6) * (1 + 2 * x)**2 * y * (2 - 3 * (1 + 2 * x)**2 * y + (1 + 2 * x)**4 * y**2) # Calculation with all triangles
    numberOfCalculations = (1/6) * y * (2 - 3 * y + 12 * x * (1 + x) * (-1 + y) * y + y**2 + 12 * x * (1 + x) * y * (-1 + 4 * x * y + 4 * y * x**2)) # Calculation with only one particle in the main cell.
    
    return numberOfCalculations
    
    
    
def numberOfCalcultions(Np, Ds, d=2):
    
    calculations = [((-1 + Np) * Np + (-1 + (1 + 2 * Ds)**d) * Np**2), ((-2 + Np) * (-1 + Np) * Np + (-1 + (1 + 2 * Ds)**d) * (-1 + Np) * Np**2 + (-1 + (1 + 2 * Ds)**d) * Np**2 * (-1 + (-1 + (1 + 2 * Ds)**d) * Np))]
    
    return calculations
         
def calculationTime(Np, Ds, d=2, relaxingDs=1, epochs=0, Cp=30*10**-6, Ct=40*10**-6):
    #CP calculation time pair
    #CT calculationTime triangle
    calculations = numberOfCalcultions(Np, Ds, d)
    
    calculationsRelax = numberOfCalcultions(Np, relaxingDs, d)
    
    time = Cp * (calculations[0] + epochs * calculationsRelax[0]) + Ct * (calculations[1] + epochs * calculationsRelax[1])
    
    return time