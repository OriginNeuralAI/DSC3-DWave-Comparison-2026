# Frequently Asked Questions

Pre-emptive answers to the questions a careful reader, reviewer, or procurement officer would ask. Detailed treatment in `main.pdf`.

---

## Q: You claim DSC-3 reaches N = 10⁶ spins on a $1.57/hour droplet. Does it find a "true" ground state at that scale?

**A: No.** At L = 100 (N = 10⁶) we run the *fast* preset (limited step + restart budget) and reach E/E_LB = 0.5581, which is ~6.3% below the Hartmann (2001) thermodynamic-limit asymptote of 0.5954. This is a preset-induced gap, not an engine ceiling: at production preset for L ≤ 40 (N ≤ 64,000) we are within 1% of Hartmann. The paper documents an attempted production-preset run at L = 100 that was OOM-killed on the 62 GB droplet — explicit reproducible negative observation in §9 of `main.pdf`. A 128 GB droplet would close that gap.

## Q: Why doesn't the abstract just say "we solve 10⁶ spins"?

**A:** Because saying so without conditioning on preset, seeds, and quality target would be the same kind of headline-without-fine-print this paper criticises D-Wave for. The abstract conditions all three explicitly.

## Q: The MaxCut Δ vs SA-only is +0.13% at N=10,000 d=0.50. Isn't that within noise?

**A: No.** σ across n=3 seeds is 0.010% at that cell, so Δ/σ = 13 — many standard deviations above zero. The same is true for every (N, d) cell in §B3 of `main.pdf`. See `tab:b3_maxcut_5000` for the full table with σ_Δ column.

## Q: You compare DSC-3 to "matched-budget" SA-only. Is that wall-clock-matched?

**A: No, it's compute-intensity-matched** (same step count, same restart count, same per-call timeout — see §2 of `main.pdf`). The 16-solver ensemble dispatch uses ~10× more wall-time than a single SA-only chain because all sixteen solvers run in parallel. A wall-clock-matched SA baseline (giving SA 10× the parameter budget) is a stricter comparison; we did not run it in this round and acknowledge it as a follow-up. Falsification F2 is explicit about this scope.

## Q: D-Wave's "1 million Frontier-years" sampling result on the 3D ±J quench — does your work disprove it?

**A: No.** That is a sampling-fidelity claim (matching the quantum quench distribution); our paper is about ground-state arg-min on the same Hamiltonian. The two are different problems with different complexity classes. See §15.1 of `main.pdf`.

## Q: For B3 MaxCut you ran "matched-spec random ensembles" — why not D-Wave's actual Stride instances?

**A:** Because D-Wave has not released those instance files. We generate Erdős–Rényi MaxCut at the same N, density, and sign distribution as the Stride paper's reported scales, with deterministic seeds documented in §B3 of `main.pdf` and reproducible from `make_plots.py` + `aggregate_results.py`. This is `matched-spec` in the Reproduction Fidelity Map (Table 5), not exact reproduction.

## Q: Why is the ratio sometimes "10⁴–10⁵" and sometimes "~10²"?

**A:** The 10⁴–10⁵ figure compares capex-amortised D-Wave Advantage2 cost ($229–343/hour) to DSC-3 droplet cost ($1.57/hour) at the same wall-time. The ~10² figure compares per-solve dollar cost using the upper bound of D-Wave's public Leap tier pricing ($1.30/solve) to DSC-3's measured per-solve cost ($0.024 at N=1,728). Different normalisations yield different ratios; all four are tabulated in §11 of `main.pdf`.

## Q: The cryptanalysis claim — DSC-3 has SHA-256 / AES / RSA / GNFS encoders. Are those production-ready cryptanalysis tools?

**A: No, they are reduced-round demonstrations.** Full SHA-256 (r=64) and crypto-grade AES-128/256 remain out of reach for all known annealers, classical or quantum. The B5 PoQW result is at r=4 SHA-256 rounds — a functional demonstration, not a crypto-grade attack. B6 capability-only framing in `main.pdf` is precise about this. The point is that D-Wave has no comparable publication in this vertical; we acknowledge our results are also non-cryptographic.

## Q: How would I evaluate DSC-3 on my own workload?

**A:** Three paths:

1. **Live demo (zero install):** Try DSC-3 in a browser at <https://dsc3.originneural.ai/>. Two REST endpoints — `POST /v1/solve` (problem you supply, up to 5×10⁸ spins) and `POST /v1/mega-benchmark` (full 1M → 500M scaling sweep). The endpoints share the same engine binary used in this paper.
2. **Reproduce the paper:** Follow Appendix A of `main.pdf` and `run_*.sh` scripts in this repo on a comparable GPU droplet.
3. **Adapt to your workload:** Map your problem to an Ising / QUBO formulation (the `src/problems/` encoders in the parent `isomorphic-engine` repository have examples for 16 problem classes), run on the same DSC-3 engine, compare to your existing classical solvers at matched compute budget.

## Q: Is D-Wave Advantage2 obsolete?

**A: No, and the paper does not claim it is.** D-Wave wins on (W1) quantum-coherent sampling fidelity, (W2) wall-clock at native QPU instance size, (W3) latency-critical real-time decision loops where the 100 ns anneal cycle matters, and (W4) reverse-annealing protocols. For ground-state optimisation in the regime our cost numbers cover, the procurement case for a $10–15M Advantage2 system over a $1.57/hour cloud droplet is harder to make on the published evidence — that's the paper's narrower claim. See §14 W1–W4 of `main.pdf`.

## Q: When will you push the L = 100 production-preset result?

**A:** On a 128 GB-RAM droplet. The OOM on the 62 GB droplet is a documented negative observation in §9, not a permanent gap. A 128 GB droplet is roughly $5–10/hour from DigitalOcean GPU Optimized; the run takes ~90 min single-seed. We will update the paper to v0.15.2 with the L=100 production-preset row if and when it lands.

## Q: Is there a Zenodo DOI?

**A: Pending.** GitHub Release `v0.15.1-paper` is now eligible for Zenodo's automatic GitHub→DOI integration. When the toggle is flipped on Zenodo's side, the next release will mint a DOI we'll fold back into the paper title page and update CITATION.cff.

## Q: Can I quote a figure or table?

**A: Yes**, under CC-BY-4.0 (see `LICENSE`). Attribution: *Daugherty, Ward, Ryan (Origin Neural, 2026), DSC-3 vs D-Wave Advantage2 industrial benchmarks, [URL]*. No prior permission needed for academic use.
