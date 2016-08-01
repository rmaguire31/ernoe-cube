"""This module contains the verification code for the Cube3D base class.
"""
import re
import logging
import numpy as np

from ernoe.cube.internals.cube3d import Cube3D


class InvalidMoveKeyErr(Exception):
    """Raised for Cube3D class instance with an incomplete moveset."""
    pass
    
    
class InvalidInverseErr(Exception):
    """Raised when executing (F, F') does not result in an identity
    operation.
    """
    pass


class SingleMoveGroupErr(Exception):
    """Raised when executing (F, F, F, F) does not result in an
    identity operation.
    """
    pass


def verif(ranks=range(2, 10)):
    """Tests Cube3D base class.
    """
    
    # Sweep all ranks.
    for rank in ranks:
        
        
        c = Cube3D(rank)
        
        move_keys = sorted(c.move_keys)
        
        logging.debug("Rank %d: Moveset is %s", rank, move_keys)
        
        # Check each move has a working inverse.
        for move_key in move_keys:
            
            # Save initial state.
            init_state = c.state.copy()
            
            # Determine inverse move.
            m = re.match(
                    r"(?P<slice_num>[1-9]\d*)(?P<face>[LFDRBU])w(?P<rot_num>[1-3])",
                    move_key,
                )
            try:
                parts = m.groupdict()
            except TypeError:
                raise InvalidMoveKeyErr
            move_key_i = "%s%sw%d" % (
                    parts['slice_num'],
                    parts['face'],
                    4-int(parts['rot_num']),
                )
                
            logging.debug(
                    "Rank %d: Inverse of (%s) is (%s)",
                    rank, move_key, move_key_i,
                )
                
            # Execute move followed by inverse.
            try:
                c.execute_seq((move_key, move_key_i))
            except KeyError:
                raise InvalidMoveKeyErr
                
            if np.any(c.state != init_state):
                raise InvalidInverseErr
                
            logging.info(
                    "Rank %d: Validated move and inverse (%s, %s)",
                    rank, move_key, move_key_i,
                )
                
            # Check move obeys obeys fourfold symmetry.
            c.execute_seq((move_key,) * 4)
            
            if np.any(c.state != init_state):
                raise SingleMoveGroupErr
      
            logging.info(
                    "Rank %d: Validated cyclic group for (%s)",
                    rank, move_key,
                )
                
        logging.info("Rank %d: Validated moveset.", rank)

if __name__ == "__main__":
    logging.addLevelName(logging.INFO,     '>')
    logging.addLevelName(logging.DEBUG,    '?')
    logging.addLevelName(logging.WARNING,  '!')
    logging.addLevelName(logging.ERROR,    '@')
    logging.addLevelName(logging.CRITICAL, '@@@')
    logging.basicConfig(
            format="[%(asctime)s][%(levelname)s] %(message)s",
            level=logging.INFO,
        )
    verif()
    
