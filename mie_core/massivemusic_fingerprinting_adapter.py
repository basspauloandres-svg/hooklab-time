#!/usr/bin/env python3
"""Optional fail-closed MassiveMusic Fingerprinting adapter for Gate A.

No provisioning -> deterministic REFERENCE_UNAVAILABLE.
The adapter never falls back to previews, scraping, downloads, user uploads, or
other unauthorized substitutes. With provisioning it delegates only to explicitly
configured commands executed inside the authorized environment and preserves
provenance for every stage.
"""
from __future__ import annotations
import argparse, json, os, subprocess
from datetime import datetime, timezone
from pathlib import Path

SCHEMA="HOOKLAB_MASSIVEMUSIC_FINGERPRINTING_ADAPTER_v1.0"
REQUIRED_ENV=("HOOKLAB_MM_PARTNER_ID","HOOKLAB_MM_AUTHORIZED_ENV_ID","HOOKLAB_MM_TRACK_RESOLVER_CMD","HOOKLAB_MM_PIPELINE_CMD")

def _utc(): return datetime.now(timezone.utc).isoformat()
def provisioning(env=os.environ):
    missing=[k for k in REQUIRED_ENV if not str(env.get(k,"" )).strip()]
    return {"provisioned":not missing,"missing":missing,"partner_id_present":bool(env.get("HOOKLAB_MM_PARTNER_ID")),"authorized_environment_id":env.get("HOOKLAB_MM_AUTHORIZED_ENV_ID")}

def _run_json(cmd, payload):
    p=subprocess.run(cmd,shell=True,input=json.dumps(payload),text=True,capture_output=True,timeout=3600)
    if p.returncode!=0: return {"ok":False,"returncode":p.returncode,"stderr":p.stderr[-2000:]}
    try:return {"ok":True,"data":json.loads(p.stdout)}
    except Exception:return {"ok":False,"returncode":p.returncode,"stderr":"NON_JSON_OUTPUT"}

def run(payload, env=os.environ, runner=_run_json):
    prov=provisioning(env); base={"schema":SCHEMA,"song_id":payload.get("song_id"),"provider":"massivemusic_fingerprinting","timestamp":_utc(),"provisioning":prov,"fallback_attempted":False,"forbidden_fallbacks":["preview","scraping","alternative_download","manual_user_upload","unauthorized_substitute"]}
    if not prov["provisioned"]:
        return {**base,"status":"REFERENCE_UNAVAILABLE","scientific_failure":False,"reason":"MASSIVEMUSIC_FINGERPRINTING_NOT_PROVISIONED","provenance":{"stages":[],"authorization_boundary":"FAIL_CLOSED_BEFORE_MEDIA_ACCESS"}}
    identity=runner(env["HOOKLAB_MM_TRACK_RESOLVER_CMD"],payload)
    stages=[{"stage":"TRACK_RESOLUTION","result":identity}]
    if not identity.get("ok"):
        return {**base,"status":"AUDIT","scientific_failure":False,"reason":"AUTHORIZED_TRACK_RESOLUTION_ERROR","provenance":{"stages":stages}}
    track=identity["data"]
    if track.get("version_identity_status")!="VERIFIED" or not track.get("authorized_computational_access"):
        return {**base,"status":"AUDIT","scientific_failure":False,"reason":"VERSION_OR_AUTHORIZATION_NOT_VERIFIED","track":track,"provenance":{"stages":stages}}
    execution_payload={"target":payload,"resolved_track":track,"required_pipeline":["AUTHORIZED_MEDIA","VOCAL_EXTRACTION","AUDIO_MIDI_ALIGNMENT","VALIDATION"]}
    result=runner(env["HOOKLAB_MM_PIPELINE_CMD"],execution_payload); stages.append({"stage":"AUTHORIZED_AUDIO_ANALYSIS_PIPELINE","result":result})
    if not result.get("ok"):
        return {**base,"status":"AUDIT","scientific_failure":False,"reason":"AUTHORIZED_PIPELINE_EXECUTION_ERROR","track":track,"provenance":{"stages":stages}}
    data=result["data"]; decision=data.get("validation_decision")
    if decision not in {"PASS","FAIL"}:
        return {**base,"status":"AUDIT","scientific_failure":False,"reason":"NO_VALIDATION_DECISION","track":track,"analysis":data,"provenance":{"stages":stages}}
    return {**base,"status":decision,"scientific_failure":decision=="FAIL","track":track,"analysis":data,"provenance":{"stages":stages,"authorized_environment_id":prov["authorized_environment_id"],"media_retention":"PROVIDER_ENVIRONMENT_ONLY_UNLESS_SEPARATELY_AUTHORIZED"}}

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--input",required=True);ap.add_argument("--output",required=True);a=ap.parse_args()
    out=run(json.loads(Path(a.input).read_text(encoding="utf-8")))
    Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding="utf-8");print(json.dumps({"song_id":out["song_id"],"status":out["status"]}))
if __name__=="__main__":main()
