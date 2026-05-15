#!/usr/bin/env python3
"""Generate figures (PDF/PNG) for the DSC-3 vs D-Wave paper.

Reads results/*.json, writes figures/*.pdf for inclusion in main.tex.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).parent
RESULTS = HERE / "results"
FIGURES = HERE / "figures"
FIGURES.mkdir(exist_ok=True)


def load_json(path):
    text = path.read_text()
    text = re.sub(r'(?<![\"\w])inf(?![\w])', '"inf"', text)
    text = re.sub(r'(?<![\"\w])NaN(?![\w])', '"NaN"', text)
    text = re.sub(r'(?<![\"\w])nan(?![\w])', '"NaN"', text)
    return json.loads(text)


def plot_b1_quality_vs_size(b1_paths, out_path):
    """Plot E/E_LB vs N for each variant; horizontal line at Hartmann literature value."""
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    HARTMANN = 1.7863 / 3.0  # convert per-spin to per-bond at 3-bonds-per-spin density
    ax.axhline(HARTMANN, color="black", linestyle="--", linewidth=1.0, label=f"Hartmann 2001: {HARTMANN:.4f}")
    colors = {"production": "#1f77b4", "gpu_scale": "#2ca02c"}
    for label, path in b1_paths.items():
        if not path.exists():
            continue
        data = load_json(path)
        sizes = []
        ratios = []
        sa_ratios = []
        for a in data.get("aggregated", []):
            sizes.append(a["N"])
            ratios.append(abs(a["median_gs_ratio"]))
        ax.plot(sizes, ratios, marker="o", label=f"DSC-3 ({label})", color=colors.get(label, None), linewidth=2)
        # SA-only line if available.
        per_seed = data.get("per_seed", [])
        if any(isinstance(r.get("sa_only_energy"), (int, float)) for r in per_seed):
            groups = defaultdict(list)
            for r in per_seed:
                if isinstance(r.get("sa_only_energy"), (int, float)) and r["lower_bound"] != 0:
                    groups[r["N"]].append(abs(r["sa_only_energy"] / r["lower_bound"]))
            sa_sizes = sorted(groups.keys())
            sa_meds = [sorted(groups[n])[len(groups[n]) // 2] for n in sa_sizes]
            ax.plot(sa_sizes, sa_meds, marker="s", linestyle=":", label=f"SA-only ({label})", color=colors.get(label, None), alpha=0.6)
    ax.set_xscale("log")
    ax.set_xlabel(r"$N$ spins")
    ax.set_ylabel(r"$|E|/|E_{\rm LB}|$")
    ax.set_title("B1: 3D $\\pm J$ Ising spin glass — DSC-3 vs SA-only vs Hartmann literature")
    ax.legend(loc="best", fontsize=9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path)
    print(f"[ok] wrote {out_path}")


def plot_b1_wall_vs_size(b1_paths, out_path):
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    colors = {"production": "#1f77b4", "gpu_scale": "#2ca02c"}
    for label, path in b1_paths.items():
        if not path.exists():
            continue
        data = load_json(path)
        sizes = []
        walls = []
        for a in data.get("aggregated", []):
            sizes.append(a["N"])
            walls.append(a["median_wall_s"])
        ax.plot(sizes, walls, marker="o", label=f"DSC-3 ({label})", color=colors.get(label, None), linewidth=2)
    # D-Wave reference horizontal line: ~120s for N~5000 (Science 2025 sampling claim).
    ax.axhline(120, color="red", linestyle="-.", linewidth=1.5, label="D-Wave Adv2 sampling (~2 min @ N~5000)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"$N$ spins")
    ax.set_ylabel("median wall (s)")
    ax.set_title("B1: time-to-ground-state scaling on DSC-3 (Ada-6000 droplet)")
    ax.legend(loc="best", fontsize=9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path)
    print(f"[ok] wrote {out_path}")


def plot_b3_maxcut_vs_sa(b3_paths, out_path):
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    for label, path in b3_paths.items():
        if not path.exists():
            continue
        data = load_json(path)
        groups = defaultdict(list)
        for r in data.get("per_instance", []):
            if r["problem"] == "MaxCut":
                groups[r["n_vars"]].append(r["gap_pct"])
        sizes = sorted(groups.keys())
        meds = [sorted(g)[len(g) // 2] for g in (groups[n] for n in sizes)]
        ax.plot(sizes, meds, marker="o", label=f"DSC-3 ({label})", linewidth=2)
    ax.axhline(0, color="black", linestyle="--", linewidth=0.7, label="SA-only baseline")
    ax.set_xscale("log")
    ax.set_xlabel(r"$N$ vertices")
    ax.set_ylabel("DSC-3 cut % advantage over SA-only")
    ax.set_title("B3 MaxCut: DSC-3 ensemble vs strong-classical SA-alone baseline")
    ax.legend(loc="best", fontsize=9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path)
    print(f"[ok] wrote {out_path}")


def plot_hardware_generality(droplet_paths, local_paths, out_path):
    """Side-by-side: same engine, two GPUs (Ada-6000 cloud vs 5070 Ti consumer)."""
    fig, (ax_q, ax_w) = plt.subplots(1, 2, figsize=(11, 4.2))
    droplet_points = {}
    for p in droplet_paths:
        if not p.exists(): continue
        d = load_json(p)
        for a in d.get("aggregated", []):
            droplet_points[a["L"]] = (a["median_gs_ratio"], a["median_wall_s"])
    local_points = {}
    for p in local_paths:
        if not p.exists(): continue
        d = load_json(p)
        for a in d.get("aggregated", []):
            local_points[a["L"]] = (a["median_gs_ratio"], a["median_wall_s"])
    ls_local = sorted(local_points.keys())
    ls_droplet = sorted(droplet_points.keys())
    # quality
    ax_q.plot(ls_droplet, [droplet_points[L][0] for L in ls_droplet], marker="o", label="Ada-6000 droplet", color="#2ca02c", linewidth=2)
    ax_q.plot(ls_local, [local_points[L][0] for L in ls_local], marker="s", label="5070 Ti workstation", color="#1f77b4", linewidth=2)
    ax_q.axhline(1.7863 / 3.0, color="black", ls="--", lw=0.8, label="Hartmann (2001)")
    ax_q.set_xlabel("$L$ (linear size)")
    ax_q.set_ylabel(r"$|E|/|E_{\rm LB}|$")
    ax_q.set_title("Quality: same engine, two GPUs")
    ax_q.legend(fontsize=8)
    ax_q.grid(alpha=0.3)
    # wall
    ax_w.plot(ls_droplet, [droplet_points[L][1] for L in ls_droplet], marker="o", label="Ada-6000 droplet", color="#2ca02c", linewidth=2)
    ax_w.plot(ls_local, [local_points[L][1] for L in ls_local], marker="s", label="5070 Ti workstation", color="#1f77b4", linewidth=2)
    ax_w.set_xlabel("$L$ (linear size)")
    ax_w.set_ylabel("median wall (s)")
    ax_w.set_yscale("log")
    ax_w.set_title("Wall-time: same engine, two GPUs")
    ax_w.legend(fontsize=8)
    ax_w.grid(alpha=0.3, which="both")
    fig.tight_layout()
    fig.savefig(out_path)
    print(f"[ok] wrote {out_path}")


def plot_maxcut_crossover(b3_batched_path, out_path):
    """DSC-3 ensemble advantage over SA-only as N grows."""
    if not b3_batched_path.exists():
        print(f"[skip] {b3_batched_path}")
        return
    d = load_json(b3_batched_path)
    rows = [r for r in d.get("per_instance", []) if r["problem"] == "MaxCut" and isinstance(r.get("gap_pct"), (int, float))]
    by_n = defaultdict(list)
    for r in rows:
        by_n[r["n_vars"]].append(r["gap_pct"])
    sizes = sorted(by_n.keys())
    meds = [sorted(by_n[n])[len(by_n[n]) // 2] for n in sizes]
    fig, ax = plt.subplots(figsize=(7.5, 4.0))
    ax.plot(sizes, meds, marker="o", linewidth=2, color="#d62728")
    ax.axhline(0, ls="--", color="black", lw=0.8, label="SA-only baseline")
    ax.set_xscale("log")
    ax.set_xlabel(r"$N$ vertices (MaxCut)")
    ax.set_ylabel("DSC-3 ensemble vs.\\ SA-only ($\\Delta$\\%)")
    ax.set_title("B3 MaxCut: ensemble advantage grows with problem size")
    ax.grid(alpha=0.3, which="both")
    ax.legend(fontsize=9)
    fig.tight_layout()
    fig.savefig(out_path)
    print(f"[ok] wrote {out_path}")


def plot_ceiling_push(droplet_paths, local_paths, out_path):
    """Wall time vs N for all ceiling probes, log-log."""
    fig, ax = plt.subplots(figsize=(8, 4.4))
    droplet_pts = []
    for p, label in droplet_paths:
        if not p.exists(): continue
        d = load_json(p)
        for a in d.get("aggregated", []):
            droplet_pts.append((a["N"], a["median_wall_s"]))
    local_pts = []
    for p, label in local_paths:
        if not p.exists(): continue
        d = load_json(p)
        for a in d.get("aggregated", []):
            local_pts.append((a["N"], a["median_wall_s"]))
    if droplet_pts:
        droplet_pts.sort()
        ax.plot([p[0] for p in droplet_pts], [p[1] for p in droplet_pts], marker="o", label="Ada-6000 droplet", color="#2ca02c", linewidth=2)
    if local_pts:
        local_pts.sort()
        ax.plot([p[0] for p in local_pts], [p[1] for p in local_pts], marker="s", label="5070 Ti workstation", color="#1f77b4", linewidth=2)
    ax.axvline(4400, color="red", ls=":", lw=1.5, label="D-Wave Advantage2 max qubits (4,400)")
    ax.axhline(120, color="red", ls="-.", lw=1.0, label="D-Wave Science 2025 sampling time (~120 s)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"$N$ spins")
    ax.set_ylabel("median wall (s)")
    ax.set_title("DSC-3 ceiling push: wall-time scaling well past D-Wave's embedding limit")
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(alpha=0.3, which="both")
    fig.tight_layout()
    fig.savefig(out_path)
    print(f"[ok] wrote {out_path}")


def plot_b3_beyond_embedding(out_path):
    """B3 MaxCut Delta-vs-SA at N=500..10000, with N>4400 marked as
    past D-Wave Advantage2's embedding ceiling."""
    # Hand-curated from b3_gpu_batched.json (N<=2000) and the new
    # b3_maxcut_xlarge.json medians.
    n_values = [500, 1000, 2000, 5000, 5000, 10000, 10000]
    densities = [0.5, 0.5, 0.5, 0.30, 0.50, 0.30, 0.50]
    delta_pct = [0.21, 0.27, 0.37, 0.27, 0.19, 0.20, 0.13]
    sigma_pct = [0.0, 0.0, 0.0, 0.017, 0.010, 0.015, 0.010]
    fig, ax = plt.subplots(figsize=(7.8, 4.4))
    by_d = defaultdict(list)
    for n, d, dlt, sg in zip(n_values, densities, delta_pct, sigma_pct):
        by_d[d].append((n, dlt, sg))
    colors = {0.30: "#1f77b4", 0.50: "#d62728"}
    for d, points in by_d.items():
        points.sort()
        ns = [p[0] for p in points]
        dlts = [p[1] for p in points]
        sgs = [p[2] for p in points]
        ax.errorbar(ns, dlts, yerr=sgs, marker="o", capsize=3, linewidth=2,
                    color=colors[d], label=f"density $d={d}$")
    ax.axhline(0, color="black", linestyle="--", linewidth=0.8, label="SA-only baseline")
    ax.axvline(4400, color="gray", linestyle=":", linewidth=1.2)
    ax.text(4400, ax.get_ylim()[1] * 0.92,
            " D-Wave Advantage2\n 4{,}400-qubit ceiling",
            fontsize=8, color="gray", verticalalignment="top")
    ax.set_xscale("log")
    ax.set_xlabel(r"$N$ vertices (Erd\H{o}s--R\'enyi fully-connected MaxCut)")
    ax.set_ylabel(r"DSC-3 cut $\Delta$ vs SA-only (\%)")
    ax.set_title("B3 MaxCut crossover persists past the D-Wave embedding ceiling")
    ax.legend(loc="lower left", fontsize=9)
    ax.grid(True, alpha=0.3, which="both")
    fig.tight_layout()
    fig.savefig(out_path)
    print(f"[ok] wrote {out_path}")


def plot_cost_comparison(out_path):
    """Log-scale bar chart: capex per machine + per-solve + power + energy."""
    metrics = ["Capex per machine (\\$)",
               "Cost / solve (\\$, B1 N=1{,}728)",
               "Power continuous (kW)",
               "Energy / solve (Wh)"]
    dwave = [12_500_000, 1.30, 12.5, 200]
    dsc3  = [5_000,      0.024, 0.30, 4.6]
    import numpy as np
    x = np.arange(len(metrics))
    width = 0.36
    fig, ax = plt.subplots(figsize=(8.5, 4.6))
    bars1 = ax.bar(x - width/2, dwave, width, label="D-Wave Advantage2", color="#d62728")
    bars2 = ax.bar(x + width/2, dsc3,  width, label="DSC-3 droplet/workstation", color="#1f77b4")
    ax.set_yscale("log")
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=9, rotation=12)
    ax.set_ylabel("(log scale)")
    ax.set_title("Cost / power / energy: D-Wave Advantage2 vs DSC-3")
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(True, alpha=0.3, axis="y", which="both")
    for bars in (bars1, bars2):
        for b in bars:
            ax.text(b.get_x() + b.get_width()/2, b.get_height(),
                    f"{b.get_height():g}", ha="center", va="bottom", fontsize=7)
    fig.tight_layout()
    fig.savefig(out_path)
    print(f"[ok] wrote {out_path}")


def plot_benchmark_gap_heatmap(out_path):
    """Heatmap of the Benchmark Gap table: D-Wave 'missing' vs DSC-3 'released'."""
    import numpy as np
    benchmarks = ["B1 Ising", "B2 FX", "B3 Stride", "B4 SCM", "B5d Drug", "B5p PoQW", "B6 Crypto"]
    axes = ["Instances", "Per-inst wall", "Baseline pipe", "Q/C split"]
    # 0 = absent, 1 = present (or N/A counted as present for completeness)
    dwave = np.array([
        [0, 1, 0, 0],  # B1 (Zephyr-embedded only; sampling wall reported)
        [0, 0, 0, 0],  # B2
        [0, 0, 0, 0],  # B3
        [0, 0, 0, 0],  # B4
        [0, 0, 0, 0],  # B5d
        [0, 0, 0, 0],  # B5p (no benchmark)
        [0, 0, 0, 0],  # B6 (no publication)
    ])
    dsc3 = np.ones_like(dwave)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.5, 3.8))
    for ax, mat, title in [(ax1, dwave, "D-Wave publishes"), (ax2, dsc3, "DSC-3 publishes")]:
        ax.imshow(mat, cmap="RdYlGn", vmin=0, vmax=1, aspect="auto")
        ax.set_xticks(range(len(axes)))
        ax.set_xticklabels(axes, rotation=20, fontsize=9)
        ax.set_yticks(range(len(benchmarks)))
        ax.set_yticklabels(benchmarks, fontsize=9)
        ax.set_title(title)
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                ax.text(j, i, "✓" if mat[i, j] else "×",
                        ha="center", va="center",
                        color="white" if mat[i, j] else "black",
                        fontsize=12, fontweight="bold")
    fig.suptitle("The Benchmark Gap: artefacts released, per benchmark and per axis", fontsize=10)
    fig.tight_layout()
    fig.savefig(out_path)
    print(f"[ok] wrote {out_path}")


if __name__ == "__main__":
    b1_paths = {
        "production (Ada-6000)": RESULTS / "b1_full.json",
        "gpu_scale (Ada-6000)": RESULTS / "b1_gpu_scale.json",
        "local (5070 Ti)": RESULTS / "b1_local_5070ti.json",
    }
    b3_paths = {
        "quality": RESULTS / "b3_full.json",
        "gpu_batched": RESULTS / "b3_gpu_batched.json",
    }
    plot_b1_quality_vs_size(b1_paths, FIGURES / "b1_quality.pdf")
    plot_b1_wall_vs_size(b1_paths, FIGURES / "b1_walltime.pdf")
    plot_b3_maxcut_vs_sa(b3_paths, FIGURES / "b3_maxcut.pdf")

    plot_hardware_generality(
        droplet_paths=[RESULTS / "b1_full.json", RESULTS / "b1_gpu_scale.json"],
        local_paths=[RESULTS / "b1_local_5070ti.json", RESULTS / "b1_local_frontier.json"],
        out_path=FIGURES / "hardware_generality.pdf",
    )
    plot_maxcut_crossover(RESULTS / "b3_gpu_batched.json", FIGURES / "maxcut_crossover.pdf")
    plot_ceiling_push(
        droplet_paths=[
            (RESULTS / "b1_full.json", "droplet_full"),
            (RESULTS / "b1_gpu_scale.json", "droplet_gpu"),
            (RESULTS / "b1_droplet_megascale.json", "droplet_mega"),
            (RESULTS / "b1_droplet_ultra.json", "droplet_ultra"),
        ],
        local_paths=[
            (RESULTS / "b1_local_5070ti.json", "local"),
            (RESULTS / "b1_local_frontier.json", "local_frontier"),
            (RESULTS / "b1_local_extreme.json", "local_extreme"),
            (RESULTS / "b1_local_mega2.json", "local_mega2"),
            (RESULTS / "b1_local_ceiling.json", "local_ceiling"),
        ],
        out_path=FIGURES / "ceiling_push.pdf",
    )
    plot_b3_beyond_embedding(FIGURES / "b3_beyond_embedding.pdf")
    plot_cost_comparison(FIGURES / "cost_comparison.pdf")
    plot_benchmark_gap_heatmap(FIGURES / "benchmark_gap.pdf")
