"""This module contains the base class for a Rubik's Cube in three
dimensions.
"""

# Use the matrix namespace.
import numpy as np
import numpy.matlib as npm
from ernoe.cube.internals.cubie3d import Cubie3D

# Transformation matrices, centred at [0,0,0]
_RX = np.matrix(
        [[1, 0,  0, 0],
         [0, 0, -1, 0],
         [0, 1,  0, 0],
         [0, 0,  0, 1]],
        dtype=int
    )
_RY = np.matrix(
        [[ 0, 0, 1, 0],
         [ 0, 1, 0, 0],
         [-1, 0, 0, 0],
         [ 0, 0, 0, 1]],
        dtype=int
    )
_RZ = np.matrix(
        [[0, -1, 0, 0],
         [1,  0, 0, 0],
         [0,  0, 1, 0],
         [0,  0, 0, 1]],
        dtype=int
    )

class Cube3D(object):
    """Base class for the general Rubik's cube, in three dimensions.
    """

    def __init__(self, rank):
        """Initialised state and moveset of cube.
        """
        
        # First build elementary transformation matrices.
        t  = npm.identity(4)
        ti = npm.identity(4)
        t[0:3, 3]  = (rank-1) / 2
        ti[0:3, 3] = -(rank-1) / 2
        
        rx  = (t @ _RX  @ ti).astype(int)
        ry  = (t @ _RY  @ ti).astype(int)
        rz  = (t @ _RZ  @ ti).astype(int)
        
        self._move = {}
        self._move_alias = {}
        
        combinations = [
                (slice_num, face, rot_num)
                for slice_num in range(0, rank // 2)
                for face in ('B', 'D', 'F', 'L', 'R', 'U')
                for rot_num in range(1, 4)
            ]
        for slice_num, face, rot_num in combinations:
            
            # Construct move key.
            key = '%d%sw%d' % (slice_num+1, face, rot_num)
            
            # Construct and record aliases for move key.
            rot_aliases = [str(rot_num)]
            if rot_num == 1:
                rot_aliases.append('')
            elif rot_num == 3:
                rot_aliases.append('\'')
                
            slice_aliases = ['%d%sw' % (slice_num+1, face)]
            if slice_num == 0:
                slice_aliases.append(face)
            elif slice_num == 1:
                slice_aliases.append('%sw' % (face))
             
            aliases = [
                    '%s%s' % (slice_alias, rot_alias)
                    for slice_alias in slice_aliases
                    for rot_alias in rot_aliases
                ]
            for alias in aliases:
                self._move_alias[alias] = key
            
                    
            # Construct mask and transform matrix for move.
            if face == 'L':
                mask = np.mgrid[slice_num:slice_num+1, 0:rank, 0:rank]
                mask = mask.reshape(3, -1).transpose()
                transform = rx**rot_num
            elif face == 'F':
                mask = np.mgrid[0:rank, slice_num:slice_num+1, 0:rank]
                mask = mask.reshape(3, -1).transpose()
                transform = ry**rot_num
            elif face == 'D':
                mask = np.mgrid[0:rank, 0:rank, slice_num:slice_num+1]
                mask = mask.reshape(3, -1).transpose()
                transform = rz**rot_num
            elif face == 'R':
                mask = np.mgrid[rank-slice_num-1:rank-slice_num, 0:rank, 0:rank]
                mask = mask.reshape(3, -1).transpose()
                transform = rx.I**rot_num
            elif face == 'B':
                mask = np.mgrid[0:rank, rank-slice_num-1:rank-slice_num, 0:rank]
                mask = mask.reshape(3, -1).transpose()
                transform = ry.I**rot_num
            elif face == 'U':
                mask = np.mgrid[0:rank, 0:rank, rank-slice_num-1:rank-slice_num]
                mask = mask.reshape(3, -1).transpose()
                transform = rz.I**rot_num
                
            # Save move.
            self._move[key] = (mask, transform)
            
        # Initialise cube state.
        self._all = np.mgrid[0:rank, 0:rank, 0:rank].reshape(3, -1).transpose()
        self._state = np.empty((rank, rank, rank), dtype=Cubie3D)
        for pos in self._all:
            self._state[tuple(pos)] = Cubie3D(pos)
            
        # Initialise cache
        self._moves_cache = {}
        
    @property
    def move_keys(self, aliases=False):
        """Returns read only list of valid move_keys for cls.execute.
        """
        if aliases:
            return self._move_alias.keys()
        else:
            return self._move.keys()
        
    @property
    def state(self):
        """Returns read only state of cube.
        """
        return self._state

    def cache_seq(self, move_keys):
        """Optimises and caches the sequence of moves in move_keys.
           
        Moves must be an ordered iterable sequence of strings returned 
        by cube instance's move_keys method.
        """
        
        if tuple(move_keys) in self._moves_cache.keys():
            return
        
        # Save state and execute move sequence.
        state = self._state.copy()
        self.execute_seq(move_keys)
        
        moves_dict = {}
        for pos in self._all:
                        
            # Find where the cubie has moved to.
            home = state[tuple(pos)].home
            for new_pos in self._all:
                if np.all(self._state[tuple(new_pos)].home == home):
                    break
           
            # Skip identity transformations.
            if np.all(
                    self._state[tuple(new_pos)].pose == state[tuple(pos)].pose):
                continue
            
            # Find the linear transformation which mapped the pose of
            # the cubie to the new pose.
            transform = self._state[new_pos].pose @ state[pos].pose.I
            
            # Check if any other cubies use this transformation.
            if str(transform) in moves_dict.keys():
                mask, _ = moves_dict[str(transform)]
                mask = np.concatenate((mask, pos[np.newaxis, :]), axis=0)
            else:
                mask = pos[np.newaxis, :]
                
            # Save mask for this transformation.
            moves_dict[str(transform)] = (mask, transform)
                
        # Revert state of cube.
        self._state = state
        
        # Add moves to cache.
        self._moves_cache[tuple(move_keys)] = moves_dict.values()
            

    def execute_seq(self, move_keys):
        """Iterates over a sequence of moves corresponding to the keys
        in move_keys.
              
        Moves must be an ordered iterable sequence of strings returned 
        by cube instance's move_keys method.
        """
        
        try:
            moves = self._moves_cache[tuple(move_keys)]
        except KeyError:
            moves = [self._move[self._move_alias[key]] for key in move_keys]
        
        new_pos = np.empty(3, dtype=int)
        for mask, transform in moves:
            
            # This is not a linear transformation, so we need to operate
            # on a temporary copy.
            state = self._state.copy()
            
            for pos in mask:
                
                # Transform pose of cubie by rotating about centre of
                # cube.
                state[tuple(pos)].reorient(transform)
                
                # Extract position vector from pose of cubie and
                # reposition it in the cube state.
                new_pos[:] = state[tuple(pos)].pose[0:3, 3].reshape(-1)
                self._state[tuple(new_pos)] = state[tuple(pos)]
            
