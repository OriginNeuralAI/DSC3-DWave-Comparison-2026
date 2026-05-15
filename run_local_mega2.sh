#!/bin/bash
# Wait for current local extreme (L=50,60,80) to finish, then push megascale
# L=100, 150 (N up to 3.4M) using the direct-CSR megascale binary.
set -e
cd /c/Users/ripva/Desktop/isomorphic-engine

while [ ! -f paper_dsc3_vs_dwave/results/b1_local_extreme.json ]; do
    sleep 30
done
sleep 10

echo "Local extreme done, launching MEGASCALE 2 at $(date)"

./target/release/examples/dwave_b1_megascale.exe \
    --L 100,150 --seeds 0,1 --preset fast --with-gpu --sa-baseline \
    --out paper_dsc3_vs_dwave/results/b1_local_mega2.json \
    > paper_dsc3_vs_dwave/results/b1_local_mega2.log 2>&1

echo "Mega2 done at $(date), launching ULTRA ceiling probe..."

# Ceiling probe — single seed at huge N. Some may OOM on 16 GB.
./target/release/examples/dwave_b1_megascale.exe \
    --L 200,250 --seeds 0 --preset fast --with-gpu \
    --out paper_dsc3_vs_dwave/results/b1_local_ceiling.json \
    > paper_dsc3_vs_dwave/results/b1_local_ceiling.log 2>&1

echo "All local ceiling probes done at $(date)"
