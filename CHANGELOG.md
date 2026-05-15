# Changelog

All notable changes to this paper and its accompanying artefacts.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [v0.15.2-paper] — 2026-05-14

Zenodo-anchored release.

- **Zenodo DOI minted: [10.5281/zenodo.20192275](https://doi.org/10.5281/zenodo.20192275)**
- Paper title page now displays the DOI
- README + CITATION.cff updated with DOI reference
- DOI badge added to README header

## [v0.15.1-paper] — 2026-05-14

Initial public release.

### Paper

- 40-page LaTeX paper covering six benchmark families (B1–B6) reproducing
  D-Wave Advantage2's 2024–2026 published industrial benchmarks on the
  DSC-3 classical 16-solver ensemble.
- Headline result: 3D ±J Ising ground states matching Hartmann (2001) within
  1% at production preset for L ≤ 40 (N ≤ 64,000); droplet-feasible ceiling
  probe at L = 100 (N = 10⁶) at fast preset (E/E_LB = 0.5581).
- MaxCut crossover at N = 5,000 and N = 10,000 with σ-error bars
  (3 seeds per cell, all Δ/σ ≥ 13).
- Honest documentation of production-preset L = 100 OOM on the 62 GB
  droplet as a reproducible negative observation.

### Data artefacts

- 12 load-bearing JSON result files with SHA-256 digests pinned in
  paper Appendix E.
- 24 auxiliary smoke/dev JSONs in `results/` for transparency.
- 9 figures (PDF + PNG previews).
- 15 generated LaTeX tables in `tables/`.

### Reproducibility scripts

- `aggregate_results.py` — JSON → LaTeX table generator.
- `make_plots.py` — JSON → matplotlib figure generator.
- `rebuild_paper.sh` — full pipeline driver.
- `run_*.sh` / `run_*.bat` — exact commands used on the gpu-ramp droplet
  and local 5070 Ti workstation.

### Methodology

- Multi-seed protocol (n ≥ 4 on B1, B2, B4, B5; n = 3 on B3).
- Compute-intensity-matched SA-only baseline for B1 / B3 MaxCut.
- Exact dynamic-programming baseline for B3 Knapsack and B4 / B5 (drug).
- Reproduction Fidelity Map classifying each benchmark as
  full / matched-class / matched-spec / partial / capability-only.

### Companion work

- Cites companion paper: *DSC-3 Benchmark Suite: 500 Million Spins on a
  Single GPU* (Daugherty, Ward, Ryan; Origin Neural, April 2026).
