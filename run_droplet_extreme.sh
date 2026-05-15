#!/bin/bash
# Wait for B3 batched to finish, then launch DROPLET CEILING push using
# the direct-CSR megascale binary. Stops at N = 27 M spins (L=300) — beyond
# this would take 20+ hours per size, diminishing returns for the paper.
set -e

while [ ! -f /root/isomorphic-engine/paper_dsc3_vs_dwave/results/b3_gpu_batched.json ]; do
    sleep 30
done
sleep 10

echo "B3 batched done, launching DROPLET MEGASCALE B1 push at $(date)"

export LD_LIBRARY_PATH=/usr/local/cuda-12.9/lib64:$LD_LIBRARY_PATH
cd /root/isomorphic-engine

# Stage 1 — multi-seed quality, L=50 .. 150 (N up to 3.4 M).
./target/release/examples/dwave_b1_megascale \
    --L 50,80,100,150 --seeds 0,1,2,3 --preset fast --with-gpu --sa-baseline \
    --out paper_dsc3_vs_dwave/results/b1_droplet_megascale.json \
    > paper_dsc3_vs_dwave/results/b1_droplet_megascale.log 2>&1

echo "Megascale done at $(date), launching DROPLET ULTRA push..."

# Stage 2 — single-seed ceiling probe, L=200, 250, 300 (N up to 27 M spins,
# i.e. 6 130× D-Wave Advantage2's 4 400-qubit max).
./target/release/examples/dwave_b1_megascale \
    --L 200,250,300 --seeds 0 --preset fast --with-gpu --sa-baseline \
    --out paper_dsc3_vs_dwave/results/b1_droplet_ultra.json \
    > paper_dsc3_vs_dwave/results/b1_droplet_ultra.log 2>&1

echo "All droplet ceiling runs complete at $(date)"
