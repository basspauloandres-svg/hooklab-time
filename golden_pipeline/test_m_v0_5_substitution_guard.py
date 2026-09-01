#!/usr/bin/env python3
"""Negative invariants for the guarded golden M-substitution renderer.

These tests intentionally do not render an audible candidate. They prove that
unverified timeline alignment and altered frozen H/T provenance are rejected.
"""
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / 'app-mie-p30-harmony-beat-v0.1.html'
SCRIPT = ROOT / 'golden_pipeline' / 'render_m_v0_5_substitution.js'


def run(renderer, manifest, out):
    return subprocess.run(
        ['node', str(SCRIPT), str(renderer), str(manifest), str(out)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def minimal_manifest(status='BLOCKED'):
    return {
        'version': 'guard-test',
        'alignment_status': status,
        'same_source_confirmed': status == 'VERIFIED',
        'alignment_evidence': ['synthetic guard test'] if status == 'VERIFIED' else [],
        'melody_events': [
            {'id': 'x', 'start_s': 13.4, 'end_s': 13.6, 'midi': 60, 'state': 'LOCK'}
        ],
    }


def test_unverified_alignment_is_refused(tmp):
    manifest = tmp / 'blocked.json'
    manifest.write_text(json.dumps(minimal_manifest('BLOCKED')), encoding='utf-8')
    r = run(RENDERER, manifest, tmp / 'should_not_exist.wav')
    assert r.returncode != 0
    assert 'alignment_status must be VERIFIED' in (r.stderr + r.stdout)
    assert not (tmp / 'should_not_exist.wav').exists()


def test_renderer_byte_change_is_refused_before_render(tmp):
    altered = tmp / 'altered.html'
    altered.write_bytes(RENDERER.read_bytes() + b'\n')
    manifest = tmp / 'verified.json'
    manifest.write_text(json.dumps(minimal_manifest('VERIFIED')), encoding='utf-8')
    r = run(altered, manifest, tmp / 'should_not_exist_2.wav')
    assert r.returncode != 0
    assert 'canonical renderer SHA mismatch' in (r.stderr + r.stdout)
    assert not (tmp / 'should_not_exist_2.wav').exists()


def main():
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        test_unverified_alignment_is_refused(tmp)
        test_renderer_byte_change_is_refused_before_render(tmp)
    print('PASS guarded M substitution negative invariants')


if __name__ == '__main__':
    main()
