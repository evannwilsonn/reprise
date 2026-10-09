"""
Replay the Mooncake request traces through a tiered KV-cache model and record, per request,
where its reusable context was found and what that did to compute and time to first token.

Inputs (all in the repo, nothing hidden in code):
  data/raw/*_trace.jsonl   Mooncake FAST'25 traces: arrival time, token counts, prefix block hashes
  seeds/model_profile.csv  bytes of KV cache per token, FLOPs per token
  seeds/hardware.csv       GPUs per node, nodes, peak FLOPS, utilisation, $/GPU-hour
  seeds/tiers.csv          capacity, read/write bandwidth, latency and $/GB-month for each tier
  seeds/policies.csv       which tiers a policy may use and what it admits below server memory
  seeds/scenarios.csv      tier-size multipliers and model variant

How a request is served:
  - Its prompt is a list of 512-token blocks identified by prefix hashes. Reuse is only possible for
    the longest run of leading blocks that are all still cached somewhere (a prefix cache), because
    each block's KV depends on everything before it.
  - Each cached block is either loaded from its tier (latency + size / bandwidth) or recomputed,
    whichever is faster. Loading is never forced when recomputing would be quicker.
  - Every block after the cached prefix is computed. Prefill FLOPs = 2 * params * tokens plus the
    attention term 2 * layers * hidden * (end^2 - start^2), at the stated utilisation.
  - Time to first token here = load time + prefill time on one node (8-way tensor parallel).
    It leaves out queueing and the decode step, which are the same for every policy.
  - Afterwards all of the request's blocks sit in GPU memory as most-recently used. Tiers are
    exclusive LRU: overflow from one tier moves down to the next the policy allows, or is dropped.
  - The cluster's tiers are treated as one shared pool (Mooncake's design), sized per node x nodes.

    python sim/simulate.py            # every trace x policy x scenario -> data/sim/
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import time
from collections import OrderedDict
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]
BLOCK_TOKENS = 512
TRACES = ["conversation", "toolagent", "synthetic"]
TIER_ORDER = ["hbm", "dram", "ssd", "hdd"]


def seed(name: str) -> list[dict]:
    return list(csv.DictReader(open(ROOT / "seeds" / f"{name}.csv", encoding="utf-8")))


class Tiers:
    """Exclusive LRU tiers. Each block lives in at most one tier."""

    def __init__(self, capacities: dict[str, int], allowed: list[str], reuse_only_below_dram: bool):
        self.allowed = allowed
        self.cap = {t: capacities[t] for t in allowed}
        self.lru = {t: OrderedDict() for t in allowed}
        self.where: dict[int, str] = {}
        self.refs: dict[int, int] = {}
        self.reuse_only = reuse_only_below_dram
        self.writes = {t: 0 for t in TIER_ORDER}      # blocks written into each tier
        self.dropped = 0

    def lookup(self, h: int) -> str | None:
        return self.where.get(h)

    def _place(self, h: int, tier_idx: int) -> None:
        """Put block h in allowed[tier_idx] (or below if not admitted), cascading evictions."""
        while tier_idx < len(self.allowed):
            t = self.allowed[tier_idx]
            if self.reuse_only and t in ("ssd", "hdd") and self.refs.get(h, 0) < 2:
                break                                  # one-off context isn't worth writing to disk
            self.lru[t][h] = None
            self.where[h] = t
            self.writes[t] += 1
            if len(self.lru[t]) <= self.cap[t]:
                return
            h, _ = self.lru[t].popitem(last=False)     # evict the least recently used block
            del self.where[h]
            tier_idx += 1
        self.dropped += 1

    def touch(self, h: int) -> None:
        """Block h was just used: make it most-recent in GPU memory."""
        self.refs[h] = self.refs.get(h, 0) + 1
        cur = self.where.get(h)
        if cur == self.allowed[0]:
            self.lru[cur].move_to_end(h)
            return
        if cur is not None:
            del self.lru[cur][h]
            del self.where[h]
        self._place(h, 0)


def main() -> None:
    t_start = time.time()
    models = {m["model_id"]: m for m in seed("model_profile")}
    hw = {r["item"]: float(r["value"]) for r in seed("hardware")}
    tiers = {t["tier"]: t for t in seed("tiers")}
    policies = seed("policies")
    scenarios = seed("scenarios")
    nodes, gpus = hw["nodes"], hw["gpus_per_node"]
    node_flops = gpus * hw["gpu_peak_tflops"] * 1e12 * hw["prefill_mfu"]

    out_dir = ROOT / "data" / "sim"
    out_dir.mkdir(parents=True, exist_ok=True)
    traces = {}
    for name in TRACES:
        path = ROOT / "data" / "raw" / f"{name}_trace.jsonl"
        traces[name] = [json.loads(line) for line in open(path, encoding="utf-8")]

    run_rows = []
    for sc in scenarios:
        m = models[sc["model_id"]]
        params, layers, hidden = float(m["parameters_b"]) * 1e9, int(m["layers"]), int(m["hidden_size"])
        kv_bytes_token = 2 * layers * int(m["kv_heads"]) * int(m["head_dim"]) * int(m["kv_bytes_per_value"])
        block_gb = kv_bytes_token * BLOCK_TOKENS / 1e9
        caps = {t: int(float(tiers[t]["capacity_gb_per_node"]) * float(sc[f"{t}_scale"]) * nodes / block_gb)
                for t in TIER_ORDER}

        def compute_s(a: int, b: int) -> float:
            """Seconds to prefill tokens a..b-1 given the first a are already in cache."""
            if b <= a:
                return 0.0
            flops = 2 * params * (b - a) + 2 * layers * hidden * (b * b - a * a)
            return flops / node_flops

        def load_s(tier: str) -> float:
            if tier == "hbm":
                return hw["hbm_to_gpu_overhead_ms"] / 1000
            t = tiers[tier]
            bw = float(t["read_gb_s_per_node"]) * (float(sc["hdd_read_scale"]) if tier == "hdd" else 1.0)
            return float(t["access_latency_ms"]) / 1000 + block_gb / bw

        for pol in policies:
            allowed = [t for t in pol["tiers_used"].split(",") if t]
            for tname, reqs in traces.items():
                pcaps = {t: 10**12 for t in TIER_ORDER} if pol["unlimited"] == "true" else caps
                cache = Tiers(pcaps, allowed, pol["admission"] == "reused") if allowed else None
                cols = {k: [] for k in ("request_idx", "timestamp_ms", "input_tokens", "output_tokens", "blocks",
                                        "prefix_blocks_cached", "hits_hbm", "hits_dram", "hits_ssd", "hits_hdd",
                                        "hits_recomputed_instead", "cached_tokens", "computed_tokens",
                                        "load_ms", "compute_ms", "ttft_ms", "gpu_seconds")}
                for i, r in enumerate(reqs):
                    hids, n_in = r["hash_ids"], r["input_length"]
                    hits = {t: 0 for t in TIER_ORDER}
                    skipped = 0
                    load = comp = 0.0
                    cached_tok = 0
                    prefix = 0
                    if cache:
                        for h in hids:
                            if cache.lookup(h) is None:
                                break
                            prefix += 1
                    for j in range(prefix):
                        a, b = j * BLOCK_TOKENS, min(n_in, (j + 1) * BLOCK_TOKENS)
                        tier = cache.lookup(hids[j])
                        ls, cs = load_s(tier), compute_s(a, b)
                        if ls <= cs:
                            load += ls
                            hits[tier] += 1
                            cached_tok += b - a
                        else:                       # cheaper to recompute than to fetch from this tier
                            comp += cs
                            skipped += 1
                    start = min(n_in, prefix * BLOCK_TOKENS)
                    comp += compute_s(start, n_in)
                    if cache:
                        for h in hids:
                            cache.touch(h)
                    vals = (i, r["timestamp"], n_in, r["output_length"], len(hids), prefix, hits["hbm"], hits["dram"],
                            hits["ssd"], hits["hdd"], skipped, cached_tok, n_in - cached_tok,
                            round(load * 1000, 3), round(comp * 1000, 3), round((load + comp) * 1000, 3),
                            round(comp * gpus, 4))
                    for k, v in zip(cols, vals):
                        cols[k].append(v)
                tbl = pa.table({"trace": [tname] * len(reqs), "policy_id": [pol["policy_id"]] * len(reqs),
                                "scenario_id": [sc["scenario_id"]] * len(reqs), **cols})
                fname = out_dir / f"requests__{sc['scenario_id']}__{pol['policy_id']}__{tname}.parquet"
                pq.write_table(tbl, fname)
                run_rows.append({
                    "trace": tname, "policy_id": pol["policy_id"], "scenario_id": sc["scenario_id"],
                    "block_gb": round(block_gb, 6), "kv_bytes_per_token": kv_bytes_token,
                    **{f"capacity_blocks_{t}": (pcaps[t] if t in allowed and pol["unlimited"] != "true" else 0) for t in TIER_ORDER},
                    "unlimited": pol["unlimited"] == "true",
                    **{f"blocks_written_{t}": (cache.writes[t] if cache else 0) for t in TIER_ORDER},
                    **{f"blocks_resident_{t}": (len(cache.lru[t]) if cache and t in allowed else 0) for t in TIER_ORDER},
                    "blocks_dropped": cache.dropped if cache else 0,
                    "requests": len(reqs),
                    "file": fname.name,
                    "sha256": hashlib.sha256(fname.read_bytes()).hexdigest(),
                })
                print(f"{sc['scenario_id']:<10} {pol['policy_id']:<16} {tname:<13} "
                      f"mean TTFT {sum(cols['ttft_ms']) / len(reqs):8.1f} ms  "
                      f"cached {sum(cols['cached_tokens']) / sum(cols['input_tokens']):6.1%}")
    with open(out_dir / "_runs.json", "w", encoding="utf-8") as fh:
        json.dump(run_rows, fh, indent=1)
    print(f"{len(run_rows)} simulations in {time.time() - t_start:.0f}s -> data/sim/")


if __name__ == "__main__":
    main()
