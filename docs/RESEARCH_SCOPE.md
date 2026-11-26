# Research scope

## Purpose

MovingSpace is a Python research library for studying the reliability of
directional sensitivities when a parameter change affects both a mechanical
problem and its Galerkin trial space.

The motivating setting is geometry-driven structural analysis: changes in
geometry can alter the pulled-back mechanical operator, loads, support
representations, and the mechanical approximation space. A small state error
alone is not treated as evidence that the computed directional sensitivity is
reliable.

## Initial mathematical scope

The first reference setting is:

- linear variational mechanics;
- coercive, well-posed problems;
- a fixed discretization level during each parameter differentiation;
- parameter-dependent operators and loads;
- parameter-dependent affine support/lift data;
- parameter-dependent finite-dimensional trial subspaces;
- directional sensitivities with respect to explicit design directions.

The library will distinguish the continuous/reference problem, its discrete
Galerkin approximation, and the derivative of each. The meaning of a
"fixed discretization" must be stated per benchmark: a fixed reference mesh
with a parameter-dependent pullback is not the same as remeshing after every
geometry update.

## Out of scope for the initial release

- a general-purpose finite-element solver;
- automatic mesh generation or remeshing;
- nonlinear material laws, contact, plasticity, and dynamics;
- a general-purpose shape optimizer;
- claims of certified bounds before their assumptions and constants are
  implemented and independently verified;
- coupling to a particular FFD implementation as a mandatory dependency.

## Research principles

1. **Verification before breadth.** Every implemented identity or estimator
   must have a corresponding executable verification contract.
2. **Explicit derivatives.** Directional derivatives are explicit inputs or
   independently supplied reference quantities; automatic differentiation is
   optional, not foundational.
3. **Separate error categories.** State error, sensitivity error, estimator
   value, and certified upper bound are distinct quantities.
4. **No silent assumptions.** Geometry pullback, trial-space motion, support
   motion, and load variation must be represented separately.
5. **Solver independence.** The mathematical core must not require a specific
   FEM package. Backend adapters may be added after the reference contracts
   are stable.

## Status

This repository is an early research scaffold. The package import test is not
evidence that any research theorem, estimator, or certification result has
been validated.
