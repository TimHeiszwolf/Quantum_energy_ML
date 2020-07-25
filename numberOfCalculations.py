
def numberOfCalcultions(Np, Ds, d=2):
    """
    The number of calculations needed for a potential energy calculation.
    Np is the number of particles per cell.
    Ds is the depth of the surrounding cells.
    d is the dimension of the calculation.
    """
    calculations = [((-1 + Np) * Np + (-1 + (1 + 2 * Ds)**d) * Np**2), ((-2 + Np) * (-1 + Np) * Np + (-1 + (1 + 2 * Ds)**d) * (-1 + Np) * Np**2 + (-1 + (1 + 2 * Ds)**d) * Np**2 * (-1 + (-1 + (1 + 2 * Ds)**d) * Np))]
    
    return calculations
         
def calculationTime(Np, Ds, d=2, relaxingDs=1, scans=0, Cp=30*10**-6, Ct=40*10**-6):
    """
    The total calculation time used to generate a datapoint.
    Np is the number of particles per cell.
    Ds is the depth of the surrounding cells.
    d is the dimension of the calculation.
    relaxingDs is the depth of surrounding cells used during the relaxation procces.
    scans is the amount of particle scans during the relaxation procces.
    Cp is the calculation time of the potential energie per pair in the sum.
    Ct is the calculation time of the potential energie per triplet in the sum.
    """
    calculations = numberOfCalcultions(Np, Ds, d)
    calculationsRelax = numberOfCalcultions(Np, relaxingDs, d)
    
    return Cp * (calculations[0] + scans * calculationsRelax[0]) + Ct * (calculations[1] + scans * calculationsRelax[1])