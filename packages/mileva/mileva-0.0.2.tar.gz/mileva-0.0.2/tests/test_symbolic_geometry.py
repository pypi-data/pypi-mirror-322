from sympy import simplify, diff, sin, tensorproduct, tensorcontraction, Array, eye, flatten, Q, zeros

import mileva.geometry.examples as examples


def covariant_diff_metric(geo):
    """
    The covariant derivative of the inverse metric should be zero.
    """
    # Compute the covariant derivative of the inverse metric
    result = geo.covariant_diff(geo.metric)
    # Check that all elements are zero
    for elem in flatten(result):
        assert elem.expand().rewrite(sin).simplify() == 0


def raising_or_lowering_metric_indices(geo):
    """
    Raising or lowering the indices of the metric should give the identity.
    """
    # Check that raising and lowering the indices of the metric gives the identity
    assert geo.raise_index(geo.metric,     0).simplify() == Array(eye(geo.dim))
    assert geo.raise_index(geo.metric,     1).simplify() == Array(eye(geo.dim))
    assert geo.lower_index(geo.inv_metric, 0).simplify() == Array(eye(geo.dim))
    assert geo.lower_index(geo.inv_metric, 1).simplify() == Array(eye(geo.dim))


def raising_and_lowering_same_index(geo):
    """
    Raising and lowering the same index should give the same tensor again.
    """
    # Define a rank
    rank = 3
    # Define a random tensor
    M = geo.tensor_function('M', rank=rank)
    # Check that raising and lowering the same index gives the same tensor again
    for r in range(rank):
        assert geo.lower_index(geo.raise_index(M, r), r).simplify() == M
        assert geo.raise_index(geo.lower_index(M, r), r).simplify() == M


def orthonormal_indices(geo):
    """
    Orthonormal indices, when cont
    """
    # Define a vector
    V = geo.vector_function('V')
    # Make orthonormal
    o_V = geo.make_orthonormal(V)
    # Check if norm is Euclidean
    o_norm = tensorcontraction(tensorproduct(geo.raise_index(o_V, 0), o_V), (0, 1))
    e_norm = tensorcontraction(tensorproduct(                  V,       V), (0, 1))
    assert o_norm == e_norm


def christoffel_1st(geo):
    """
    Test if the new implementation of the Christoffel symbols (1st) is the same as the old.
    """
    ch1_org = geo._christoffel_1st_original()   # Using sympy
    ch1_new = geo._christoffel_1st()            # Own implementation
    assert ch1_org == ch1_new


def christoffel_2nd(geo):
    """
    Test if the new implementation of the Christoffel symbols (2nd) is the same as the old.
    """
    ch2_org = geo._christoffel_2nd_original()   # Using sympy
    ch2_new = geo._christoffel_2nd()            # Own implementation
    assert ch2_org == ch2_new


def riemann(geo):
    """
    Test if the new implementation of the Riemann tensor is the same as the old.
    """
    rmn_org = geo._riemann_original()   # Using sympy
    rmn_new = geo._riemann()            # Own implementation
    assert rmn_org == rmn_new


def ricci(geo):
    """
    Test if the new implementation of the Ricci tensor is the same as the old.
    """
    ric_org = geo._ricci_original()   # Using sympy
    ric_new = geo._ricci()            # Own implementation
    assert ric_org == ric_new


def test_all_example_geometries():
    """
    Run all test functions on all example geometries.
    """
    for name in examples.list_of_example_geometries:
        # Print the geometry that is being tested
        print('Testing geometry:', name)
        # Get the example geometry
        geo = getattr(examples, name)()
        # Run all test functions on this geometry
        covariant_diff_metric             (geo)
        raising_or_lowering_metric_indices(geo)
        raising_and_lowering_same_index   (geo)
        christoffel_1st                   (geo)
        christoffel_2nd                   (geo)
        riemann                           (geo)
        ricci                             (geo)


def test_euclidean_2_pol_div():
    """
    Check if the divergence of a vector field in 2D polar coordinates is correct.
    (By comparing with text book expression.)
    """
    # Define the geometry
    geo = examples.Euclidean2dPol()
    # Define a vector function
    F = geo.vector_function('F')
    # Define the divergence of vector F (in orthonormal polar coordinate basis!)
    rho, theta = geo.coords
    div_F      = 1/rho * diff(rho*F[0], rho) + 1/rho * diff(F[1], theta)
    # Check the divergence of F
    assert simplify(div_F - geo.divergence(geo.make_orthonormal(F))) == 0, "euclidean_2_pol divergence is wrong!"


def test_euclidean_3_sph_div():
    """
    Check if the divergence of a vector field in 3D spherical coordinates is correct.
    (By comparing with text book expression.)
    """
    # Define the geometry
    geo = examples.Euclidean3dSph()
    # Define a vector function
    F = geo.vector_function('F')
    # Define the divergence of vector F (in orthonormal polar coordinate basis!)
    r, theta, phi = geo.coords
    div_F         = 1/r**2 * diff(r**2 * F[0], r) + 1/(r*sin(theta)) * diff(sin(theta) * F[1], theta) + 1/(r*sin(theta)) * diff(F[2], phi)
    # Check the divergence of F
    assert simplify(div_F - geo.divergence(geo.make_orthonormal(F)).refine(Q.positive(sin(theta)))) == 0, "euclidean_3_sph divergence is wrong!"


def test_euclidean_3_cyl_lap():
    """
    Check if the Laplacian of a scalar field in 3D cylindrical coordinates is correct.
    (By comparing with text book expression.)
    """
    # Define the geometry
    geo = examples.Euclidean3dCyl()
    # Define a vector function
    f = geo.scalar_function('f')
    # Define the Laplacian of scalar f
    rho, psi, z = geo.coords
    lap_f       = 1/rho * diff(rho * diff(f, rho), rho) + 1/rho**2 * diff(diff(f, psi), psi) + diff(diff(f, z), z)
    # Check the divergence of F
    assert simplify(lap_f - geo.laplacian(f)) == 0, "euclidean_3_cyl Laplacian is wrong!"


def test_euclidean_3_sph_lap():
    """
    Check if the Laplacian of a scalar field in 3D spherical coordinates is correct.
    (By comparing with text book expression.)
    """
    # Define the geometry
    geo = examples.Euclidean3dSph()
    # Define a vector function
    f = geo.scalar_function('f')
    # Define the Laplacian of scalar f
    r, theta, phi = geo.coords
    lap_f         = 1/r**2 * diff(r**2 * diff(f, r), r) + 1/(r**2*sin(theta)) * diff(sin(theta) * diff(f, theta), theta) + 1/(r*sin(theta))**2 * diff(diff(f, phi), phi)
    # Check the divergence of F
    assert simplify(lap_f - geo.laplacian(f).refine(Q.positive(sin(theta)))) == 0, "euclidean_3_sph Laplacian is wrong!"


def test_schwarzschild():
    """
    Check the properties of the Schwarzschild geometry.
    """
    # Define the geometry
    geo = examples.Schwarzschild()
    # Extract the coordinates
    t, r, theta, phi = geo.coords
    # Verify the Ricci tensor
    assert geo.ricci.simplify() == Array(zeros(4))
    # Verify the Ricci scalar
    assert geo.ricci_scalar.simplify() == 0
    # Verify the Einstein tensor
    assert geo.einstein().simplify() == Array(zeros(4))
    # Verify the Kretchmann scalar
    assert geo.kretschmann_scalar().simplify() == 48 * geo.M**2 / r**6