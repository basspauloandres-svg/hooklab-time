import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from mie_core.mie_frozen_reference_contract import (
    H_CHANGED,
    MISSING,
    PASS,
    SOURCE_MISMATCH,
    T_CHANGED,
    audit_candidate_against_frozen_reference,
    canonical_sha256,
)


def manifest_for(harmony, tactus, source_sha="a" * 64):
    return {
        "schema": "HOOKLAB_MIE_FROZEN_REFERENCE_MANIFEST_v1",
        "changed_module": "M_ONLY",
        "source_sha256": source_sha,
        "harmony_reference_sha256": canonical_sha256(harmony),
        "tactus_reference_sha256": canonical_sha256(tactus),
        "reference_artifact": {"artifact_id": 1, "zip_sha256": "b" * 64},
        "reference_commit": "c" * 40,
    }


def test_predeclared_hashes_are_required():
    result = audit_candidate_against_frozen_reference(
        manifest={},
        source_sha256="a" * 64,
        harmony_candidate=[],
        tactus_candidate=[],
    )
    assert result["status"] == MISSING
    assert result["harmony_byte_equivalent"] is False
    assert result["tactus_byte_equivalent"] is False


def test_candidate_passes_only_against_external_predeclared_hashes():
    harmony = [{"start_s": 0.0, "end_s": 1.0, "root_pc": 0, "state": "LOCK"}]
    tactus = [{"t": 0.0, "score": 0.9}, {"t": 0.5, "score": 0.8}]
    result = audit_candidate_against_frozen_reference(
        manifest=manifest_for(harmony, tactus),
        source_sha256="a" * 64,
        harmony_candidate=list(harmony),
        tactus_candidate=list(tactus),
    )
    assert result["status"] == PASS
    assert result["harmony_byte_equivalent"] is True
    assert result["tactus_byte_equivalent"] is True


def test_harmony_change_blocks_m_only_experiment():
    harmony = [{"start_s": 0.0, "end_s": 1.0, "root_pc": 0, "state": "LOCK"}]
    tactus = [{"t": 0.0, "score": 0.9}]
    changed = [{"start_s": 0.0, "end_s": 1.0, "root_pc": 5, "state": "LOCK"}]
    result = audit_candidate_against_frozen_reference(
        manifest=manifest_for(harmony, tactus),
        source_sha256="a" * 64,
        harmony_candidate=changed,
        tactus_candidate=tactus,
    )
    assert result["status"] == H_CHANGED


def test_tactus_change_blocks_promotion():
    harmony = [{"start_s": 0.0, "end_s": 1.0, "root_pc": 0, "state": "LOCK"}]
    tactus = [{"t": 0.0, "score": 0.9}]
    changed_t = [{"t": 0.0, "score": 0.8}]
    result = audit_candidate_against_frozen_reference(
        manifest=manifest_for(harmony, tactus),
        source_sha256="a" * 64,
        harmony_candidate=harmony,
        tactus_candidate=changed_t,
    )
    assert result["status"] == T_CHANGED


def test_source_hash_must_match_reference_source():
    harmony = []
    tactus = []
    result = audit_candidate_against_frozen_reference(
        manifest=manifest_for(harmony, tactus, source_sha="a" * 64),
        source_sha256="d" * 64,
        harmony_candidate=harmony,
        tactus_candidate=tactus,
    )
    assert result["status"] == SOURCE_MISMATCH


if __name__ == "__main__":
    test_predeclared_hashes_are_required()
    test_candidate_passes_only_against_external_predeclared_hashes()
    test_harmony_change_blocks_m_only_experiment()
    test_tactus_change_blocks_promotion()
    test_source_hash_must_match_reference_source()
    print("MIE_FROZEN_REFERENCE_CONTRACT_PASS")
