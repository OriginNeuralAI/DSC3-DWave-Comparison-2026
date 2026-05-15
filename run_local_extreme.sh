#!/bin/bash
# Wait for current local frontier to finish, then push to the ceiling using
# the direct-CSR megascale binary.
set -e
cd /c/Users/ripva/Desktop/isomorphic-engine

while [ ! -f paper_dsc3_vs_dwave/results/b1_local_frontier.json ]; do
    sleep 30
done
sleep 10

echo "Frontier done, launching LOCAL MEGASCALE push at $(date)"

# Local 5070 Ti megascale: L = 60, 80, 100, 150 → N from 216K to 3.375M.
# Fast preset (2K steps × 4 restarts) — keeps wall-time bounded at huge N.
# Single seed at the largest size to map the ceiling without wasting hours.
./target/release/examples/dwave_b1_megascale.exe \
    --L 60,80,100,150 --seeds 0 --preset fast --with-gpu --sa-baseline \
    --out paper_dsc3_vs_dwave/results/b1_local_megascale.json \
    > paper_dsc3_vs_dwave/results/b1_local_megascale.log 2>&1

echo "Local megascale done at $(date), pushing LOCAL ULTRA at $(date)"

# ULTRA push — find the actual ceiling on 16 GB VRAM. Try L = 200, 250
# (N = 8M, 15.6M). Either succeeds (we have the ceiling number) or OOMs (we
# have an upper bound). One seed each — this is ceiling exploration.
./target/release/examples/dwave_b1_megascale.exe \
    --L 200,250 --seeds 0 --preset fast --with-gpu --sa-baseline \
    --out paper_dsc3_vs_dwave/results/b1_local_ultra.json \
    > paper_dsc3_vs_dwave/results/b1_local_ultra.log 2>&1

echo "Local ultra done at $(date)"
