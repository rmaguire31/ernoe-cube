"""This module contains the base class for a Rubik's Cube in three
dimensions.
"""

# Use the matrix namespace.
from ernoe.cube.internals import state
from ernoe.cube.internals.transform import RotationC
from itertools import product


class BaseCube(object):
    """Base class and function for the general rubik's cube.
    """

    def __init__(self, m, n):
        """Initialised state and moveset of cube.
        """
        
        # Global mask.
        self.__global_mask = state.Mask(product(range(m), repeat=n))
        
        # Initialise cube state.
        self._state = state.StateMatrix(m, n)
        
        # Generate rotation matrices.
        c = np.matrix([(m-1)/2]*n)
        R = np.empty((n, n), dtype=RotationC)
        
        for a, b in product(range(n), range(n)):
            R[a,b] = RotationC(n, a, b, c)
            
        # Generate moves.
        self._move = {}
        for a, b, w in product(range(n), range(n), range(1, m//2 + 1)):
            self.__move[(a, b, w)] = (
                    R[a,b],
                    state.move_mask(m, n, a, b, w) & self.global_mask,
                )
           
    @property
    def _move(self):
        """
        """
        return self.__move
            
    @property
    def global_mask(self):
        """
        """
        return self.__global_mask

    def execute_seq(self, move_keys):
        """Iterates over a sequence of moves corresponding to the keys
        in move_keys.
              
        Moves must be an ordered iterable sequence of strings returned 
        by cube instance's move_keys method.
        """
        
        for move_key in move_keys:
            
            # Get transformation matrix and mask for this move.
            R, mask = self.move[move_key]
            
            # Reorient cubies.
            tmp_state = R @ self._state[mask.idx].copy()
            
            # Permute cubies.
            step = tmp_state.shape[0]
            for start in range(0, tmp_state.shape[1], tmp_state.shape[0]):
            
                # State is a sequence of cubie pose matrix.
                cubie = tmp_state[:, start:start+step]
                
                # Position of cubie is stored in pose matrix.
                pos = tuple(cubie.A[:-1, -1])
                
                # Assign pose matrix to its new position.
                self._state[pos][...] = cubie
            
