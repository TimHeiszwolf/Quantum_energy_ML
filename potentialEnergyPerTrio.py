import math
import numpy as np


def potentialEnergyPerTrio(lengths, E0=1, Rc=1):
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
    Mc = 1 / 3
    A0 = 1
    n = 6
    R = 2 * Rc
    
    a = Mc * lengths[0] / Rc
    b = Mc * lengths[1] / Rc
    c = Mc * lengths[2] / Rc
    
    circumference = a + b + c
    #s = (a + b + c) / 2
    #area2Triangle = s * (s - a) * (s - b) * (s - c)
    
    if circumference >= R:
        return 0.0
    else:
        longRangePotential = -2 * (1 / (circumference**n) - 1 / (R**n))
        shortRangePotential = (1 / (circumference**(2 * n)) - 1 / (R**(2 * n)))
        correction = -(2 * n / (R**(n + 1))) * (1 - 1/(R**n)) * (circumference - R)
        
        return E0 * A0 * (shortRangePotential + longRangePotential + correction)

if __name__ == "__main__":
    import doctest
    doctest.testmod()