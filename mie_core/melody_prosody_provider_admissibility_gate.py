#!/usr/bin/env python3
"""Fail-closed admissibility registry for melody/prosody research providers."""
from __future__ import annotations
import json,argparse
from pathlib import Path
PROVIDERS={
 'DALI':{'license':'CC BY-NC-SA 4.0','access':'RESTRICTED_REQUESTED','melody':'NOTES+TIME','lyrics':'TIME_ALIGNED','role':'TARGET_COVERAGE_CANDIDATE','status':'PENDING_PROVISIONING'},
 'RWC2_POP':{'license':'CC BY-NC 4.0','access':'OPEN_RELEASE','melody':'F0+ALIGNED_MIDI_ARCHIVE','lyrics':'AVAILABLE_ARCHIVE','role':'METHOD_REPLICATION','status':'RESEARCH_AUTHORIZED'},
 'MEDLEYDB_MELODY':{'license':'CC BY-NC-SA 4.0','access':'REQUEST_FOR_FULL_AUDIO; ANNOTATIONS_DOCUMENTED','melody':'F0','lyrics':'NO_PRIMARY_LYRIC_LAYER','role':'METHOD_CALIBRATION','status':'RESEARCH_AUTHORIZED'},
 'VOCADITO':{'license':'CREATIVE_COMMONS_PUBLIC','access':'OPEN','melody':'F0+TWO_NOTE_ANNOTATIONS','lyrics':'HUMAN_ANNOTATED','role':'NOTE_TRANSCRIPTION_CALIBRATION','status':'RESEARCH_AUTHORIZED'},
 'CANTE2MIDI':{'license':'OPEN_ZENODO_RECORD','access':'OPEN_METADATA/ANNOTATIONS','melody':'NOTE_LEVEL_MIDI_LIKE+F0','lyrics':'NOT_PRIMARY','role':'ORNAMENTED_VOCAL_CALIBRATION','status':'RESEARCH_AUTHORIZED'}
}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out={'schema':'HOOKLAB_MELODY_PROSODY_PROVIDER_REGISTRY_v1.0','providers':PROVIDERS,'invariants':['provider authorization != M300 target coverage','calibration datasets cannot increase M300 scientific N','DALI remains fail-closed until granted/provisioned','YouTube links are never authorized audio substitutes','melody representation semantics must be explicit before cross-provider pooling']};Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({k:v['status'] for k,v in PROVIDERS.items()}))
if __name__=='__main__':main()
