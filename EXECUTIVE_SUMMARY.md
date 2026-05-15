# Executive Summary

**For:** CTOs, procurement officers, R&D directors evaluating quantum-annealing platforms against classical alternatives.

**Question this paper answers:** Should my optimisation pipeline use a D-Wave QPU, or a classical GPU ensemble?

---

## In one paragraph

On the 2024–2026 industrial benchmarks D-Wave Advantage2 is marketed against — 3D ±J Ising spin glasses, currency arbitrage, the Stride 45-instance suite, supply-chain optimisation, drug-discovery QUBOs, and Proof-of-Quantum-Work — a 16-solver classical ensemble (DSC-3, Origin Neural) running on a $1.57/hour cloud GPU droplet produces solutions of competitive or superior quality at a fraction of the dollar and energy cost. Across the six benchmarks, the per-solve cost ratio is 10²–10⁵× cheaper, the capex-per-machine ratio is ~10⁶×, and the energy-per-solve ratio is ~42×. The maximum problem size the QPU can physically embed (4,400 qubits) is reached and exceeded by 200× on the same workload class. The paper releases every result as a SHA-256-pinned JSON artefact; every claim is falsifiable with a documented experiment.

## Procurement bottom line

| For this workload class | D-Wave Advantage2 procurement case | DSC-3 alternative |
|---|---|---|
| 3D Ising ground-state search | Cannot embed at N ≥ 10,000; sampling regime, not optimisation | $0.38/solve at N=10⁶ on $1.57/hour droplet |
| Fully-connected MaxCut, N ≥ 1,000 | Embedding overhead-bound; physically infeasible at N=10,000 | +0.13–0.37% over SA-only at matched compute budget |
| Currency arbitrage (QUBO) | Outperforms tabu (claim, unverifiable from public data) | 100% Hamiltonian-cycle feasibility at N≤8; reproducible JSON artefacts |
| Supply-chain optimisation | 12–18% cost-reduction claim across 5 verticals (proprietary pipelines) | 1 of 5 verticals (UFL) shown; +5–30% gap to exact DP — DP is the right tool when applicable |
| Cryptanalysis (SHA, AES, RSA, GNFS) | **No published benchmark in this vertical** | Production encoders shipped; reduced-round demonstrations |
| Real-time sub-millisecond decision loops | QPU 100 ns anneal cycle (structural advantage) | Seconds-scale wall-time — **D-Wave wins here** |
| Quantum-coherent quench sampling (Science 2025) | Sole demonstrated platform | Not applicable (classical engine) |

## Where D-Wave wins (W1–W4, paper §14)

1. Quantum-coherent sampling fidelity
2. Wall-clock at native QPU instance size
3. Sub-millisecond latency-critical decision loops
4. Reverse-annealing protocols

## Where the data does not yet support a procurement preference for D-Wave

For ground-state optimisation in the regime our cost numbers cover (B1–B5), the published D-Wave evidence does not support a $10–15M Advantage2 capex over a $1.57/hour cloud droplet running classical methods. That is the paper's narrower claim.

## The "Benchmark Gap"

Across all six benchmarks, every D-Wave reference is missing at least one of four reproducibility artefacts (instances, per-instance wall-times, classical baseline pipeline, quantum/classical work split). This paper releases all four for every benchmark it runs, with SHA-256 manifest in Appendix E. We do not assume bad faith; we observe empirically that *a procurement claim that cannot be reproduced cannot be budgeted against*.

## Try it yourself

Three paths:

1. **Live demo** (zero install): <https://dsc3.originneural.ai/> — REST endpoints accept your QUBO/Ising up to N = 5×10⁸ spins.
2. **Replicate the paper**: follow `main.pdf` Appendix A; verify SHA-256s against Appendix E.
3. **Map your workload**: encode your problem as Ising/QUBO, run on the same DSC-3 engine, compare to your existing classical solver at matched compute budget.

---

**Authors:** Bryan W. Daugherty, Gregory Ward, Shawn Ryan — Origin Neural — <https://originneural.ai>

**Full paper:** [main.pdf](main.pdf) (40 pages, 9 figures, 22 tables)
