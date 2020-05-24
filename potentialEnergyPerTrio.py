import math


def potentialEnergyPerTrio(lengths, Rc=(50 * math.sqrt(10) / 27)):
    """
    The (simplified) potential energy based on the lengths of the sides of a triangle (a, b and c).
    
    >>> potentialEnergyPerTrio([20, 20, 20])
    -8.628094085496563e-07
    
    >>> potentialEnergyPerTrio([0.1, 0.6, 1])
    1383087510.7362177
    
    >>> potentialEnergyPerTrio([0.01, 0.006, 0.001])
    1.3830891814439465e+25
    
    >>> potentialEnergyPerTrio([0.7211102550927979, 0.36055512754639896, 0.8062257748298549])
    47801.621030097835
    
    >>> potentialEnergyPerTrio([1, 1, 1])
    -13.83088344325057
    """
    a = lengths[0]
    b = lengths[1]
    c = lengths[2]
    
    #s = (a + b + c) / 2
    #area2Triangle = s * (s - a) * (s - b) * (s - c)
    
    longRangePotential = -(((a / Rc) + (b / Rc) + (c / Rc))**-6)
    shortRangePotential = ((a / Rc)**-8 + (b / Rc)**-8 + (c / Rc)**-8) / 100000
    
    return shortRangePotential + longRangePotential


if __name__ == "__main__":
    import doctest
    doctest.testmod()