"""This module contains the classes for matrix transformations used to
transform cubes.
"""

# Use the matrix namespace.
from numpy import matlib
    

class RotationO(matlib.matrix):
    """RotationO(int(n), int(a), int(b)) -> matrix(R)
    """

    def __new__(cls, n, a, b):
        """
        """
        
        if not (
                isinstance(n, int)
                and isinstance(a, int)
                and isinstance(b, int)
                and a < n
                and b < n
            ):
            raise ValueError
            
        R = matlib.identity(n+1, dtype=int)
        R[a, a] = 0
        R[b, b] = 0
        R[a, b] = -1
        R[b, a] = 1
        return super().__new__(cls, R)
        
        
class Translation(matlib.matrix)
    """Translation(ndarray(c)) -> matrix(T)
    """

    def __new__(cls, c)
        """
        """
        
        c = c.view(matlib.matrix).reshape(1, -1)
            
        T = matlib.vstack((
            matlib.hstack((matlib.identity(c.size), c)),
            matlib.hstack((matlib.zeros(c.size), matlib.ones(1))),
        ))
        return super().__new__(cls, T)
        
        
class RotationC(matlib.matrix):
    """RotationC(int(n), int(a), int(b), ndarray(c)) -> matrix(Rc)
    """
    
    def __new__(cls, a, b, c, dtype=int)
        """
        """
        
        T = Translation(c)
        R = RotationO(c.size, a, b)
        if T.shape != R.shape:
            raise ValueError
        
        Rc = T @ R @ T.I
        return super().__new__(cls, Rc, dtype=dtype)
        
