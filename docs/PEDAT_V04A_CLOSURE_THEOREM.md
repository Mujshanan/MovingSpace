# PEDAT-V04A-∞: Closure-Based Sensitivity-Error Bound

**Status:** theorem mathematically audited under stated assumptions; moving-domain specialization derived; numerical benchmark pending; Lean formalization not verified. This document records a research result, not an implemented or certified software feature.

## Abstract setting

Let (V,b₀) be a real Hilbert space. Let V̂ₕ⊂V be any linear subspace, not necessarily closed or finite-dimensional, and let W=cl(V̂ₕ) in the b₀ norm. Let Π̄:V→W be the orthogonal projection. Let ŷ(t) be the continuous solution, ŷₕ(t)∈V̂ₕ the Galerkin solution, and ê(t)=ŷₕ(t)−ŷ(t).

Assume:

- **A1:** bounded bilinear forms b̂ₜ are operator-norm differentiable at zero, with b̂₀=b₀ and derivative b′₀.
- **A2:** ŷ(t) and ŷₕ(t) are strongly differentiable in V at zero.
- **A3:** for a seminorm |·|ΩV and β≥0, |b′₀(u,vₕ)|≤β|u|ΩV||vₕ|| for u∈V, vₕ∈V̂ₕ; the second-slot continuity needed for closure extension holds (and follows from A1 for bounded forms).
- **A4-c:** b̂ₜ(ê(t),vₕ)=0 for all vₕ∈V̂ₕ and t near zero.

Density and continuity extend A3 and Galerkin orthogonality to W. Differentiating the extended orthogonality gives b₀(ė,w)=−b′₀(e,w) for w∈W, where e=ê(0). With p=Π̄ė and δ₀,V=|e|ΩV, testing by p yields ||p||≤βδ₀,V. Difference quotients of ŷₕ(t) belong to V̂ₕ; strong differentiability and closedness of W imply ẏₕ∈W, hence (I−Π̄)ė=−(I−Π̄)ẏ. Put δ̄₁=||(I−Π̄)ẏ||. Pythagoras gives

$$
\boxed{\|\dot e\|\le
\sqrt{\beta^2\delta_{0,V}^2+\bar\delta_1^2}.}
$$

The exact identity is ||Π̄ė||=sup_{w∈W\{0}} |b′₀(e,w)|/||w||; treat W={0} separately. The finite-dimensional theorem follows because finite-dimensional subspaces of Hilbert spaces are closed.

## Moving-domain scalar diffusion

For an orientation-preserving bi-Lipschitz map Tₜ:Ω̂→Ω(t), Fₜ=DTₜ, jₜ=det Fₜ>0, and scalar diffusion κ(x,t), the correct pullback is

$$
C_t=\kappa(T_t,t)j_tF_t^{-1}F_t^{-T},\quad
\widehat b_t(u,v)=\int_{\widehat\Omega}\nabla u^TC_t\nabla v.
$$

With aₜ=κ(Tₜ,t), F=F₀, Ḟ=Ḟ₀, j=j₀, ȧ₀=∂ₜκ(T₀,0)+∇ₓκ(T₀,0)·Ṫ₀, and j̇=j tr(F⁻¹Ḟ),

$$
\begin{aligned}
C'_0={}&\dot a_0jF^{-1}F^{-T}
+a_0\dot jF^{-1}F^{-T}\\
&-a_0jF^{-1}\dot F F^{-1}F^{-T}\\
&-a_0jF^{-1}F^{-T}\dot F^TF^{-T}.
\end{aligned}
$$

Both inverse-derivative terms are required.

For Option A, define |u|²ΩV,C₀=∫Ω̂V ∇uᵀC₀∇u. If C′₀ vanishes a.e. outside Ω̂V and C₀ is uniformly SPD, then with

$$
\beta=\operatorname*{ess\,sup}_{\widehat\Omega_V}
\|C_0^{-1/2}C'_0C_0^{-1/2}\|_2
$$

we obtain |b′₀(u,w)|≤β|u|ΩV,C₀||w||C₀. The support condition is essential. The PDE specialization also requires suitable coefficient/map regularity, uniform coercivity, differentiability of the pulled-back load and solution maps, and exact transport of the FE space; arbitrary remeshing is outside A4-c.

## Certified-estimator requirements

A certified result has the form

$$
\mathcal E_{cert}=\sqrt{\beta_{cert}^2\delta_{0,V,cert}^2+
\bar\delta_{1,cert}^2}
$$

only when each input is a proven upper bound. Sampling plus a safety factor is not a β certificate. A global reliable energy estimator can bound the local primal error conservatively; a region-restricted residual estimator is not automatically locally reliable. A fine sensitivity-grid difference is an indicator unless a guaranteed tail bound, including discretization and algebraic error, is supplied. Account for quadrature, geometry/coefficient representation, solver, and rounding errors.

## 1D manufactured example audit

For Tₜ(x)=x+tφ(x), φ=0.25sin(πx), κ(x,t)=1+0.3sin(πx)+0.2t cos(πx), Cₜ=κ(Tₜ,t)/(1+tφ′), direct differentiation gives

$$
C_0=1+0.3\sin(\pi x),\qquad
C'_0=(0.2-\pi/4)\cos(\pi x).
$$

Therefore C′₀ is active across the interior except isolated zeros; ΩV=(0.2,0.8) is not a valid support region. Use ΩV=(0,1). A conservative analytic upper bound is βcert=π/4−0.2, since C₀≥1 and |cos(πx)|≤1.

For ŷ(x,t)=sin(πTₜ(x))e^(−0.4t),

$$
\partial_x\dot{\widehat y}(x,0)=
-\pi^2\sin(\pi x)\phi(x)
+\pi\cos(\pi x)\phi'(x)
-0.4\pi\cos(\pi x).
$$

The revised numerical run has not completed. High-order quadrature and finite-difference sweeps are planned diagnostics, not validated certificates. Finite quadrature does not automatically give exact continuous Galerkin orthogonality. No numerical results or certified final bound are claimed.

## Verification status

The closure argument is mathematically established under A1–A4-c. The Lean source still requires compilation with the pinned toolchain and no unfinished proof placeholders; it is not formally verified. The benchmark must be executed and its quadrature and finite-difference sweeps inspected. Keep theorem, PDE specialization, and estimator implementation as separate layers; proof of the theorem does not certify software or estimator values.
