#!/bin/bash
# Pull latest results from droplet, regenerate tables and plots, rebuild PDF.
set -e
cd "$(dirname "$0")"

echo "[1/4] Pulling latest results from droplet..."
for f in b1_gpu_scale.json b1_gpu_scale.log b3_gpu_scale.json b3_gpu_scale.log b1_full.json b3_full.json; do
  scp -q gpu-ramp:/root/isomorphic-engine/paper_dsc3_vs_dwave/results/$f results/ 2>/dev/null || true
done

echo "[2/4] Aggregating tables..."
python aggregate_results.py

echo "[3/4] Building plots..."
python make_plots.py 2>/dev/null || echo "  (plots skipped — matplotlib?)"

echo "[4/4] Compiling PDF..."
pdflatex -interaction=nonstopmode main.tex > /dev/null
pdflatex -interaction=nonstopmode main.tex > /dev/null
echo "Done: main.pdf"
ls -la main.pdf
