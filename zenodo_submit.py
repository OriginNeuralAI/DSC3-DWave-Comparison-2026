#!/usr/bin/env python3
"""
Submit the DSC-3 vs D-Wave Advantage2 paper to Zenodo.

Uploads main.pdf from this directory, sets metadata, publishes,
records DOI. Adapted from zenodo_submit_all.py.

Usage:
    export ZENODO_TOKEN="..."   # or set inline below
    python zenodo_submit.py
"""

import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

# Read token from env (no token in source code)
ZENODO_TOKEN = os.environ.get("ZENODO_TOKEN", "")
ZENODO_API = "https://zenodo.org/api"

HERE = Path(__file__).parent
PDF_PATH = HERE / "main.pdf"

AUTHORS = [
    {"name": "Daugherty, Bryan W.", "affiliation": "Origin Neural"},
    {"name": "Ward, Gregory",        "affiliation": "Origin Neural"},
    {"name": "Ryan, Shawn",          "affiliation": "Origin Neural"},
]

TITLE = (
    "A Reproducible Classical Reference for D-Wave Advantage2's "
    "2024-2026 Industrial Benchmarks: Ground-state 3D pm J Ising at "
    "N = 10^6 Spins on a $1.57/Hour GPU Droplet, with SHA-256-Pinned "
    "Artefacts and a 'Benchmark Gap' Audit"
)

DESCRIPTION = (
    "On a single $1.57/hour cloud GPU droplet (NVIDIA RTX 6000 Ada, "
    "48 GB / 62 GB system RAM) and a $700 consumer workstation, we "
    "reproduce D-Wave Advantage2's 2024-2026 published industrial "
    "benchmarks on the DSC-3 classical 16-solver ensemble without "
    "consuming any D-Wave Leap QPU minutes. The production-preset "
    "ensemble matches the Hartmann (2001) literature value within 1% "
    "for L<=40 (N<=64,000); a million-spin droplet-feasible ceiling "
    "probe at L=100 (N=10^6) reaches E/E_LB=0.5581. The DSC-3 "
    "ensemble beats matched compute-intensity SA-only by +6-7% on 3D "
    "EA and +0.13-0.37% (sigma<=0.02%) on fully-connected MaxCut up "
    "to N=10,000 (over 2x past Advantage2's 4,400-qubit embedding "
    "ceiling). Cost ratio is 10^4-10^5x cheaper per solve; capex "
    "ratio is 10^6x per machine. The paper identifies a 'Benchmark "
    "Gap' in D-Wave's published references (every reference is "
    "missing at least one of: instance files, per-instance "
    "wall-times, classical baseline pipeline, quantum/classical work "
    "split) and releases all four artefacts for every benchmark it "
    "runs, with SHA-256 manifest. 40 pages, 9 figures, 22 tables, "
    "12 SHA-256-pinned JSON result artefacts."
)

KEYWORDS = [
    "quantum annealing", "D-Wave Advantage2", "Ising model",
    "3D spin glass", "Edwards-Anderson", "Hartmann 2001",
    "ground-state search", "MaxCut", "TSP", "Knapsack",
    "currency arbitrage", "supply chain optimization",
    "drug discovery", "cryptanalysis", "Boneh-Durfee",
    "GNFS", "Proof of Quantum Work", "reverse annealing",
    "Stride hybrid solver", "DSC-3", "Isomorphic Engine",
    "reproducibility", "SHA-256", "benchmark gap",
    "classical optimization", "GPU computing",
    "Daugherty-Ward-Ryan",
]


def api_call(method, endpoint, data=None, binary_data=None, content_type="application/json"):
    url = f"{ZENODO_API}/{endpoint}" if not endpoint.startswith("http") else endpoint
    headers = {"Authorization": f"Bearer {ZENODO_TOKEN}"}
    if binary_data is not None:
        headers["Content-Type"] = "application/octet-stream"
        req = urllib.request.Request(url, data=binary_data, headers=headers, method=method)
    elif data is not None:
        headers["Content-Type"] = content_type
        body = json.dumps(data).encode("utf-8") if isinstance(data, dict) else data
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
    else:
        req = urllib.request.Request(url, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"  HTTP {e.code}: {body[:400]}")
        return {"error": e.code, "body": body}


def main():
    if not ZENODO_TOKEN:
        sys.exit("ZENODO_TOKEN env var is required.")
    if not PDF_PATH.exists():
        sys.exit(f"PDF not found at {PDF_PATH}")

    print(f"Title:  {TITLE}")
    print(f"PDF:    {PDF_PATH} ({PDF_PATH.stat().st_size:,} bytes)")
    print(f"Authors: {', '.join(a['name'] for a in AUTHORS)}")
    print()

    print("Creating Zenodo deposit...")
    dep = api_call("POST", "deposit/depositions", data={})
    if "error" in dep:
        sys.exit("Deposit creation failed.")
    dep_id = dep["id"]
    bucket = dep["links"]["bucket"]
    print(f"  Deposit ID: {dep_id}")

    print("Uploading main.pdf...")
    with open(PDF_PATH, "rb") as f:
        pdf_data = f.read()
    up = api_call("PUT", f"{bucket}/main.pdf", binary_data=pdf_data)
    if "error" in up:
        sys.exit("Upload failed.")
    print(f"  Uploaded: {up.get('size', '?'):,} bytes")

    print("Setting metadata...")
    meta = {
        "metadata": {
            "title": TITLE,
            "upload_type": "publication",
            "publication_type": "article",
            "creators": AUTHORS,
            "description": DESCRIPTION,
            "publication_date": "2026-05-14",
            "access_right": "open",
            "license": "cc-by-4.0",
            "keywords": KEYWORDS,
            "notes": (
                "GitHub repository with all source, results JSON (SHA-256 "
                "manifest in Appendix E), figures, tables, and run scripts: "
                "https://github.com/OriginNeuralAI/DSC3-DWave-Comparison-2026 "
                "(release tag v0.15.1-paper). Live demo: https://dsc3.originneural.ai/"
            ),
            "related_identifiers": [
                {"identifier": "https://github.com/OriginNeuralAI/DSC3-DWave-Comparison-2026",
                 "relation": "isSupplementedBy", "scheme": "url"},
                {"identifier": "https://github.com/OriginNeuralAI/DSC3-DWave-Comparison-2026/releases/tag/v0.15.1-paper",
                 "relation": "isVersionOf", "scheme": "url"},
                {"identifier": "https://dsc3.originneural.ai/",
                 "relation": "isDocumentedBy", "scheme": "url"},
            ],
            "version": "v0.15.1-paper",
        }
    }
    m = api_call("PUT", f"deposit/depositions/{dep_id}", data=meta)
    if "error" in m:
        sys.exit("Metadata set failed.")
    prereserve = m.get("metadata", {}).get("prereserve_doi", {}).get("doi", "?")
    print(f"  DOI prereserved: {prereserve}")

    print("Publishing...")
    pub = api_call("POST", f"deposit/depositions/{dep_id}/actions/publish")
    if "error" in pub:
        sys.exit("Publish failed.")
    doi = pub.get("doi") or pub.get("metadata", {}).get("doi", "?")
    html_url = pub.get("links", {}).get("html") or pub.get("links", {}).get("record_html", "?")
    print()
    print("=" * 60)
    print("PUBLISHED ON ZENODO")
    print("=" * 60)
    print(f"  DOI: {doi}")
    print(f"  URL: {html_url}")
    print(f"  Deposit ID: {dep_id}")

    with open(HERE / "zenodo_submission_record.json", "w") as f:
        json.dump({
            "doi": doi,
            "url": html_url,
            "deposit_id": dep_id,
            "title": TITLE,
            "publication_date": "2026-05-14",
            "version": "v0.15.1-paper",
        }, f, indent=2)
    print(f"  Record saved to {HERE / 'zenodo_submission_record.json'}")


if __name__ == "__main__":
    main()
