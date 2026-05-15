#!/bin/bash
set -e

# Wait for B1-GPU-scale (running L=14,16,18,20) to finish.
while pgrep -f "dwave_b1_tfim_spin_glass --L 14,16,18,20" > /dev/null; do
  sleep 30
done

echo "B1 done, starting B3-GPU-batched at $(date)"
export LD_LIBRARY_PATH=/usr/local/cuda-12.9/lib64:$LD_LIBRARY_PATH
cd /root/isomorphic-engine

# B3 with batched GPU (4 chains + 4 Z2 complement evals per restart).
# Smaller batch (4 vs 8) to keep wall-times reasonable; we still get 4*16*2 = 128
# effective explorations per instance vs 16 for the single-chain GPU wrapper.
./target/release/examples/dwave_b3_stride \
  --seeds 0,1,2,3 --preset quality --with-gpu --gpu-batch 4 \
  --tsp-sizes 8,10,12,16,20,25,30 \
  --maxcut-sizes 20,40,60,100,200,500,1000,2000 \
  --knapsack-sizes 10,20,30,40,50 \
  --out paper_dsc3_vs_dwave/results/b3_gpu_batched.json \
  > paper_dsc3_vs_dwave/results/b3_gpu_batched.log 2>&1

echo "All scale runs done at $(date)"
