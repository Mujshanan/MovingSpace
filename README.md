# MovingSpace

**MovingSpace** is a Python research library for investigating directional
sensitivity reliability in parameter-dependent Galerkin spaces, with a focus
on geometry-driven structural mechanics.

> **Status: early research scaffold.** The package structure, scope, and
> verification plan are established. A first finite-dimensional moving-Galerkin
> derivative oracle is included in the test suite. The research sensitivity
> error identities, a posteriori estimators, and certification procedures are
> not yet implemented or validated.

## Research objective

A geometry/design parameter can change the mechanical operator, loads,
support/lifting data, and the mechanical trial space at the same time. Accurate
state solutions do not, by themselves, certify accurate directional
sensitivities.

MovingSpace is intended to provide a solver-independent framework for
representing these effects, checking exact sensitivity identities, and
developing a posteriori sensitivity-error estimation and directional
fidelity certification.

## Initial scope

The initial reference setting is linear, coercive variational mechanics with
a fixed discretization level during each parameter differentiation. The
framework will explicitly distinguish:

- geometry mapping and reference-domain pullback;
- parameter-dependent mechanical operators and loads;
- support constraints and affine lifting;
- parameter-dependent trial subspaces and their motion;
- state error and directional sensitivity error;
- heuristic estimators and mathematically certified bounds.

MovingSpace is **not** intended to be a general-purpose finite-element solver
or a general-purpose structural optimizer. FEM integrations will be optional
adapters after the mathematical interfaces are verified.

## Repository status

| Area | Status |
|---|---|
| Python package scaffold | Initial |
| Research scope and architecture | Drafted |
| Verification specification | Drafted |
| Finite-dimensional moving-Galerkin derivative oracle | Initial test reference |
| Research sensitivity-error identities | Not yet implemented |
| A posteriori estimator and certification | Not yet implemented |
| FEM adapters and benchmarks | Deferred |

## Installation

Python 3.11 or newer is required.

Install the current public verification branch:

```bash
python -m pip install "git+https://github.com/Mujshanan/MovingSpace.git@foundation/verification-first"
```

For development and verification tools:

```bash
python -m pip install "movingspace[dev] @ git+https://github.com/Mujshanan/MovingSpace.git@foundation/verification-first"
```

Then import the package:

```python
import movingspace
print(movingspace.__version__)
```

For a local development checkout:

```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# Linux/macOS:
source .venv/bin/activate

python -m pip install -e ".[dev]"
python -m pytest
ruff check .
```

## Project documents

- [Research scope](docs/RESEARCH_SCOPE.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Verification specification](docs/VERIFICATION_SPECIFICATION.md)

## Verification-first policy

Every mathematical feature must have documented assumptions, an independent
reference calculation, and executable tests. The verification plan includes
moving-subspace identities, support/lift kinematics, the fixed-space
sensitivity proxy, finite-difference step-size sweeps, estimator bounds,
directional ray-fidelity checks, and trial-space refinement.

The current algebraic tests are reference checks for the differentiated
discrete Galerkin equations. They are not yet verification of the full
research theorems or any certified estimator.

## License and reuse

The repository is publicly visible, but no open-source license has been
selected. Public visibility alone does not grant permission to redistribute,
modify, or reuse the code. A license will be added after the project’s
licensing terms are decided.
