from __future__ import annotations

from ciphertopology.pilot_report import build_pilot_report_markdown


def test_build_pilot_report_includes_core_sections() -> None:
    manifest = {
        "asset_count": 2,
        "total_bytes": 100,
        "assets": [
            {"path": "docs/source.md", "source_type": "document", "trust_flags": ["chunk_hashable"]},
            {"path": "gis/water.geojson", "source_type": "gis_layer", "trust_flags": ["gis_layer_candidate"]},
        ],
    }
    verification = {
        "answer_id": "answer-1",
        "status": "approved",
        "citation_count": 1,
        "approved_count": 1,
        "rejected_count": 0,
    }
    gis_profile = {
        "gis_candidate_count": 1,
        "covered_sector_count": 1,
        "missing_sector_count": 11,
    }

    report = build_pilot_report_markdown(
        manifest=manifest,
        verification=verification,
        gis_profile=gis_profile,
        client_name="Example Town",
    )

    assert "Example Town" in report
    assert "Source provenance summary" in report
    assert "RAG answer verification summary" in report
    assert "GIS/infrastructure profile summary" in report
    assert "Recommended remediation backlog" in report
    assert "Claim boundary" in report
