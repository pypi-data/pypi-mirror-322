from sympy          import Function, Matrix, Array, simplify, derive_by_array, tensorcontraction, tensorproduct, permutedims, sqrt, diff, Add, O, Order, latex, Rational
from sympy.diffgeom import TensorProduct, metric_to_Christoffel_1st, metric_to_Christoffel_2nd, metric_to_Riemann_components, metric_to_Ricci_components


def swap_indices(arr, i, j):
    """
    Swap two indices of an Array.
    """
    # Get the ordering in the array
    order = list(range(len(arr.shape)))
    # Swap the indices
    order[i], order[j] = order[j], order[i]
    # Perform the permutation on the array
    arr = permutedims(arr, order)
    # Return the result
    return arr


class Geometry:
    """
    Set of helper functions to conveniently work in a given geometry.
    """

    def __init__(self, coordsys, metric):
        """
        Constructor for a Geometry with a given (sympy.diffgeom) coordinate system and (sympy.Array) metric.
        """
        # Define attributes
        self.coordsys = coordsys   # Coordinate system
        self.metric   = metric     # Metric tensor, as a matrix
        # Check if the metric is symmetric
        assert Matrix(self.metric) == Matrix(self.metric).T, "Metric must be symmetric!"
        # Check if the dimensions of the metric match the coordinate system
        assert self.metric.shape == (self.dim, self.dim), "Metric must have the same dimensions as the coordinate system!"


    @property
    def coordsys(self):
        """
        Coordinate system of the geometry.
        """
        return self._coordsys


    @coordsys.setter
    def coordsys(self, c):
        """
        Set the coordinate system of the geometry.
        """
        # Set the coordinate system
        self._coordsys = c
        # Set all dependent properties
        self.dim           = self.coordsys.dim
        self.coords        = self.coordsys.symbols
        self.base_scalars  = self.coordsys.base_scalars()
        self.base_vectors  = self.coordsys.base_vectors()
        self.base_oneforms = self.coordsys.base_oneforms()


    @property
    def metric(self):
        """
        Metric of the geometry.
        """
        return self._metric


    @metric.setter
    def metric(self, m):
        """
        Set the metric of the geometry.
        """
        # Set the metric
        self._metric = Array(m)
        # Set all dependent properties
        # self.frame_field         = self._frame_field()
        # self.sqrt_abs_det_metric = self._sqrt_abs_det_metric()
        self.inv_metric          = self._inv_metric()
        self.metric_as_2_form    = self._metric_as_2_form()
        self.christoffel_1st     = self._christoffel_1st()
        self.christoffel_2nd     = self._christoffel_2nd()
        self.riemann             = self._riemann()
        self.ricci               = self._ricci()
        self.ricci_scalar        = self._ricci_scalar()


    def frame_field(self):
        """
        Frame field (or vielbein, or in 4D vierbein or tetrad) of the geometry.
        """
        # Diagonalize the metric
        P, D = Matrix(self.metric).diagonalize()
        # Compute the square root of the eigenvalues
        sqrt_D = sqrt(D).doit().factor(deep=True)
        # Return result
        return sqrt_D * P


    def _sqrt_abs_det_metric(self):
        """
        Square root of the absolute value of the determinant of the metric tensor.
        """
        return sqrt(abs(Matrix(self.metric).det()))
        

    def _inv_metric(self):
        """
        Inverse of the metric tensor.
        """
        # Check if series expansion is needed, if so return first order inverse
        if self.metric.has(O):
            # Extract the expansion variable
            epsilon = self.metric.atoms(Order).pop().free_symbols.pop()
            # Extract the background metric
            bg = self.metric.applyfunc(lambda x: x.removeO()).subs({epsilon: 0})
            # Return the first order inverse
            return Array(Matrix(bg).inv()) - (self.metric - bg)
        else:
            return Array(Matrix(self.metric).inv())

            
    def tensor_function(self, name, rank, args=None):
        """
        A tensor function in this geometry (with all lower / covariant indices).
        """
        if rank == 0:
            if args is None: args = self.coords
            return Function(name)(*args)
        else:
            return Array([self.tensor_function(rf'{name}_{{{latex(sym)}}}', rank=rank-1, args=args) for sym in self.coords], shape=rank*(self.dim,))


    def scalar_function(self, name, args=None):
        """
        A scalar (i.e. rank 0) function in this geometry.
        """
        return self.tensor_function(name, rank=0, args=args)


    def vector_function(self, name, args=None):
        """
        A vector (i.e. rank 1) function in this geometry.
        """
        return self.tensor_function(name, rank=1, args=args)
    

    def matrix_function(self, name, args=None):
        """
        A matrix (i.e. rank 2) function in this geometry.
        """
        return self.tensor_function(name, rank=2, args=args)
    

    def coords_to_base_scalars(self, expr):
        """
        Replace coordinate symbols in the expression by base scalars.
        """
        return expr.subs([(x, y) for (x, y) in zip(self.coords, self.base_scalars)])
    

    def base_scalars_to_coords(self, expr):
        """
        Replace coordinate symbols in the expression by base scalars.
        """
        return expr.subs([(x, y) for (x, y) in zip(self.base_scalars, self.coords)])
    

    def _metric_as_2_form(self):
        """
        Returns the metric tensor as a 2-form.
        """
        # Replace coordinate symbols by base scalars in metric
        metric_bs = self.coords_to_base_scalars(self.metric)
        # Construct two-form
        m = 0
        for i, di in enumerate(self.base_oneforms):
            for j, dj in enumerate(self.base_oneforms):
                m += metric_bs[i,j] * TensorProduct(di, dj)
        # Return result
        return m
    

    def _christoffel_1st_original(self):
        """
        Christoffel symbol of the 1st kind.
        """
        return self.base_scalars_to_coords(metric_to_Christoffel_1st(self.metric_as_2_form))


    def _christoffel_1st(self):
        """
        Christoffel symbol of the 1st kind.
        """
        # Compute metric derivatives
        d_g = [diff(self.metric, coord) for coord in self.coords]
        # Get indices
        ind = list(range(self.coordsys.dim))
        # Compute Christoffel (1st) symbols
        ch1 = [[[(d_g[k][i, j] + d_g[j][i, k] - d_g[i][j, k])/2 for k in ind] for j in ind] for i in ind]
        # Return result
        return Array(ch1)


    def _christoffel_2nd_original(self):
        """
        Christoffel symbol of the 2nd kind.
        """
        return self.base_scalars_to_coords(metric_to_Christoffel_2nd(self.metric_as_2_form))


    def _christoffel_2nd(self):
        # Get indices
        ind = list(range(self.coordsys.dim))
        # Compute Christoffel (2nd) symbols
        ch2 = [[[Add(*[self.inv_metric[i, l]*self.christoffel_1st[l, j, k] for l in ind]) for k in ind] for j in ind] for i in ind]
        # Return result
        return Array(ch2)


    def _riemann_original(self):
        """
        Riemanm tensor components.
        """
        return self.base_scalars_to_coords(metric_to_Riemann_components(self.metric_as_2_form))


    def _riemann(self):
        """
        Riemann tensor components.
        """
        # Get indices
        ind = list(range(self.coordsys.dim))
        # Introduce shorthand for the Christoffel symbols
        ch2 = self.christoffel_2nd
        # Compute the derivative of the Christoffel symbols
        d_ch2 = [[[[diff(ch2[i, j, k], coord) for coord in self.coords] for k in ind] for j in ind] for i in ind]
        # Compute the two terms of the Riemann tensor
        riemann_a = [[[[d_ch2[i][j][l][k] - d_ch2[i][j][k][l] for l in ind] for k in ind] for j in ind] for i in ind]
        riemann_b = [[[[Add(*[ch2[i, a, k]*ch2[a, j, l] - ch2[i, a, l]*ch2[a, j, k] for a in ind]) for l in ind] for k in ind] for j in ind] for i in ind]
        # Return result
        return Array(riemann_a) + Array(riemann_b)


    def _ricci_original(self):
        """
        Ricci tensor components.
        """
        return self.base_scalars_to_coords(metric_to_Ricci_components(self.metric_as_2_form))


    def _ricci(self):
        """
        Ricci tensor components.
        """
        # Get indices
        ind = list(range(self.coordsys.dim))
        # Compute the Ricci tensor
        ricci = [[Add(*[self.riemann[k, i, k, j] for k in ind]) for j in ind] for i in ind]
        # Return result
        return Array(ricci)


    def _ricci_scalar(self):
        """
        Ricci scalar.
        """
        return self.contract_indices(self.ricci, 0, 1)


    def einstein(self):
        """
        Einstein tensor.
        """
        return self.ricci - Rational(1, 2) * self.metric * self.ricci_scalar


    def kretschmann_scalar(self):
        """
        Kretschmann scalar.
        """
        # Get indices
        ind = list(range(self.coordsys.dim))
        # Raise all indeces of the Riemann tensor (first one is already raised)
        riemann_upp = self.raise_indices(self.riemann, 1, 2, 3)
        riemann_low = self.lower_indices(self.riemann, 0)
        # Compute the Kretchmann scalar
        kretchmann = Add(*[riemann_low[i, j, k, l] * riemann_upp[i, j, k, l] for l in ind for k in ind for j in ind for i in ind])
        # Return result
        return kretchmann


    def gradient(self, func):
        """
        Gradient of a function, i.e. the ordinary derivative with respect to all coordinates in this geometry.
        """
        return derive_by_array(func, self.coords)


    def covariant_diff(self, func):
        """
        Covariant derivative of a function (with only lower indices) in this geometry.
        """
        # Add the (ordinary) gradient
        d = self.gradient(func)
        # Check if the function has indices (and thus is not scalar)
        if isinstance(func, Array):
            # Add the contractions with the Christoffel symbols
            for i in range(len(func.shape)):
                # Contract with the Christoffel symbol
                d_i = tensorcontraction(tensorproduct(self.christoffel_2nd, func), (0, 3+i))
                # Ensure that the ordering of the indices is the same
                d_i = swap_indices(d_i, 1, 3+i-2)
                # Add the result
                d -= d_i
        # Return result
        return d


    def raise_index(self, tensor, index=0):
        """
        Raise the index of a tensor.
        """
        # Contract the index with the inverse metric, ensuring that the index ordering remains the same
        return tensorcontraction(swap_indices(tensorproduct(self.inv_metric, tensor), 1, 2+index), (0, 1))


    def raise_indices(self, tensor, *indices):
        """
        Raise the indices of a tensor.
        """
        for i in indices:
            tensor = self.raise_index(tensor, i)
        return tensor


    def lower_index(self, tensor, index=0):
        """
        Lower the index of a tensor.
        """
        # Contract the index with the metric, ensuring that the index ordering remains the same
        return tensorcontraction(swap_indices(tensorproduct(self.metric, tensor), 1, 2+index), (0, 1))


    def lower_indices(self, tensor, *indices):
        """
        Lower the indices of a tensor.
        """
        for i in indices:
            tensor = self.lower_index(tensor, i)
        return tensor


    def contract_indices(self, tensor, i, j):
        """
        Contract two indices of a tensor.
        (Assuming all indices are lower indices.)
        """
        return tensorcontraction(self.raise_index(tensor, i), (i, j))


    def divergence(self, func):
        """
        Divergence of a tensor function w.r.t. the first index. 
        """
        return self.contract_indices(self.covariant_diff(func), 0, 1)


    def laplacian(self, func):
        """
        Laplacian of a (tensor) function.
        """
        return self.divergence(self.covariant_diff(func))
    

    def get_metric_in(self, new_coordsys):
        """
        Get the metric tensor in a new coordinate system.
        """
        # Compute the Jacobian of the new coordinate system w.r.t. the original one
        jac = new_coordsys.jacobian(self.coordsys)
        # Compute the new metric tensor
        new_metric = Array(jac.T * Matrix(self.metric) * jac)
        # Return result
        return simplify(new_metric)


    def make_orthonormal(self, tensor):
        """
        Transform a tensor to an orthonormal basis.
        """
        # Compute frame field
        frame_field = self.frame_field()
        # Contract every index with the frame field
        for i in range(len(tensor.shape)):
            tensor = swap_indices(tensorcontraction(tensorproduct(frame_field, tensor), (1, 2+i)), 0, i)
        # Return result
        return simplify(tensor)
   