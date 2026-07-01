from __future__ import annotations

import json
from pathlib import Path

from ciphertopology.rag_provenance import build_manifest, sha256_bytes, write_manifest


def test_sha256_bytes_is_deterministic() -> None:
    assert sha256_bytes(b"cipher-topology-lab") == sha256_bytes(b"cipher-topology-lab")
    assert sha256_bytes(b"cipher-topology-lab") != sha256_bytes(b"cipher-topology")


def test_build_manifest_hashes_text_chunks(tmp_path: Path) -> None:
    source = tmp_path / "docs" / "source.md"
    source.parent.mkdir()
    source.write_text("alpha\nbeta\ngamma\n", encoding="utf-8")

    manifest = build_manifest(tmp_path, lines_per_chunk=2)

    assert manifest.asset_count == 1
    asset = manifest.assets[0]
    assert asset.path == "docs/source.md"
    assert asset.source_type == "document"
    assert "chunk_hashable" in asset.trust_flags
    assert len(asset.chunks) == 2
    assert asset.chunks[0].start_line == 1
    assert asset.chunks[0].end_line == 2
    assert asset.chunks[1].start_line == 3
    assert asset.chunks[1].end_line == 3


def test_write_manifest_outputs_json(tmp_path: Path) -> None:
    source = tmp_path / "data.geojson"
    source.write_text('{"type":"FeatureCollection","features":[]}', encoding="utf-8")

    manifest = build_manifest(tmp_path)
    out = write_manifest(manifest, tmp_path / "manifest.json")
    payload = json.loads(out.read_text(encoding="utf-8"))

    assert payload["schema_version"] == "rag-provenance-manifest/v0.1"
    assert payload["asset_count"] == 1
    assert payload["assets"][0]["source_type"] == "gis_layer"
    assert "gis_layer_candidate" in payload["assets"][0]["trust_flags"]
