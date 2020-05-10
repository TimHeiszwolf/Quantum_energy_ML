import math


def potentialEnergyPerTrio(lengths):
    """
    The (simplified) potential energy based on the lengths of the sides of a triangle (a, b and c).
    
    >>> potentialEnergyPerTrio([1, 1, 1])
    -0.013417421124828532
    
    >>> potentialEnergyPerTrio([0.1, 0.6, 1])
    9999.59176181373
    
    >>> potentialEnergyPerTrio([0.01, 0.006, 0.001])
    1.0000006012312612e+20
    
    >>> potentialEnergyPerTrio([0.7211102550927979, 0.36055512754639896, 0.8062257748298549])
    0.13118489703592645
    """
    a = lengths[0]
    b = lengths[1]
    c = lengths[2]
    
    #s = (a + b + c) / 2
    #area2Triangle = s * (s - a) * (s - b) * (s - c)
    
    longRangePotential = - 10 * ((a + b + c)**-6)#- 500 * math.exp(-(a + b + c)*2)#-10 *(a + b + c)**-8
    shortRangePotential = (a**-8 + b**-8 + c**-8) / 10000#(a**-6+b**-6+c**-6)/1000#(a + b + c)**-10
    
    return shortRangePotential + longRangePotential


if __name__ == "__main__":
    import doctest
    doctest.testmod()