# Architecture

## Design boundary

MovingSpace is a sensitivity-analysis and verification layer, not a finite
element solver. It should accept algebraic or variational data from a caller
and expose a small set of mathematical interfaces. A later adapter may connect
those interfaces to a finite-element backend without making that backend a
core dependency.

## Conceptual layers

1. **Geometry and pullback**
   - parameterized domain maps;
   - Jacobians and directional map derivatives;
   - explicit reference-to-physical conventions.
2. **Mechanical problem**
   - bilinear/operator data;
   - load functional and its directional derivative;
   - support constraints and affine lifting data;
   - coercivity and well-posedness metadata where available.
3. **Trial spaces**
   - basis or subspace representation;
   - parameter dependence of the span;
   - projectors and basis/gauge transformations;
   - explicit directional motion.
4. **Sensitivity analysis**
   - state solve;
   - differentiated continuous and discrete equations;
   - moving-space and support/lift contributions;
   - exact identity checks.
5. **Estimation and certification**
   - fixed-space sensitivity proxy;
   - primal/dual residual information;
   - a posteriori bounds with their assumptions exposed;
   - directional ray-fidelity certification.
6. **Verification**
   - manufactured solutions;
   - algebraic reference cases;
   - independent finite-difference checks;
   - gauge-invariance and refinement studies.

## Mathematical problem convention

The initial abstract convention is an affine admissible set
g(theta) + V(theta) and a linear variational problem

a_theta(u_theta, v) = ell_theta(v) for admissible test functions,

with the homogeneous trial subspace and lift treated as distinct objects.
Concrete modules must document whether their unknown is the total state or the
homogeneous correction. This convention must not be changed implicitly.

## Directional derivative convention

A direction is an explicit vector d in parameter space. Directional
derivatives are denoted by D_d; finite-difference checks perturb
theta along theta +/- h d. The normalization of d must be stated in
each test and benchmark.

## Basis and gauge convention

A basis is a representation of a subspace, not the subspace itself. Numerical
quantities claimed to be subspace-invariant must be tested under nonsingular
basis changes that preserve the span. Basis derivatives must not be confused
with derivatives of the represented subspace.

## Backend policy

The first implementation target is a small solver-independent algebraic
reference layer. It will be used to verify identities on manufactured
finite-dimensional problems before introducing FEM adapters. Candidate
adapters are deliberately deferred until the contracts are stable.

## API policy

No public theorem or estimator API is frozen in this scaffold. Names and
signatures will be introduced only alongside a mathematical contract,
documented assumptions, and tests that exercise nontrivial cases.
