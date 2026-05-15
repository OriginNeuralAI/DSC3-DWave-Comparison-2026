#!/usr/bin/env python3
"""Aggregate B1 and B3 JSON results into LaTeX tables for the paper.

Usage:
  python aggregate_results.py        # reads results/*.json, writes tables/*.tex
"""
import json
import os
import re
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent
RESULTS = HERE / "results"
TABLES = HERE / "tables"
TABLES.mkdir(exist_ok=True)


def load_json(path):
    text = path.read_text()
    text = re.sub(r'(?<![\"\w])inf(?![\w])', '"inf"', text)
    text = re.sub(r'(?<![\"\w])NaN(?![\w])', '"NaN"', text)
    text = re.sub(r'(?<![\"\w])nan(?![\w])', '"NaN"', text)
    return json.loads(text)


def median(xs):
    xs = sorted(x for x in xs if isinstance(x, (int, float)))
    return xs[len(xs) // 2] if xs else float("nan")


def aggregate_b1(json_path, label):
    if not json_path.exists():
        print(f"[skip] {json_path} not found")
        return
    data = load_json(json_path)
    rows = []
    for a in data.get("aggregated", []):
        rows.append(
            (a["L"], a["N"], a["lower_bound"], a["median_energy"], a["std_energy"],
             a["best_energy"], a["worst_energy"], a["median_wall_s"], a["mean_wall_s"], a["median_gs_ratio"])
        )
    lines = [
        r"\begin{tabular}{rrrrrrrrr}",
        r"\toprule",
        r"$L$ & $N$ & edges & median $E$ & $\sigma_E$ & best & worst & median wall (s) & $E/E_{\rm LB}$ \\",
        r"\midrule",
    ]
    for (L, N, lb, me, se, be, we, mw, _aw, mgr) in rows:
        lines.append(
            f"{L} & {N} & {3 * N} & {me:.1f} & {se:.1f} & {be:.1f} & {we:.1f} & {mw:.2f} & {mgr:.4f} \\\\"
        )
    lines += [r"\bottomrule", r"\end{tabular}"]
    out = TABLES / f"b1_{label}.tex"
    out.write_text("\n".join(lines) + "\n")
    print(f"[ok] wrote {out}")

    # SA-alone comparison (if present in per_seed).
    per_seed = data.get("per_seed", [])
    if any(r.get("sa_only_energy") not in (None, "inf", "NaN") for r in per_seed):
        groups = defaultdict(list)
        for r in per_seed:
            groups[r["L"]].append(r)
        lines = [
            r"\begin{tabular}{rrrrrrr}",
            r"\toprule",
            r"$L$ & $N$ & median DSC-3 $E$ & median SA-only $E$ & median $\Delta\%$ & DSC-3 wall (s) & SA wall (s) \\",
            r"\midrule",
        ]
        for L in sorted(groups.keys()):
            rs = groups[L]
            dsc3_es = [r["energy"] for r in rs]
            sa_es = [r.get("sa_only_energy") for r in rs if isinstance(r.get("sa_only_energy"), (int, float))]
            dsc3_walls = [r["wall_s"] for r in rs]
            sa_walls = [r.get("sa_only_wall_s") for r in rs if isinstance(r.get("sa_only_wall_s"), (int, float))]
            me_d = median(dsc3_es)
            me_s = median(sa_es) if sa_es else float("nan")
            delta = (me_s - me_d) / abs(me_d) * 100 if me_d not in (0, float("nan")) else float("nan")
            mw_d = median(dsc3_walls)
            mw_s = median(sa_walls) if sa_walls else float("nan")
            lines.append(
                f"{L} & {rs[0]['N']} & {me_d:.1f} & {me_s:.1f} & {delta:+.2f}\\% & {mw_d:.2f} & {mw_s:.4f} \\\\"
            )
        lines += [r"\bottomrule", r"\end{tabular}"]
        out2 = TABLES / f"b1_{label}_vs_sa.tex"
        out2.write_text("\n".join(lines) + "\n")
        print(f"[ok] wrote {out2}")


def aggregate_b3(json_path, label):
    if not json_path.exists():
        print(f"[skip] {json_path} not found")
        return
    data = load_json(json_path)
    rows = data.get("per_instance", [])

    # Group by (problem, n_vars).
    groups = defaultdict(list)
    for r in rows:
        groups[(r["problem"], r["n_vars"])].append(r)

    for problem in ["TSP", "MaxCut", "Knapsack"]:
        lines = [
            r"\begin{tabular}{rrrrrr}",
            r"\toprule",
        ]
        if problem == "TSP":
            lines.append(r"$n$ & $n^2$ vars & median DSC-3 & median NN+2opt & median gap & median wall (s) \\")
        elif problem == "MaxCut":
            lines.append(r"$N$ & median DSC-3 & median SA-only & median $\Delta$\% & median wall (s) & valid \\")
        else:  # Knapsack
            lines.append(r"$n$ items & median DSC-3 & DP optimum & median gap\% vs opt & median wall (s) & valid \\")
        lines.append(r"\midrule")

        keys = sorted([k for k in groups if k[0] == problem], key=lambda k: k[1])
        for key in keys:
            rs = groups[key]
            walls = [r["wall_s"] for r in rs]
            gaps = [r["gap_pct"] for r in rs if isinstance(r["gap_pct"], (int, float))]
            valids = sum(1 for r in rs if r["valid"])
            mw = median(walls)
            mg = median(gaps) if gaps else float("nan")

            dsc3s = [r.get("dsc3_polished", r.get("dsc3_objective_polished", 0.0)) if problem == "Knapsack" else r.get("dsc3", r.get("dsc3_objective", 0.0)) for r in rs]
            base = [r.get("baseline", r.get("baseline_objective", 0.0)) for r in rs]
            md = median(dsc3s)
            mb = median(base)

            if problem == "TSP":
                n = int((key[1]) ** 0.5)
                lines.append(f"{n} & {key[1]} & {md:.3f} & {mb:.3f} & {mg:+.2f}\\% & {mw:.2f} \\\\")
            elif problem == "MaxCut":
                lines.append(f"{key[1]} & {md:.0f} & {mb:.0f} & {mg:+.2f}\\% & {mw:.2f} & {valids}/{len(rs)} \\\\")
            else:
                # n_items unrelated to n_vars (n_vars includes slack); derive from instance_id
                m = re.match(r"n(\d+)_", rs[0].get("instance_id", rs[0].get("id", "")))
                n_items = int(m.group(1)) if m else key[1]
                lines.append(f"{n_items} & {md:.2f} & {mb:.2f} & {mg:+.2f}\\% & {mw:.2f} & {valids}/{len(rs)} \\\\")

        lines += [r"\bottomrule", r"\end{tabular}"]
        out = TABLES / f"b3_{label}_{problem.lower()}.tex"
        out.write_text("\n".join(lines) + "\n")
        print(f"[ok] wrote {out}")


def aggregate_ceiling(b1_paths, out_path):
    """Combine multiple B1 result files into a single ceiling table."""
    all_rows = []
    for label, path in b1_paths.items():
        if not path.exists():
            continue
        data = load_json(path)
        for a in data.get("aggregated", []):
            all_rows.append((a["L"], a["N"], a["median_energy"], a["median_gs_ratio"], a["median_wall_s"], label))
    all_rows.sort(key=lambda r: r[1])  # sort by N
    lines = [
        r"\begin{tabular}{rrrrrl}",
        r"\toprule",
        r"$L$ & $N$ & median $E$ & $E/E_{\rm LB}$ & wall (s) & source \\",
        r"\midrule",
    ]
    for (L, N, me, mgr, mw, label) in all_rows:
        lines.append(f"{L} & {N:,} & {me:,.0f} & {mgr:.4f} & {mw:.1f} & {label} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    out_path.write_text("\n".join(lines) + "\n")
    print(f"[ok] wrote {out_path}")


if __name__ == "__main__":
    aggregate_b1(RESULTS / "b1_full.json", "production")
    aggregate_b1(RESULTS / "b1_gpu_scale.json", "gpu_scale")
    aggregate_b1(RESULTS / "b1_local_5070ti.json", "local_5070ti")
    aggregate_b1(RESULTS / "b1_local_frontier.json", "local_frontier")
    aggregate_b1(RESULTS / "b1_local_extreme.json", "local_extreme")
    aggregate_b1(RESULTS / "b1_local_mega2.json", "local_mega2")
    aggregate_b1(RESULTS / "b1_local_ceiling.json", "local_ceiling")
    aggregate_b1(RESULTS / "b1_droplet_megascale.json", "droplet_megascale")
    aggregate_b1(RESULTS / "b1_droplet_ultra.json", "droplet_ultra")
    aggregate_b3(RESULTS / "b3_full.json", "quality")
    aggregate_b3(RESULTS / "b3_gpu_batched.json", "gpu_batched")
    aggregate_ceiling({
        "droplet_full": RESULTS / "b1_full.json",
        "droplet_gpu_scale": RESULTS / "b1_gpu_scale.json",
        "droplet_megascale": RESULTS / "b1_droplet_megascale.json",
        "droplet_ultra": RESULTS / "b1_droplet_ultra.json",
        "local_5070ti": RESULTS / "b1_local_5070ti.json",
        "local_frontier": RESULTS / "b1_local_frontier.json",
        "local_extreme": RESULTS / "b1_local_extreme.json",
        "local_mega2": RESULTS / "b1_local_mega2.json",
        "local_ceiling": RESULTS / "b1_local_ceiling.json",
    }, TABLES / "b1_ceiling_combined.tex")
    print("Done.")
