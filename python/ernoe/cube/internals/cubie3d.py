"""This module contains the class for a Rubik's Cube cubie, the
fundamental building block of a Rubik's Cube.
"""

# Use the matrix namespace.
import numpy.matlib as npm


class Cubie3D(object):
    """Class for the cubie of a Rubik's cube, in three dimensions.
    
    This class is initialised with a home postion vector, which is a
    numpy column vector. This read only property `home` can be used
    to identify a cubie as it should be unique to each cubie.
    
    As any three dimensional rigid body, the state of a cubie also
    includes it's orientation which is a read only 3x3 numpy array
    initialised to the identity matrix.
    """

    def __init__(self, home):
        """Initialise home and current pose matrix."""
        self._pose = npm.identity(4, dtype=int)
        self._pose[0:3, 3] = home[:, npm.newaxis]
        self._home = self._pose

    @property
    def pose(self):
        """Returns the current orientation of the cubie."""
        return self._pose
    
    @property
    def home(self):
        """Returns the home postion of the cubie."""
        return self._home
        
    def reorient(self, transform):
        """Multiplies cubie's current pose matrix by transform."""
        self._pose = transform @ self._pose
        
    def __eq__(self, other):
        return (
                np.all(self.pose == other.pose)
                and np.all(self.home == other.home)
            )
