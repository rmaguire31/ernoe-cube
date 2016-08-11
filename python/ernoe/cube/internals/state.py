"""This module contains the class representing the matrix state and
classes to access it.
"""

# Use the matrix namespace.
from numpy import matlib
from itertools import product
from collections.abc import Set, Hashable


class StateMatrix(matlib.matrix):
    """StateMatrix(int(m), int(n)) -> StateMatrix(S)
    """
    
    def __new__(cls, m, n):
        """
        """
        
        if not all((
                isinstance(m, int),
                isinstance(n, int),
            )):
            raise ValueError
        
        data = matlib.hstack([
            matlib.vstack((
                matlib.hstack((matlib.identity(n, dtype=int), matlib.matrix(p, dtype=int).T)),
                matlib.hstack((matlib.matrix(p, dtype=int), matlib.ones(1))),
            ))
            for p in product(range(m), repeat=n)
        ])
        return super().__new__(cls, data, dtype=int).view(cls)
        
    def __init__(self, m, n):
        """
        """
        self.ndshape = (m,)*n + (n+1,)*2
        
    def __getitem__(self, index):
        """
        """
        nd_data = self.view(matlib.ndarray).T.reshape(self.ndshape)
        snd_data = nd_data[index]
        s_data = snd_data.reshape(-1, self.shape[0]).T.view(matlib.matrix)
        
        return s_data
     

def move_mask(m, n, a, b, w):
    """Move mask constructor.
    """
    
    # Sanity check.
    if not (
            and isinstance(m, int)
            and isinstance(n, int)
            and isinstance(a, int)
            and isinstance(b, int)
            and isinstance(w, int)
            and a < n
            and b < n
            and a != b
            and abs(w) <= m // 2
        ):
        raise ValueError

    # All indicies.
    X = range(m)
    
    # Indicies in the slice.
    S = X[:w] if w > 0 else X[w:]
    
    # Only the dimensions parallel with the rotation plane include all
    # indices, all other dimensions include the indicies in the slice.
    fmt = [S]*n
    fmt[a] = X
    fmt[b] = X
    
    # Take the cartesian product of the range of indicies in each
    # dimension.
    return Mask(product(*fmt))
    

class Mask(Set, Hashable):
    """Class for indexing and masking StateMatrix instances.
    
    Supports set operations for construction of new masks.
    """
       
    __hash__ = Set._hash()
        
    def __init__(cls, iterable):
        """
        """
        
        self._data = tuple(sorted({tuple(t) for t in iterable}))
        self._idx = tuple([tuple(t) for t in matlib.array(self._data).T]

    @property
    def idx(self):
        """Transposed tuple of positions used for indexing ndarrays.
        """
        return self._idx
        
    def __contains__(self, value):
        return value in self._data
        
    def __iter__(self):
        return iter(self._data)
        
    def __len__(self):
        return len(self._data)
