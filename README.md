# MovingSpace

**MovingSpace** is a Python research library for investigating directional
sensitivity reliability in parameter-dependent Galerkin spaces, with a focus
on geometry-driven structural mechanics.

> **Status: early research scaffold.** The package structure, scope, and
> verification plan are being established. The mathematical sensitivity
> identities, estimators, and certification procedures are not yet implemented
> or validated.

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
| Mathematical reference implementation | Not yet implemented |
| Sensitivity identities and tests | Not yet implemented |
| A posteriori estimator and certification | Not yet implemented |
| FEM adapters and benchmarks | Deferred |

## Install for development

Python 3.11 or newer is required.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
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

A passing package-import test is only a software smoke test. It is not evidence
that a theorem or estimator has been verified.

## License

The project license has not yet been selected. This repository is currently
private; no public reuse or redistribution terms are asserted at this stage.
