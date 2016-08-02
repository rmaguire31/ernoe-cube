"""This module contains the class for a Rubik's Cube cubie, the
fundamental building block of a Rubik's Cube.
"""

# Use the matrix namespace.
import numpy.matlib as npm


class CubieMxxN(object):
    """Class for the cubie of a Rubik's cube, in N dimensions.
    
    This class is initialised with a home postion vector, which is a
    numpy column vector. This read only property `home` can be used
    to identify a cubie as it should be unique to each cubie.
    
    As any N dimensional rigid body, the state of a cubie also includes
    it's position and orientation which is a read only N+1xN+1 numpy
    array initialised to identity orientation and home position.
    """

    def __init__(self, home):
        """Initialise home and current pose matrix."""
        assert(home.ndims == 1)
        self._pose = npm.identity(home.size + 1, dtype=int)
        self._pose[0:-2, -1] = home[:, npm.newaxis]
        self._home = self._pose

    @property
    def pose(self):
        """Returns the current pose matrix of the cubie."""
        return self._pose
    
    @property
    def home(self):
        """Returns the home pose matrix of the cubie."""
        return self._home
        
    def reorient(self, transform):
        """Multiplies cubie's current pose matrix by transform."""
        self._pose = transform @ self._pose
        
    def __eq__(self, other):
        eq = np.all(self.pose == other.pose) and np.all(self.home == other.home)
        return eq
