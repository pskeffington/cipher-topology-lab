from __future__ import annotations

import argparse
import csv
from pathlib import Path

from ciphertopology.generators import StreamSpec, generate_stream
from ciphertopology.utils import ensure_dirs, read_json, sha256_file


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    config = read_json(args.config)
    raw_dir = Path("data/raw")
    ensure_dirs(raw_dir, "results/logs")

    manifest_path = Path("data/raw/stream_manifest.csv")
    rows = []

    for condition in config["conditions"]:
        for replicate in range(config["replicates"]):
            spec = StreamSpec(condition, replicate, config["master_seed"], config["stream_bytes"])
            stream, meta = generate_stream(spec)
            stream_id = f"{condition}_r{replicate:03d}"
            out_path = raw_dir / f"{stream_id}.bin"
            out_path.write_bytes(stream)
            rows.append({
                "stream_id": stream_id,
                "condition": condition,
                "replicate": replicate,
                "master_seed": config["master_seed"],
                "bytes": len(stream),
                "path": str(out_path),
                "sha256": sha256_file(out_path),
                **meta,
            })

    fieldnames = sorted(set().union(*(row.keys() for row in rows)))
    with manifest_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} streams to {raw_dir}")
    print(f"Wrote manifest to {manifest_path}")


if __name__ == "__main__":
    main()
