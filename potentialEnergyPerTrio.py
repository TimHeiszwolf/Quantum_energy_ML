def potentialEnergyPerTrio(lengths):
    """
    The (simplified) potential energy based on the lengths of the sides of a triangle (a, b and c).
    
    >>> potentialEnergyPerTrio([1, 1, 1])
    80.9375
    
    >>> potentialEnergyPerTrio([0.1, 0.6, 1])
    115989177.09076478
    
    >>> potentialEnergyPerTrio([0.01, 0.006, 0.001])
    1.1598917709076485e+24
    
    >>> potentialEnergyPerTrio([0.7211102550927979, 0.36055512754639896, 0.8062257748298549])
    15477.243602126406
    """
    
    a = lengths[0]
    b = lengths[1]
    c = lengths[2]
    
    s = (a + b + c) / 2
    area2Triangle = s * (s - a) * (s - b) * (s - c)
    
    longRangePotential = (a**-8 + b**-8 + c**-8)#(a**-2 + b**-2 + c**-2)**4#(a**-4 + b**-4 + c**-4)**2
    shortRangePotential = - 1000 * area2Triangle / (a**12 + b**12 + c**12)# - * area2Triangle / (a**12 + b**12 + c**12)
    
    return shortRangePotential + longRangePotential

if __name__ == "__main__":
    import doctest
    doctest.testmod()