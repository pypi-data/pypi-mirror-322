from sympy             import symbols, sin, diag, eye
from sympy.diffgeom    import Manifold, Patch, CoordSystem
from sympy.diffgeom.rn import R2_r, R2_p, R3_r, R3_c, R3_s

from .geometry import Geometry


list_of_example_geometries = [
    'Euclidean2dRec',
    'Euclidean2dPol',
    'Euclidean3dRec',
    'Euclidean3dCyl',
    'Euclidean3dSph',
    'Minkowski2dRec',
    'Minkowski4dRec',
    'Schwarzschild',
]


class Euclidean2dRec(Geometry):
    """
    Euclidean 2D geometry in rectangular (cartesian) coordinates.
    """
    def __init__(self):
        super().__init__(R2_r, eye(2))


class Euclidean2dPol(Geometry):
    """
    Euclidean 2D geometry in polar coordinates.
    """
    def __init__(self):
        super().__init__(R2_p, Euclidean2dRec().get_metric_in(R2_p))

class Euclidean3dRec(Geometry):
    """
    Euclidean 3D geometry in rectangular (cartesian) coordinates.
    """
    def __init__(self):
        super().__init__(R3_r, eye(3))


class Euclidean3dCyl(Geometry):
    """
    Euclidean 3D geometry in cylindrical coordinates.
    """
    def __init__(self):
        super().__init__(R3_c, Euclidean3dRec().get_metric_in(R3_c))


class Euclidean3dSph(Geometry):
    """
    Euclidean 3D geometry in spherical coordinates.
    """
    def __init__(self):
        super().__init__(R3_s, Euclidean3dRec().get_metric_in(R3_s))


class Minkowski2dRec(Geometry):
    """
    Minkowski 2D geometry in rectangular (cartesian) coordinates.
    """
    def __init__(self):
        # Define the relevant coordinate system
        min_2_rec = CoordSystem('Min_2_rec', Patch('P', Manifold('M', 2)), symbols('t x', real=True))
        # Define the metric tensor
        minkowski_2_metric = diag(-1, 1)
        # Create the Minkowski 2D geometry
        super().__init__(min_2_rec, minkowski_2_metric)


class Minkowski4dRec(Geometry):
    """
    Minkowski 4D geometry in rectangular (cartesian) coordinates.
    """
    def __init__(self):
        # Define the relevant coordinate system
        min_4_rec = CoordSystem('Min_4_rec', Patch('P', Manifold('M', 4)), symbols('t x y z', real=True))
        # Define the metric tensor
        minkowski_4_metric = diag(-1, 1, 1, 1)
        # Create the Minkowski 4D geometry
        super().__init__(min_4_rec, minkowski_4_metric)


class Schwarzschild(Geometry):
    """
    Schwarzschild geometry.
    """
    def __init__(self):
        # Define the relevant coordinate system
        r = symbols('r', positive=True)
        t, theta, phi = symbols('t theta phi', real=True)
        schwarzschild_coords = CoordSystem('Schwarzschild', Patch('P', Manifold('M', 4)), (t, r, theta, phi))
        # Define the metric tensor
        self.M = M = symbols('M', positive=True)          # Shwarzschild mass
        t, r, theta, phi = schwarzschild_coords.symbols   # Note that we must use the symbols from the coordinate system!
        schwarzschild_metric = diag(-(1-2*M/r), 1/(1-2*M/r), r**2, (r*sin(theta))**2)
        # Create the Schwarzschold geometry
        super().__init__(schwarzschild_coords, schwarzschild_metric)