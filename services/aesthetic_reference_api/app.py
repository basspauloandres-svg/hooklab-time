#!/usr/bin/env python3
"""HookLab online fallback for AESTHETIC_REFERENCE_ANALYSIS.
Primary mobile path remains LOCAL_ON_DEVICE_ONNX.
This service is only a resilience fallback and never promotes audio/results into M300/Gate A/scientific evidence.
"""
import hashlib, json, os, subprocess, sys, tempfile
from pathlib import Path
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

ROOT = Path(__file__).resolve().parents[2]
SENSOR = ROOT / 'mie_core' / 'run_fulltrack_sensor_regression.py'
NORMALIZER = ROOT / 'mie_core' / 'aesthetic_reference_analysis_contract.py'
MAX_BYTES = int(os.getenv('HOOKLAB_MAX_AUDIO_BYTES', str(50 * 1024 * 1024)))
ALLOWED_ORIGINS = [x for x in os.getenv('HOOKLAB_ALLOWED_ORIGINS','https://basspauloandres-svg.github.io').split(',') if x]

app = FastAPI(title='HookLab Aesthetic Reference Analyzer Fallback', version='0.1.0')
app.add_middleware(CORSMiddleware, allow_origins=ALLOWED_ORIGINS, allow_methods=['POST','GET'], allow_headers=['*'])

@app.get('/health')
def health():
    return {'status':'ok','role':'ONLINE_API_FALLBACK','scientific_ingestion':False}

def run_analysis(audio_bytes: bytes, filename: str, session_id: str, expected_sha256: str):
    actual = hashlib.sha256(audio_bytes).hexdigest()
    if actual != expected_sha256:
        raise ValueError('SHA256_SESSION_MISMATCH')
    suffix = Path(filename or 'reference.wav').suffix or '.wav'
    with tempfile.TemporaryDirectory(prefix='hooklab_ref_') as td:
        td = Path(td)
        src = td / ('source' + suffix)
        sensor_json = td / 'sensor.json'
        out_json = td / 'analysis.json'
        src.write_bytes(audio_bytes)
        try:
            subprocess.run([sys.executable, str(SENSOR), '--audio', str(src), '--output', str(sensor_json)], cwd=ROOT, check=True, timeout=240)
            subprocess.run([sys.executable, str(NORMALIZER), '--sensor', str(sensor_json), '--session-id', session_id, '--expected-sha256', expected_sha256, '--output', str(out_json)], cwd=ROOT, check=True, timeout=30)
            result = json.loads(out_json.read_text())
            result['analysis_mode'] = 'ONLINE_API_FALLBACK'
            return result
        finally:
            # TemporaryDirectory removes source audio and all intermediates.
            pass

@app.post('/v1/analyze-reference')
async def analyze_reference(
    audio: UploadFile = File(...),
    session_id: str = Form(...),
    sha256: str = Form(...),
):
    if not audio.content_type or not audio.content_type.startswith('audio/'):
        raise HTTPException(415, 'AUDIO_MIME_REQUIRED')
    data = await audio.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise HTTPException(413, 'AUDIO_TOO_LARGE')
    try:
        return run_analysis(data, audio.filename or 'reference.wav', session_id, sha256.lower())
    except ValueError as e:
        raise HTTPException(409, str(e))
    except subprocess.TimeoutExpired:
        raise HTTPException(504, 'ANALYZER_TIMEOUT')
    except subprocess.CalledProcessError:
        raise HTTPException(502, 'ANALYZER_FAILED')
