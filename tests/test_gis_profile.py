from __future__ import annotations

from ciphertopology.gis_profile import build_gis_profile, infer_asset_sector, is_gis_candidate


def test_is_gis_candidate_from_source_type() -> None:
    asset = {"path": "data/water.geojson", "source_type": "gis_layer", "extension": ".geojson"}
    assert is_gis_candidate(asset)


def test_infer_asset_sector_from_name() -> None:
    asset = {"path": "gis/town_water_mains.geojson"}
    assert infer_asset_sector(asset) == "water"


def test_build_gis_profile_counts_missing_and_covered() -> None:
    manifest = {
        "assets": [
            {
                "path": "gis/town_roads.geojson",
                "source_type": "gis_layer",
                "extension": ".geojson",
                "trust_flags": ["gis_layer_candidate"],
            },
            {
                "path": "gis/water_hydrants.geojson",
                "source_type": "gis_layer",
                "extension": ".geojson",
                "trust_flags": ["gis_layer_candidate"],
            },
        ]
    }

    report = build_gis_profile(manifest)

    assert report.gis_candidate_count == 2
    assert report.covered_sector_count >= 2
    assert report.missing_sector_count > 0
    covered = {finding.sector for finding in report.findings if finding.status == "covered_candidate"}
    assert "roads_transportation" in covered
    assert "water" in covered
