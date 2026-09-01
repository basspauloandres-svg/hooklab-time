#!/usr/bin/env python3
"""Validate exploratory P0 producer responses without scientific promotion."""
from __future__ import annotations
REQUIRED=('preferred_condition','retain','modify','reject','reason','hook_strength','singability','memorability','creative_usefulness')
def validate(x):
 reasons=[f'MISSING_{k.upper()}' for k in REQUIRED if x.get(k) in (None,'',[])]
 for k in ('hook_strength','singability','memorability','creative_usefulness'):
  if k in x and x[k] not in (None,'') and not (1<=int(x[k])<=7): reasons.append(f'{k.upper()}_OUT_OF_RANGE')
 if x.get('preferred_condition') not in {'H','D0','HD0'}: reasons.append('INVALID_CONDITION')
 return {'status':'P0_RESPONSE_VALID' if not reasons else 'P0_RESPONSE_INVALID','blocking_reasons':reasons,'scientific_promotion':False}
