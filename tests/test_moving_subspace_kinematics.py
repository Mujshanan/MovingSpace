"""Independent verification of finite-dimensional moving-subspace kinematics.

The oracle uses Euclidean orthogonal projectors. It is deliberately separate
from the mechanical energy projection and from any public MovingSpace API.
"""

import numpy as np
import numpy.typing as npt


def _basis_data(theta: float) -> tuple[npt.NDArray, npt.NDArray]:
    """Return a full-rank basis V(theta) and its exact derivative."""
    v0 = np.array(
        [[1.0, 0.0], [0.0, 1.0], [0.4, 0.2], [0.1, 0.7]]
    )
    v1 = np.array(
        [[0.1, 0.05], [-0.08, 0.12], [0.2, -0.03], [0.04, 0.09]]
    )
    v2 = np.array(
        [[0.02, -0.01], [0.03, 0.01], [-0.04, 0.02], [0.01, -0.03]]
    )
    return v0 + theta * v1 + theta**2 * v2, v1 + 2.0 * theta * v2


def _projector(v: npt.NDArray) -> npt.NDArray:
    """Euclidean orthogonal projector onto range(V)."""
    return v @ np.linalg.solve(v.T @ v, v.T)


def _projector_derivative(v: npt.NDArray, v_dot: npt.NDArray) -> npt.NDArray:
    """Differentiate P = V (V.T V)^(-1) V.T analytically."""
    gram_inverse = np.linalg.inv(v.T @ v)
    gram_dot = v_dot.T @ v + v.T @ v_dot
    return (
        v_dot @ gram_inverse @ v.T
        - v @ gram_inverse @ gram_dot @ gram_inverse @ v.T
        + v @ gram_inverse @ v_dot.T
    )


def _normal_velocity(p: npt.NDArray, p_dot: npt.NDArray) -> npt.NDArray:
    """Normal component of subspace velocity acting on vectors in range(P)."""
    identity = np.eye(p.shape[0])
    return (identity - p) @ p_dot @ p


def test_projector_derivative_matches_independent_central_difference() -> None:
    theta = 0.31
    v, v_dot = _basis_data(theta)
    analytic = _projector_derivative(v, v_dot)

    errors = []
    for step in (1.0e-2, 3.0e-3, 1.0e-3):
        p_plus = _projector(_basis_data(theta + step)[0])
        p_minus = _projector(_basis_data(theta - step)[0])
        finite_difference = (p_plus - p_minus) / (2.0 * step)
        errors.append(np.linalg.norm(finite_difference - analytic))

    assert errors[0] > errors[1] > errors[2]
    assert errors[2] < 1.0e-7


def test_projector_derivative_obeys_differentiated_projector_constraints() -> None:
    v, v_dot = _basis_data(0.31)
    p = _projector(v)
    p_dot = _projector_derivative(v, v_dot)
    identity = np.eye(p.shape[0])

    # P^2=P implies P P_dot P=0 and (I-P)P_dot(I-P)=0.
    np.testing.assert_allclose(p, p.T, rtol=0.0, atol=1.0e-13)
    np.testing.assert_allclose(p @ p, p, rtol=0.0, atol=1.0e-13)
    np.testing.assert_allclose(p_dot, p_dot.T, rtol=0.0, atol=1.0e-12)
    np.testing.assert_allclose(p @ p_dot @ p, 0.0, rtol=0.0, atol=1.0e-12)
    np.testing.assert_allclose(
        (identity - p) @ p_dot @ (identity - p),
        0.0,
        rtol=0.0,
        atol=1.0e-12,
    )


def test_normal_subspace_velocity_is_gauge_invariant() -> None:
    theta = 0.31
    v, v_dot = _basis_data(theta)
    generator = np.array([[0.2, 0.1], [-0.05, 0.15]])
    transform = np.eye(2) + theta * generator
    transformed_v = v @ transform
    transformed_v_dot = v_dot @ transform + v @ generator

    p = _projector(v)
    p_dot = _projector_derivative(v, v_dot)
    transformed_p = _projector(transformed_v)
    transformed_p_dot = _projector_derivative(transformed_v, transformed_v_dot)

    np.testing.assert_allclose(transformed_p, p, rtol=1.0e-12, atol=1.0e-12)
    np.testing.assert_allclose(
        _normal_velocity(transformed_p, transformed_p_dot),
        _normal_velocity(p, p_dot),
        rtol=1.0e-11,
        atol=1.0e-11,
    )


def test_pure_basis_gauge_motion_has_zero_normal_velocity() -> None:
    v, _ = _basis_data(0.31)
    generator = np.array([[0.2, 0.1], [-0.05, 0.15]])
    p = _projector(v)
    p_dot = _projector_derivative(v, v @ generator)

    np.testing.assert_allclose(
        _normal_velocity(p, p_dot),
        0.0,
        rtol=0.0,
        atol=1.0e-12,
    )


def test_normal_error_derivative_identity_with_nonzero_normal_velocity() -> None:
    theta = 0.31
    v, v_dot = _basis_data(theta)
    p = _projector(v)
    p_dot = _projector_derivative(v, v_dot)
    identity = np.eye(4)

    y0 = np.array([0.8, -0.4, 1.2, 0.3])
    y1 = np.array([-0.2, 0.5, 0.1, -0.3])
    y2 = np.array([0.05, -0.02, 0.03, 0.01])
    y = y0 + theta * y1 + theta**2 * y2
    y_dot = y1 + 2.0 * theta * y2

    error_dot = -p_dot @ y + (identity - p) @ y_dot
    left = (identity - p) @ error_dot
    right = (identity - p) @ y_dot - _normal_velocity(p, p_dot) @ y

    assert np.linalg.norm(_normal_velocity(p, p_dot)) > 1.0e-3
    np.testing.assert_allclose(left, right, rtol=1.0e-12, atol=1.0e-12)
