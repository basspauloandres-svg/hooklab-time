"""Local/private HTTP service for the recovered MIE M+H+T pipeline."""

from __future__ import annotations

import base64
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import tempfile

from fastapi import FastAPI, File, Form, Header, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from mie_core.mie_recognition_contract import normalize
from mie_core.mie_recovery_pipeline import apply_reasoning
from mie_core.mie_octave_plane_resolver import resolve_event_octaves
from mie_core.mie_recovery_resynthesis import render


ROOT = Path(__file__).resolve().parents[1]
MAX_BYTES = int(os.environ.get("HOOKLAB_MAX_AUDIO_BYTES", 100 * 1024 * 1024))
ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        "HOOKLAB_CORS_ORIGINS",
        "http://127.0.0.1:8000,http://localhost:8000,https://raw.githack.com",
    ).split(",")
    if origin.strip()
]

app = FastAPI(title="HookLab MIE Analyzer", version="0.3-recovery")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "X-HookLab-Contract", "Authorization"],
)


def run_checked(command):
    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    if completed.returncode:
        raise RuntimeError(completed.stderr[-2000:] or completed.stdout[-2000:] or "MIE_PROCESS_FAILED")


def analyze_path(source_path, output_dir, *, session_id, reference_sha256):
    wav_path = output_dir / "source.wav"
    stems_dir = output_dir / "stems"
    result_dir = output_dir / "result"
    run_checked(["ffmpeg", "-y", "-i", str(source_path), "-ar", "44100", "-ac", "2", str(wav_path)])
    run_checked([sys.executable, "-m", "demucs", "-n", "htdemucs", "-o", str(stems_dir), str(wav_path)])
    run_checked(
        [
            sys.executable,
            str(ROOT / "mie_core" / "run_mie_core.py"),
            "--audio",
            str(wav_path),
            "--stems",
            str(stems_dir),
            "--output",
            str(result_dir),
        ]
    )
    raw = json.loads((result_dir / "MIE_CORE_MHT_v0_2.json").read_text(encoding="utf-8"))
    raw["notes"] = resolve_event_octaves(raw.get("notes", []))
    reasoned = apply_reasoning(
        raw,
        analysis_id=session_id,
        endpoint=os.environ.get("HOOKLAB_MIE_AI_ENDPOINT"),
        token=os.environ.get("HOOKLAB_MIE_AI_TOKEN"),
    )
    normalized = normalize(
        reasoned,
        session_id=session_id,
        reference_sha256=reference_sha256,
        sensor_version="MIE_CORE_v0.2+RECOVERY_CONTRACT_v0.3",
        ai_provenance=reasoned.get("ai_provenance"),
    )
    if normalized["status"] != "PASS":
        raise RuntimeError("MIE_CONTRACT_FAIL:" + ",".join(normalized.get("reasons", [])))
    recovered_wav = result_dir / "MIE_RECOVERED_MHT_v0_3.wav"
    normalized["resynthesis"] = render(reasoned, recovered_wav)
    normalized["audition_wav_base64"] = base64.b64encode(
        recovered_wav.read_bytes()
    ).decode("ascii")
    normalized["audition_mime"] = "audio/wav"
    return normalized


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "HOOKLAB_MIE_ANALYZER_v0.3-recovery",
        "private_ai_configured": bool(os.environ.get("HOOKLAB_MIE_AI_ENDPOINT")),
        "scientific_d_unlocked": False,
    }


@app.post("/v1/analyze-reference")
async def analyze_reference(
    audio: UploadFile = File(...),
    session_id: str = Form(...),
    reference_sha256: str = Form(...),
    authorization: str | None = Header(default=None),
):
    required_token = os.environ.get("HOOKLAB_ANALYZER_TOKEN")
    supplied_token = authorization.removeprefix("Bearer ") if authorization else ""
    if required_token and not secrets.compare_digest(required_token, supplied_token):
        raise HTTPException(status_code=401, detail="ANALYZER_AUTH_REQUIRED")
    if not session_id.startswith("HL-"):
        raise HTTPException(status_code=400, detail="INVALID_SESSION_ID")
    digest = hashlib.sha256()
    with tempfile.TemporaryDirectory(prefix="hooklab-mie-") as temporary:
        work = Path(temporary)
        source = work / "source-upload"
        total = 0
        with source.open("wb") as target:
            while chunk := await audio.read(1024 * 1024):
                total += len(chunk)
                if total > MAX_BYTES:
                    raise HTTPException(status_code=413, detail="AUDIO_TOO_LARGE")
                digest.update(chunk)
                target.write(chunk)
        if digest.hexdigest() != reference_sha256.lower():
            raise HTTPException(status_code=409, detail="REFERENCE_SHA256_MISMATCH")
        try:
            return analyze_path(source, work, session_id=session_id, reference_sha256=reference_sha256.lower())
        except RuntimeError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error
