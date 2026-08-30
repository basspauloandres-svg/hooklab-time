#!/usr/bin/env python3
"""Executable epistemic guard for HookLab/TIME.

This module makes the permanent data-first checkpoint machine-enforceable.
Any inferential/generative decision must declare its evidence origin. Human priors,
manual weights and unvalidated success rules are rejected from inferential mode.
They may exist only as explicitly labelled exploratory hypotheses.
"""
from dataclasses import dataclass, asdict
from typing import Optional

ALLOWED_INFERENTIAL_ORIGINS={
    'CORPUS_EMPIRICAL',
    'OUT_OF_SAMPLE_VALIDATED',
    'MEASUREMENT_INVARIANT',
}
EXPLORATORY_ORIGINS={'HYPOTHESIS','LITERATURE_PRIOR','HUMAN_PRIOR','EXPLORATORY_WEIGHT'}

@dataclass
class DecisionEvidence:
    decision_id:str
    origin:str
    description:str
    statistic:Optional[str]=None
    validation_scope:Optional[str]=None
    provisional:bool=False

class DataFirstViolation(RuntimeError): pass

def authorize(e:DecisionEvidence, mode:str='INFERENTIAL'):
    mode=mode.upper()
    if mode=='INFERENTIAL':
        if e.origin not in ALLOWED_INFERENTIAL_ORIGINS:
            raise DataFirstViolation(
                f'{e.decision_id}: origin={e.origin} cannot control inference. '
                'Required direction: DATA -> STATISTICAL STRUCTURE -> PATTERN -> CONTRAST -> VALIDATION -> DECISION.'
            )
        if e.provisional:
            raise DataFirstViolation(f'{e.decision_id}: provisional evidence cannot control inferential decisions.')
    elif mode=='EXPLORATORY':
        if e.origin not in ALLOWED_INFERENTIAL_ORIGINS|EXPLORATORY_ORIGINS:
            raise DataFirstViolation(f'{e.decision_id}: unknown evidence origin {e.origin}.')
    else:
        raise ValueError('mode must be INFERENTIAL or EXPLORATORY')
    return {'authorized':True,'mode':mode,'evidence':asdict(e)}

def assert_no_manual_success_weights(config:dict):
    forbidden={'success_score','manual_success_weights','ideal_song_profile','human_ranked_predictors'}
    bad=sorted(forbidden.intersection(config))
    if bad:
        raise DataFirstViolation('Forbidden pre-corpus decision fields: '+', '.join(bad))
    return True
