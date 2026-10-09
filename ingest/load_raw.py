"""
Land the traces and the simulator output in DuckDB, unchanged.

  raw_mooncake.requests    one JSON payload per trace request, with the trace name and line number
  raw_sim.requests         one row per request x policy x scenario (from data/sim/*.parquet)
  raw_sim.runs             one row per simulation: tier capacities, blocks written, file hash

    python ingest/load_raw.py
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "warehouse" / "reprise.duckdb"


def main() -> None:
    manifest = json.loads((ROOT / "data" / "raw" / "_manifest.json").read_text())
    runs = json.loads((ROOT / "data" / "sim" / "_runs.json").read_text())
    DB.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(DB))
    for s in ("raw_mooncake", "raw_sim"):
        con.execute(f"create schema if not exists {s}")
    loaded_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    parts = []
    for f in manifest["files"]:
        p = (ROOT / "data" / "raw" / f["file"]).as_posix()
        parts.append(f"""select '{f['trace']}' as trace, row_number() over () - 1 as line_no, json as payload,
                         '{f['file']}' as _source_file from read_json_objects('{p}', format = 'newline_delimited')""")
    con.execute(f"create or replace table raw_mooncake.requests as select *, cast('{loaded_at}' as timestamp) as _loaded_at "
                f"from ({' union all '.join(parts)})")

    for r in runs:   # the simulator's output must be exactly what it recorded
        f = ROOT / "data" / "sim" / r["file"]
        if hashlib.sha256(f.read_bytes()).hexdigest() != r["sha256"]:
            raise SystemExit(f"{r['file']} changed since the simulator wrote it")
    con.execute(f"""create or replace table raw_sim.requests as
        select *, regexp_extract(filename, '[^/]+$') as _source_file, cast('{loaded_at}' as timestamp) as _loaded_at
        from read_parquet('{(ROOT / 'data' / 'sim').as_posix()}/requests__*.parquet', filename = true)""")
    con.execute("alter table raw_sim.requests drop column filename")
    con.execute(f"create or replace table raw_sim.runs as select *, cast('{loaded_at}' as timestamp) as _loaded_at "
                f"from read_json_auto('{(ROOT / 'data' / 'sim' / '_runs.json').as_posix()}')")
    for t in ("raw_mooncake.requests", "raw_sim.requests", "raw_sim.runs"):
        print(f"  {t:<24} {con.execute(f'select count(*) from {t}').fetchone()[0]:>10,} rows")


if __name__ == "__main__":
    main()
