# Contributing

This repository accompanies a published research paper. The kinds of contributions we welcome and how to file them:

## 1. Falsification attempts (most welcome)

The paper makes five specific, falsifiable claims (F1–F5 in §15.5 of `main.pdf`). If you've tried to falsify one — *especially if you succeeded* — please file a [Falsification attempt issue](https://github.com/OriginNeuralAI/DSC3-DWave-Comparison-2026/issues/new?template=falsification-attempt.yml). The issue template asks for the exact command, hardware environment, observed band, and ideally the result JSON with its SHA-256.

Our response policy: we will reproduce your run on our droplet within 7 days, acknowledge the result publicly, and if confirmed, mark the relevant claim as falsified in the next paper revision.

## 2. Reproduction failures

If you followed [Appendix A of the paper](main.pdf) or one of the `run_*.sh` scripts and got something other than what's in `results/`, please file a [Reproduction failure issue](https://github.com/OriginNeuralAI/DSC3-DWave-Comparison-2026/issues/new?template=reproduction-failure.yml). Reproduction failures are debugging events: usually a hardware-environment mismatch, occasionally an engine bug, very rarely a paper-documentation gap. Any of those is worth knowing about.

## 3. Factual corrections

For typos, miscited references, off-by-one mistakes, or numerical errors in the paper text, file a [Factual correction issue](https://github.com/OriginNeuralAI/DSC3-DWave-Comparison-2026/issues/new?template=factual-correction.yml). PRs are welcome but the issue template is the lower-friction path.

## 4. New benchmarks

If you'd like to add a new D-Wave benchmark we did not cover (e.g., the four remaining SCM verticals, reverse annealing experiments, or a more recent D-Wave publication), please open a discussion issue first. The criteria for inclusion match what's in the paper's Reproduction Fidelity Map (Table 5): the benchmark needs (a) a citable D-Wave reference, (b) a reproducible classical baseline, (c) measured DSC-3 results with σ across n ≥ 3 seeds.

## What we will *not* accept

- Changes to the paper's central claims without supporting data (use a falsification issue instead).
- Renaming, restructuring, or restyling the paper for its own sake.
- Adding self-citations of unrelated work.
- Speculation about D-Wave's roadmap not anchored to a cited public statement.

## License

By contributing, you agree your contribution is licensed under CC-BY-4.0 (same as the paper). See `LICENSE`.
