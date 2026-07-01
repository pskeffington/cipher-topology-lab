from __future__ import annotations

from ciphertopology.rag_verifier import verify_answer, verify_citation


def _manifest() -> dict[str, object]:
    return {
        "assets": [
            {
                "asset_id": "asset-abc",
                "path": "docs/source.md",
                "sha256": "file-sha",
                "trust_flags": ["chunk_hashable"],
                "chunks": [
                    {
                        "chunk_id": "lines-000001-000002-chunkabc",
                        "sha256": "chunk-sha",
                        "start_line": 1,
                        "end_line": 2,
                    }
                ],
            }
        ]
    }


def test_verify_citation_approves_matching_asset_and_chunk() -> None:
    citation = {
        "citation_id": "c1",
        "path": "docs/source.md",
        "asset_sha256": "file-sha",
        "chunk_id": "lines-000001-000002-chunkabc",
        "chunk_sha256": "chunk-sha",
    }

    check = verify_citation(citation, _manifest())

    assert check.status == "approved"
    assert check.reasons == []


def test_verify_citation_rejects_missing_asset() -> None:
    citation = {"citation_id": "c1", "path": "docs/missing.md"}

    check = verify_citation(citation, _manifest())

    assert check.status == "rejected"
    assert "asset_not_found_in_manifest" in check.reasons


def test_verify_citation_rejects_hash_mismatch() -> None:
    citation = {
        "citation_id": "c1",
        "path": "docs/source.md",
        "asset_sha256": "wrong-file-sha",
        "chunk_id": "lines-000001-000002-chunkabc",
        "chunk_sha256": "chunk-sha",
    }

    check = verify_citation(citation, _manifest())

    assert check.status == "rejected"
    assert "asset_sha256_mismatch" in check.reasons


def test_verify_answer_summarizes_counts() -> None:
    answer = {
        "answer_id": "answer-1",
        "citations": [
            {
                "citation_id": "c1",
                "path": "docs/source.md",
                "asset_sha256": "file-sha",
                "chunk_id": "lines-000001-000002-chunkabc",
                "chunk_sha256": "chunk-sha",
            },
            {"citation_id": "c2", "path": "docs/missing.md"},
        ],
    }

    report = verify_answer(answer, _manifest())

    assert report.status == "rejected"
    assert report.citation_count == 2
    assert report.approved_count == 1
    assert report.rejected_count == 1
