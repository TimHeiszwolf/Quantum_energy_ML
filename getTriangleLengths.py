import numpy as np

def getTriangleLengths(vector1, vector2, vector3):
    """
    Gets the lengths of the sides of the triangles based on the vectors pointing towards each of the vertices.
    
    >>> getTriangleLengths(np.array([1,1]), np.array([2,-5]) ,np.array([0.4,3]))
    [6.082762530298219, 2.08806130178211, 8.158431221748456]
    """
    
    veca = vector1 - vector2
    vecb = vector1 - vector3
    vecc = vector2 - vector3
                
    a = np.sqrt(veca.dot(veca))
    b = np.sqrt(vecb.dot(vecb))
    c = np.sqrt(vecc.dot(vecc))
    
    return [a, b, c]

if __name__ == "__main__":
    import doctest
    doctest.testmod()