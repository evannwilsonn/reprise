"""
Export the reporting marts to dashboard/data.json.

    python dashboard/export_data.py                    # local DuckDB
    python dashboard/export_data.py --target snowflake
"""
from __future__ import annotations

import argparse
import json
import os
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLES = {
    "comparison": "select * from reporting.rpt_policy_comparison order by scenario_id, trace, policy_order",
    "bands": "select * from reporting.rpt_hit_bands order by scenario_id, policy_id, trace, band_floor",
    "warmup": "select * from reporting.rpt_warmup where policy_id in ('recompute','gpu_only','gpu_dram','all_tiers') "
              "order by scenario_id, policy_id, trace, minute",
    "tiers": "select * from reporting.rpt_tier_economics order by model_id, tier_order",
    "scenarios": "select * from reference.scenarios",
    "policies": "select * from reference.policies order by policy_order",
    "traces": "select * from intermediate.int_trace_spans order by trace",
    "hardware": "select * from reference.hardware",
}


def clean(v):
    if isinstance(v, (datetime, date)):
        return v.isoformat()
    if isinstance(v, Decimal):
        return float(v)
    if isinstance(v, float):
        return round(v, 5)
    return v


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", choices=["duckdb", "snowflake"], default="duckdb")
    args = ap.parse_args()
    if args.target == "snowflake":
        import snowflake.connector
        con = snowflake.connector.connect(
            account=os.environ["SNOWFLAKE_ACCOUNT"], user=os.environ["SNOWFLAKE_USER"],
            private_key_file=os.environ["SNOWFLAKE_PRIVATE_KEY_PATH"], role=os.environ.get("SNOWFLAKE_ROLE", "SYSADMIN"),
            warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE", "PORTFOLIO_WH"), database="REPRISE")

        def run(sql):
            cur = con.cursor()
            cur.execute(sql)
            return [c[0].lower() for c in cur.description], cur.fetchall()
    else:
        import duckdb
        con = duckdb.connect(str(ROOT / "warehouse" / "reprise.duckdb"), read_only=True)

        def run(sql):
            cur = con.execute(sql)
            return [c[0] for c in cur.description], cur.fetchall()
    import yaml
    vars_ = yaml.safe_load((ROOT / "dbt_project.yml").read_text())["vars"]
    results = ROOT / "target" / "run_results.json"
    tests = sum(1 for r in json.loads(results.read_text())["results"] if r["unique_id"].startswith("test.")) if results.exists() else None
    out = {"generated": datetime.now().isoformat(timespec="seconds"), "source": args.target,
           "manifest": json.loads((ROOT / "data" / "raw" / "_manifest.json").read_text()),
           "meta": {"amortisation_months": vars_["amortisation_months"], "dbt_tests": tests}}
    for key, sql in TABLES.items():
        cols, rows = run(sql)
        out[key] = [{c: clean(v) for c, v in zip(cols, r)} for r in rows]
    path = ROOT / "dashboard" / "data.json"
    path.write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {path.relative_to(ROOT)} ({path.stat().st_size // 1024} KB, {len(out['comparison'])} simulations) "
          f"from {args.target}")


if __name__ == "__main__":
    main()
