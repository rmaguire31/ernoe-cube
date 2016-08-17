"""This module contains the class for the 3x3x3 magic cube, allso known
as the Rubik's Magic Cube.
"""

from ernoe.cube.internals.base import BaseCube
from ernoe.cube.internals.state import Mask
from itertools import permutations, product


def cube(m, n):
    """Constructor for cube instances with some optimised stuff."""
    
    cls = type(
            'Cube%d_%d' % (m, n)
            (BaseCube,),
            {},
        )
      
    if n == 3:
        # We can optimise 3D cubes by only caring about the cubies on
        # surface of each face.  
        X = range(m)
        F = (0, m-1)
        
        global_mask = Mask({
                t for p in permutations((X, X, F)) for t in product(*p)
            })
        
        # For cubes with odd side length we can ignore the centre cubies.
        if m % 2:
            C = (m//2,)
            
            ignore = Mask({
                    t for p in permutations((C, C, F)) for t in product(*p)
                })
            global_mask = global_mask - ignore
        
        # Override BaseCube global_mask property.
        cls.__global_mask = global_mask
        cls.global_mask = property(lambda self: self.__global_mask)
        
    return cls(m, n)
    
