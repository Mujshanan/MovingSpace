"""Independent finite-dimensional oracle for moving Galerkin sensitivities.

These tests verify the differentiated discrete Galerkin equations against
central finite differences. The helpers deliberately live in the test suite:
they are a reference oracle, not yet the public MovingSpace API.
"""

import numpy as np
import numpy.typing as npt


def _data(theta: float) -> tuple[npt.NDArray, ...]:
    a0 = np.array(
        [
            [4.0, 0.3, 0.1, 0.0],
            [0.3, 3.5, 0.2, 0.1],
            [0.1, 0.2, 3.0, 0.25],
            [0.0, 0.1, 0.25, 2.8],
        ]
    )
    a1 = np.array(
        [
            [0.2, 0.05, 0.0, 0.0],
            [0.05, -0.1, 0.03, 0.0],
            [0.0, 0.03, 0.15, 0.02],
            [0.0, 0.0, 0.02, -0.05],
        ]
    )
    f0 = np.array([1.0, -0.5, 2.0, 0.7])
    f1 = np.array([0.3, 0.2, -0.4, 0.1])
    g0 = np.array([0.1, 0.0, -0.1, 0.05])
    g1 = np.array([0.2, -0.1, 0.05, 0.08])
    v0 = np.array([[1.0, 0.0], [0.0, 1.0], [0.5, 0.2], [0.1, 0.6]])
    v1 = np.array([[0.05, 0.1], [-0.08, 0.03], [0.1, -0.04], [0.02, 0.07]])
    return a0 + theta * a1, f0 + theta * f1, g0 + theta * g1, v0 + theta * v1


def _solve(theta: float, *, gauge_transform: bool = False) -> npt.NDArray:
    a, f, g, v = _data(theta)
    if gauge_transform:
        transform = np.eye(2) + theta * np.array([[0.2, 0.1], [-0.05, 0.15]])
        v = v @ transform
    reduced_operator = v.T @ a @ v
    reduced_load = v.T @ (f - a @ g)
    q = np.linalg.solve(reduced_operator, reduced_load)
    return g + v @ q


def _directional_sensitivity(
    theta: float,
    *,
    include_lift_derivative: bool = True,
    include_space_motion: bool = True,
    gauge_transform: bool = False,
) -> npt.NDArray:
    a, f, g, v = _data(theta)
    a_dot = np.array(
        [
            [0.2, 0.05, 0.0, 0.0],
            [0.05, -0.1, 0.03, 0.0],
            [0.0, 0.03, 0.15, 0.02],
            [0.0, 0.0, 0.02, -0.05],
        ]
    )
    f_dot = np.array([0.3, 0.2, -0.4, 0.1])
    g_dot = np.array([0.2, -0.1, 0.05, 0.08])
    v_dot = np.array([[0.05, 0.1], [-0.08, 0.03], [0.1, -0.04], [0.02, 0.07]])

    if not include_lift_derivative:
        g_dot = np.zeros_like(g_dot)

    if gauge_transform:
        transform_generator = np.array([[0.2, 0.1], [-0.05, 0.15]])
        transform = np.eye(2) + theta * transform_generator
        v_dot = v_dot @ transform + v @ transform_generator
        v = v @ transform

    if not include_space_motion:
        v_dot = np.zeros_like(v_dot)

    q = np.linalg.solve(v.T @ a @ v, v.T @ (f - a @ g))
    state = g + v @ q
    residual = a @ state - f

    reduced_operator = v.T @ a @ v
    reduced_rhs = (
        -v_dot.T @ residual
        - v.T @ (a_dot @ state + a @ g_dot + a @ v_dot @ q - f_dot)
    )
    q_dot = np.linalg.solve(reduced_operator, reduced_rhs)
    return g_dot + v_dot @ q + v @ q_dot


def test_moving_galerkin_sensitivity_matches_central_difference() -> None:
    theta = 0.23
    exact_directional = _directional_sensitivity(theta)

    errors = []
    for step in (3.0e-3, 1.0e-3):
        finite_difference = (_solve(theta + step) - _solve(theta - step)) / (2.0 * step)
        errors.append(np.linalg.norm(finite_difference - exact_directional))

    assert errors[0] > 0.0
    assert errors[1] < errors[0] / 7.5
    assert errors[1] < 5.0e-9


def test_lift_derivative_is_required_for_moving_support_case() -> None:
    theta = 0.23
    step = 1.0e-4
    finite_difference = (_solve(theta + step) - _solve(theta - step)) / (2.0 * step)
    correct = _directional_sensitivity(theta)
    missing_lift_term = _directional_sensitivity(theta, include_lift_derivative=False)

    assert np.linalg.norm(finite_difference - correct) < 1.0e-8
    assert np.linalg.norm(finite_difference - missing_lift_term) > 1.0e-2


def test_trial_space_motion_term_is_nontrivial_and_required() -> None:
    theta = 0.23
    correct = _directional_sensitivity(theta)
    fixed_space_approximation = _directional_sensitivity(theta, include_space_motion=False)

    assert np.linalg.norm(correct - fixed_space_approximation) > 1.0e-2


def test_sensitivity_is_invariant_under_parameter_dependent_basis_gauge() -> None:
    theta = 0.23
    original_state = _solve(theta)
    transformed_state = _solve(theta, gauge_transform=True)
    original_sensitivity = _directional_sensitivity(theta)
    transformed_sensitivity = _directional_sensitivity(theta, gauge_transform=True)

    np.testing.assert_allclose(original_state, transformed_state, rtol=1.0e-12, atol=1.0e-12)
    np.testing.assert_allclose(
        original_sensitivity,
        transformed_sensitivity,
        rtol=1.0e-11,
        atol=1.0e-11,
    )
