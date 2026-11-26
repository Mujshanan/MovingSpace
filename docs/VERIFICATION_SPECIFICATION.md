# Verification specification

## Purpose and status

This document defines the verification obligations for the first research
implementation. It is a test specification, not a claim that the tests or
the underlying results have already been implemented or passed.

Each theorem or estimator is to be translated into: (i) assumptions,
(ii) computable inputs, (iii) an exact or reference quantity,
(iv) an executable check, and (v) a stated tolerance or acceptance rule.

## Verification levels

- **V0 — software integrity:** installation, imports, deterministic tests,
  input validation, and reproducible benchmark configuration.
- **V1 — algebraic identity:** exact or high-precision finite-dimensional
  examples where both sides of an identity can be evaluated independently.
- **V2 — derivative verification:** independent central finite differences
  and step-size sweeps against analytic or independently assembled
  directional derivatives.
- **V3 — invariance and robustness:** basis/gauge transformations,
  coordinate changes where applicable, and conditioning studies.
- **V4 — estimator verification:** observed errors compared with estimator
  values and, only where justified, certified bounds.
- **V5 — refinement:** systematic increase of trial-space dimension and
  resolution with convergence and effectivity reporting.

## Test matrix

### 1. Moving-subspace sensitivity identity

**Reference cases**
- Manufactured finite-dimensional parameter-dependent matrices and trial
  subspaces.
- Include a genuinely rotating subspace; a constant subspace is only a
  control case.
- Compare both sides of the exact identity using independently computed
  state, projector, and directional subspace-motion data.

**Acceptance**
- Algebraic residual is at the scale predicted by floating-point conditioning.
- The rotating-subspace case must fail if the subspace-motion term is
  deliberately omitted.
- Results must be invariant under a nonsingular change of basis spanning the
  same trial subspace.

### 2. Support/lift kinematics and baseline-error leakage

**Reference cases**
- Prescribed support motion with a nonzero lift derivative.
- Fixed support as a zero-motion control.
- A case with nonzero baseline state error, so leakage cannot vanish
  trivially.

**Acceptance**
- Direct differentiation and the independently assembled identity agree.
- The fixed-support control removes only the support-motion contribution.
- A deliberately omitted lift term is detected by at least one nontrivial
  manufactured case.

### 3. Orthogonal fixed-space sensitivity proxy

**Reference cases**
- Compare moving-space sensitivity with the fixed-space proxy.
- Evaluate the orthogonal defect independently.
- Include a case where the normal component of trial-space motion is nonzero.

**Acceptance**
- The defect identity closes to numerical tolerance.
- The proxy agrees with the moving-space result when normal subspace motion
  vanishes.
- A basis rotation that leaves the represented subspace unchanged does not
  alter the proxy or defect.

### 4. Directional finite-difference checks

**Reference cases**
- Central-difference sweeps over a logarithmic sequence of step sizes.
- At least one analytic manufactured sensitivity.
- Perturbations in both positive and negative directions where admissible.

**Acceptance**
- A second-order convergence region is observed before roundoff or solver
  tolerance dominates.
- Report the full step-size/error table; do not select a single favorable
  step after inspection.
- Finite differences are an independent check, not the sole definition of
  the sensitivity.

### 5. A posteriori sensitivity estimator and bound

**Reference cases**
- Cases with independently known sensitivity error.
- Cases with nonzero primal and dual residuals.
- A sequence of increasingly accurate trial spaces.

**Acceptance**
- Report observed error, estimator, effectivity index, and all constants.
- A certified-bound test passes only if proven assumptions are checked and
  the computed bound encloses the independently known error, up to a declared
  roundoff allowance.
- A heuristic indicator must never be labelled a certified bound.

### 6. Directional ray-fidelity radius

**Reference cases**
- Manufactured response along a parameter ray.
- Cases with known local and nonlocal behavior.
- Points immediately inside and outside the predicted admissible radius.

**Acceptance**
- The stated fidelity criterion holds throughout the certified interval,
  within its declared numerical tolerance.
- The radius must not be reported as a global trust region unless the theorem
  proves that stronger statement.
- Failure outside the radius is informative but is not required unless the
  theorem explicitly asserts sharpness.

### 7. Trial-space refinement

**Reference cases**
- Nested and, separately, non-nested trial-space sequences.
- Increasing mechanical trial-space dimension.
- Fixed geometry and fixed parameter direction across the sequence.

**Acceptance**
- Report state error, sensitivity error, estimator, effectivity, and
  conditioning at every level.
- Do not assume monotonicity of sensitivity error or effectivity unless a
  theorem establishes it.
- Separate approximation error from algebraic-solver error.

## Cross-cutting requirements

- Use deterministic seeds for randomized tests.
- Record precision, solver tolerances, and condition numbers.
- Use relative and absolute tolerances; avoid one absolute tolerance for
  differently scaled quantities.
- Include negative tests that remove a theoretically required term.
- Keep reference calculations independent from the implementation under test.
- Preserve raw numerical tables for publication and regression analysis.

## Initial release gate

The first public research release must not claim theorem verification merely
because the package imports or the smoke test passes. Before any mathematical
module is described as verified, its corresponding V1/V2 tests must pass.
Before an estimator is called certified, V4 must pass under the theorem's
explicit assumptions. Refinement claims require V5 evidence.
