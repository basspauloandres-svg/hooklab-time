# MIE Recognition v0.3 — local/private runbook

Status: `CANDIDATE / NOT BASELINE`

## Primary producer route: mobile Colab

The producer-facing prototype is operated from the phone through
`notebooks/MIE_Recognition_v0_3_Mobile_Colab.ipynb`. Colab provides the temporary
computer, so the producer does not install Python, ffmpeg or the models on a personal
computer. The notebook retains the same M/H/T contracts and downloads a ZIP with the
audible reconstruction and recognition JSON.

The local-service instructions below remain an engineering fallback and a future
stable deployment option. They are not the required producer workflow for the current
mobile test.

## What the user must provide

For the recovery test, the producer supplies only an authorized audio file and
performs the final listening comparison. API keys, corpus files and manual stem
separation are not required from the producer.

## Local analyzer requirements

- Python 3.10;
- ffmpeg available on the system path;
- sufficient local disk/RAM for HTDemucs, Basic Pitch and Beat This;
- internet access during first model installation/download;
- a private random analyzer token.

## Installation

```bash
python3.10 -m venv .venv-mie
source .venv-mie/bin/activate
python -m pip install -r mie_core/requirements.txt
```

## Start on the same computer

```bash
export HOOKLAB_ANALYZER_TOKEN='replace-with-a-long-random-token'
uvicorn mie_core.mie_analyzer_service:app --host 127.0.0.1 --port 8765
```

Use `http://127.0.0.1:8765` as the console endpoint. The token is entered in the
console at runtime and is not committed or stored by HookLab.

## iPhone boundary

An iPhone cannot reach `127.0.0.1` on another computer. Mobile testing requires an
authenticated HTTPS route to the local service. The analyzer must never be exposed
through an unauthenticated public tunnel because uploaded audio and compute capacity
would become publicly reachable. The next deployment gate is to configure an HTTPS
private route, restrict CORS to the canonical console origin and retain the bearer
token requirement.

## Processing

`audio -> SHA-256 verification -> ffmpeg -> HTDemucs -> Basic Pitch/Plane candidate
-> harmonic sensor -> Beat This -> constrained reasoning -> M+H+T resynthesis ->
recognition JSON -> deletion of temporary audio/stems`

## Current limits

The event-level octave resolver in v0.3 is a candidate reconstruction and does not
yet replace the frozen frame-level Plane Resolver. A private AI provider is optional;
when absent, the service declares and uses the deterministic contextual reasoner.
Neither mode may create pitches absent from the acoustic candidate set.
