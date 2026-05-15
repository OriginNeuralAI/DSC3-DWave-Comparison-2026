# Results — artefact taxonomy

Every JSON in this directory is either *load-bearing* (cited in a paper table or figure with its SHA-256 in Appendix E of `main.pdf`) or *auxiliary* (smoke tests, dev scaffolding, kept for transparency).

## Load-bearing artefacts (12)

These have their SHA-256 digests pinned in Appendix E of `main.pdf`:

| File | Benchmark | What it contains |
|---|---|---|
| `b1_full.json` | B1 | L = 4–12 production preset, droplet, n = 4 seeds |
| `b1_local_5070ti.json` | B1 | L = 4–12 production preset, 5070 Ti workstation, hardware-generality check |
| `b1_local_extreme.json` | B1 | L = 50, 60, 80 fast preset, 5070 Ti, ceiling probe |
| `b1_gpu_scale.json` | B1 | L = 14–20 GPU + SA baseline, droplet |
| `b2_smoke.json` | B2 | N = 6, 8 currencies, quality preset, n = 4, 100% feasibility |
| `b2_arbitrage_n10_12.json` | B2 | N = 10, 12 currencies, production preset, 2/4 feasibility |
| `b3_full.json` | B3 | 45 Stride-class instances (TSP / Knapsack / MaxCut), quality preset |
| `b3_gpu_batched.json` | B3 | MaxCut N up to 2,000 + Knapsack 10–50, deep-exploration GPU dispatch |
| `b3_maxcut_xlarge.json` | B3 | MaxCut N = 5,000 + 10,000 beyond-embedding probe, n = 3 seeds per cell |
| `b4_facility.json` | B4 | Uncapacitated Facility Location (M, N) ≤ (8, 20), n = 4 |
| `b5_drug.json` | B5 | Drug-fragment selection QUBO, N ≤ 25 fragments, n = 4 |
| `b5_poqw.json` | B5 | Reduced-round (r = 4, 6, 8) SHA-256 preimage Ising, n = 4 |

To verify against the paper's SHA-256 manifest:

```bash
sha256sum b1_full.json b1_local_5070ti.json b1_local_extreme.json \
          b1_gpu_scale.json b2_smoke.json b2_arbitrage_n10_12.json \
          b3_full.json b3_gpu_batched.json b3_maxcut_xlarge.json \
          b4_facility.json b5_drug.json b5_poqw.json
```

Compare against Appendix E (Table `tab:data_manifest`) of `main.pdf`.

## Auxiliary artefacts (smoke / dev scaffolding)

These are kept for transparency about the development trajectory; they are not cited in the paper:

- `b1_local_5070ti_smoke.json`, `b1_local_frontier.json`, `b1_smoke*.json`, `b1_sparse_smoke.json` — earlier B1 smoke runs at smaller scales / pre-final configurations
- `b3_smoke_ks*.json`, `b3_smoke_mc.json`, `b3_smoke_tsp.json` — earlier B3 per-class smoke runs
- `b3_smoke_pbatched.json` — parallel-batched GPU shader smoke test
- `b1_droplet_smoke.json` — earliest droplet B1 build

If you reproduce a run and your output matches one of the *auxiliary* artefacts rather than the *load-bearing* one, you are likely using an older preset or smaller seed set — check Appendix A of `main.pdf` for the exact commands.

## Negative observations (not stored as JSON)

The paper also documents one explicit negative observation that has *no* JSON because the run did not complete:

- **B1 L = 100 production preset** was OOM-killed on the 62 GB droplet (twice). The reproducible system-log evidence is described in §9 of `main.pdf`; the paper's "within 1% Hartmann" claim is correspondingly conditioned on L ≤ 40 production preset rather than on L = 100. This is filed as a negative observation rather than a missing measurement.
