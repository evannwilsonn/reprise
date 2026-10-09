"""
Download the Mooncake FAST'25 request traces (kvcache-ai/Mooncake, Apache-2.0) into data/raw/
and write a manifest with row counts and SHA-256 hashes.

Each line is one request: arrival time (ms), input and output token counts, and the hashes of its
512-token prefix blocks. Identical hashes mean the KV cache for that prefix could be reused.
No prompt text is included in the traces.

    python ingest/extract.py
"""
from __future__ import annotations

import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
BASE = "https://raw.githubusercontent.com/kvcache-ai/Mooncake/main/FAST25-release/traces"
# request counts published in the release's README; the download must match them
EXPECTED = {"conversation": 12031, "toolagent": 23608, "synthetic": 3993}


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    files = []
    for name, rows in EXPECTED.items():
        path = RAW / f"{name}_trace.jsonl"
        if not path.exists():
            urllib.request.urlretrieve(f"{BASE}/{name}_trace.jsonl", path)
        n = sum(1 for line in open(path, encoding="utf-8") if line.strip())
        if n != rows:
            raise SystemExit(f"{name}: {n} requests, the release says {rows}")
        files.append({"trace": name, "file": path.name, "requests": n, "bytes": path.stat().st_size,
                      "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "source": f"{BASE}/{path.name}"})
        print(f"{name:<13} {n:>6} requests  {path.stat().st_size / 1e6:5.1f} MB")
    (RAW / "_manifest.json").write_text(json.dumps(
        {"extracted_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "files": files}, indent=1))


if __name__ == "__main__":
    main()
