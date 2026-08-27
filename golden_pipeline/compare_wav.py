#!/usr/bin/env python3
import argparse, hashlib, json, wave
from pathlib import Path
import numpy as np


def read_wav(path):
    with wave.open(str(path), 'rb') as w:
        meta = {
            'channels': w.getnchannels(),
            'sample_width': w.getsampwidth(),
            'sample_rate': w.getframerate(),
            'frames': w.getnframes(),
            'duration_s': w.getnframes() / w.getframerate(),
        }
        if meta['sample_width'] != 2:
            raise ValueError('Comparator currently requires PCM16 WAV')
        raw = w.readframes(w.getnframes())
    y = np.frombuffer(raw, dtype='<i2').astype(np.float64)
    return meta, y


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('golden')
    ap.add_argument('candidate')
    args = ap.parse_args()
    gm, g = read_wav(args.golden)
    cm, c = read_wav(args.candidate)
    report = {
        'golden': str(Path(args.golden)),
        'candidate': str(Path(args.candidate)),
        'golden_sha256': sha256(args.golden),
        'candidate_sha256': sha256(args.candidate),
        'byte_identical': sha256(args.golden) == sha256(args.candidate),
        'golden_meta': gm,
        'candidate_meta': cm,
        'structural_identity': gm == cm,
    }
    if len(g) == len(c):
        corr = float(np.corrcoef(g, c)[0, 1]) if np.std(g) and np.std(c) else None
        alpha = float(np.dot(g, c) / np.dot(c, c)) if np.dot(c, c) else None
        residual = g - (alpha * c if alpha is not None else c)
        report.update({
            'sample_correlation': corr,
            'least_squares_gain_candidate_to_golden': alpha,
            'residual_rms_pcm16': float(np.sqrt(np.mean(residual ** 2))),
            'golden_rms_pcm16': float(np.sqrt(np.mean(g ** 2))),
            'relative_residual_rms': float(np.sqrt(np.mean(residual ** 2)) / max(np.sqrt(np.mean(g ** 2)), 1e-12)),
            'max_abs_sample_difference': float(np.max(np.abs(g - c))),
        })
    else:
        report['sample_comparison'] = 'SKIPPED_LENGTH_MISMATCH'
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
