#!/usr/bin/env python3
"""Normalize observed HookLab statistical results under the canonical deduction framework.

This registry never infers a positive rule from significance alone. Missing uncertainty,
robustness, calibration, theory support, or replication can only block promotion.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path

DECISIONS={'PROMOTE_TO_CONDITIONED_DEDUCTION','HOLD_FOR_REPLICATION','NO_PROMOTION','AUDIT'}


def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def row(**kw):
    base={
      'ANALYSIS_ID':None,'POPULATION_SCOPE':None,'OUTCOME':None,'N_ELIGIBLE':None,
      'FEATURE_DOMAIN':None,'FEATURE':None,'ANALYSIS_PHASE':'EXPLORATORY',
      'EFFECT_SIZE_AND_UNCERTAINTY':{'effect':None,'uncertainty':'NOT_REPORTED_IN_SOURCE'},
      'MULTIPLICITY_CONTROL':'NOT_REPORTED_IN_SOURCE','CONTROLS_ALTERNATIVE_EXPLANATIONS':[],
      'ROBUSTNESS_SENSITIVITY':'NOT_REPORTED_IN_SOURCE','REPLICATION_STATUS':'NOT_REPLICATED',
      'THEORY_SUPPORT':'REQUIRES_THEORY_LINK','CLAIM_LEVEL':'ASSOCIATIVE',
      'CALIBRATION_STATUS':'NOT_APPLICABLE','SOURCE_RESULT':None,'DECISION':'AUDIT','RATIONALE':None
    }
    base.update(kw); assert base['DECISION'] in DECISIONS; return base


def build(mc,c,rob,m300):
    rows=[]
    k=mc['key_results']
    for outcome,key in [('weeks_on_chart','first_chorus_ratio_vs_weeks_on_chart'),('peak_strength','first_chorus_ratio_vs_peak_strength')]:
        x=k[key]
        rows.append(row(
          ANALYSIS_ID=f'MCGILL_EARLY_CHORUS_{outcome.upper()}',POPULATION_SCOPE=mc.get('role'),OUTCOME=outcome,
          N_ELIGIBLE=x['n'],FEATURE_DOMAIN='MUSIC_FORM',FEATURE='first_chorus_ratio',ANALYSIS_PHASE='HISTORICAL_CALIBRATION',
          EFFECT_SIZE_AND_UNCERTAINTY={'effect':{'spearman_rho':x['rho']},'uncertainty':'NOT_REPORTED_IN_SOURCE'},
          MULTIPLICITY_CONTROL={'method':'BH','q':x['q_bh']},CONTROLS_ALTERNATIVE_EXPLANATIONS=['historical era','genre/style','exposure','row-count discrepancy'],
          ROBUSTNESS_SENSITIVITY='CONTEMPORARY_REPLICATION_AVAILABLE_IN_COSOD_AND_M300_COSOD',REPLICATION_STATUS='REPLICATED_DIRECTIONALLY_AS_NON_SUPPORT',
          THEORY_SUPPORT='NO_POSITIVE_PATTERN_TO_INTERPRET',CLAIM_LEVEL='ASSOCIATIVE',SOURCE_RESULT='MCGILL_BILLBOARD_DEDUCTION_CALIBRATION_CURRENT_v1.json',
          DECISION='NO_PROMOTION',RATIONALE='Near-zero association; early-chorus rule not supported in historical calibration.' ))
    for feat,x in c['observed_results'].items():
        decision='NO_PROMOTION'
        rationale='Observed association did not pass the study support gate.'
        if feat=='aggregate_vocal_pitch_span_hz':
            decision='NO_PROMOTION'; rationale='Small raw-Hz association was superseded by semitone robustness analysis, which did not support advancement.'
        rows.append(row(
          ANALYSIS_ID=f'COSOD_{feat.upper()}',POPULATION_SCOPE=c['population_scope'],OUTCOME='year_end_peak_strength',N_ELIGIBLE=x['n'],
          FEATURE_DOMAIN='MUSIC_MELODY' if 'pitch' in feat else 'MUSIC_FORM',FEATURE=feat,ANALYSIS_PHASE='EXPLORATORY_CALIBRATION',
          EFFECT_SIZE_AND_UNCERTAINTY={'effect':{'spearman_rho':x['rho'],'partial_rho':x.get('partial_rho_year_collaboration_control')},'uncertainty':'NOT_REPORTED_IN_SOURCE'},
          MULTIPLICITY_CONTROL={'method':'BH','q':x['q_bh']},CONTROLS_ALTERNATIVE_EXPLANATIONS=['year','collaboration_type_gender','genre/style','exposure','artist history'],
          ROBUSTNESS_SENSITIVITY='SEMITONE_ROBUSTNESS_EXECUTED' if feat=='aggregate_vocal_pitch_span_hz' else 'M300_TARGET_SUBCOHORT_REPLICATION_AVAILABLE' if feat in {'first_chorus_s','section_events'} else 'LIMITED',
          REPLICATION_STATUS='NOT_POSITIVELY_REPLICATED',THEORY_SUPPORT='NO_PROMOTABLE_PATTERN',CLAIM_LEVEL='ASSOCIATIVE',
          CALIBRATION_STATUS='RAW_AGGREGATE_NOT_REPRESENTATION_CALIBRATED' if feat=='aggregate_vocal_pitch_span_hz' else 'NOT_APPLICABLE',
          SOURCE_RESULT='COSOD_CONTEMPORARY_DEDUCTION_CALIBRATION_CURRENT_v1.json',DECISION=decision,RATIONALE=rationale))
    for x in rob['tests']:
        rows.append(row(
          ANALYSIS_ID=f'COSOD_ROBUST_{x["feature"].upper()}',POPULATION_SCOPE=rob['population_scope'],OUTCOME='year_end_peak_strength',N_ELIGIBLE=x['n'],
          FEATURE_DOMAIN='MUSIC_MELODY',FEATURE=x['feature'],ANALYSIS_PHASE='ROBUSTNESS',
          EFFECT_SIZE_AND_UNCERTAINTY={'effect':{'spearman_rho':x['rho']},'uncertainty':'NOT_REPORTED_IN_SOURCE'},
          MULTIPLICITY_CONTROL={'method':'BH','q':x['q_bh']},CONTROLS_ALTERNATIVE_EXPLANATIONS=rob['controls'],
          ROBUSTNESS_SENSITIVITY='SEMITONE_AND_PERFORMER_AWARE_REPRESENTATION',REPLICATION_STATUS='ROBUSTNESS_CHECK_OF_RAW_HZ_SIGNAL',
          THEORY_SUPPORT='RAW_HZ_SIGNAL_NOT_ROBUST',CLAIM_LEVEL='ASSOCIATIVE',CALIBRATION_STATUS='NOT_VOCADITO_CALIBRATED_FEATURE',
          SOURCE_RESULT='COSOD_VOCAL_VARIABILITY_ROBUSTNESS_CURRENT_v1.json',DECISION='NO_PROMOTION',
          RATIONALE=rob['deductive_consequence']))
    for x in m300['tests']:
        rows.append(row(
          ANALYSIS_ID=f'M300_COSOD_{x["feature"].upper()}_{x["outcome"].upper()}',POPULATION_SCOPE=m300['population_scope'],OUTCOME=x['outcome'],N_ELIGIBLE=x['n'],
          FEATURE_DOMAIN='MUSIC_MELODY' if 'vocal_span' in x['feature'] else 'MUSIC_FORM',FEATURE=x['feature'],ANALYSIS_PHASE='TARGET_SUBCOHORT',
          EFFECT_SIZE_AND_UNCERTAINTY={'effect':{'spearman_rho':x['rho']},'uncertainty':'NOT_REPORTED_IN_SOURCE'},
          MULTIPLICITY_CONTROL={'method':'BH','q':x['q_bh']},CONTROLS_ALTERNATIVE_EXPLANATIONS=['top-15 selection','collaboration subpopulation','genre/style','exposure','artist history'],
          ROBUSTNESS_SENSITIVITY='TARGET_POPULATION_SUBCOHORT_TEST',REPLICATION_STATUS='TARGET_SUBCOHORT_TEST',THEORY_SUPPORT='NO_SUPPORTED_PATTERN',CLAIM_LEVEL='ASSOCIATIVE',
          CALIBRATION_STATUS='NOT_VOCADITO_CALIBRATED_FEATURE' if 'vocal_span' in x['feature'] else 'NOT_APPLICABLE',
          SOURCE_RESULT='M300_COSOD_TARGET_SUBCOHORT_ANALYSIS_CURRENT_v1.json',DECISION='NO_PROMOTION',RATIONALE=m300['decision']))
    rows.append(row(
      ANALYSIS_ID='M300_MEDIAN_PITCH_ST_PENDING',POPULATION_SCOPE='M300 songs with >=30 version-aligned note-event representations',OUTCOME='pre-registered M300 outcomes',N_ELIGIBLE=0,
      FEATURE_DOMAIN='MUSIC_MELODY',FEATURE='median_pitch_st',ANALYSIS_PHASE='PRE_REGISTERED_PENDING_EXTERNAL_PROVISIONING',
      EFFECT_SIZE_AND_UNCERTAINTY={'effect':None,'uncertainty':'NOT_ESTIMABLE_WITHOUT_POPULATION_DATA'},MULTIPLICITY_CONTROL='FROZEN_BH_GATE_NOT_YET_EXECUTED',
      CONTROLS_ALTERNATIVE_EXPLANATIONS=['released-recording identity','genre/style','exposure','artist history'],ROBUSTNESS_SENSITIVITY='VOCADITO_DUAL_REFERENCE_PASS',
      REPLICATION_STATUS='POPULATION_ASSOCIATION_NOT_EXECUTED',THEORY_SUPPORT='INTERPRET_ONLY_IF_PATTERN_OBSERVED',CLAIM_LEVEL='DESCRIPTIVE',
      CALIBRATION_STATUS='REPRESENTATION_CALIBRATED_DUAL_REFERENCE',SOURCE_RESULT='VOCADITO_REPRESENTATION_CALIBRATION + DALI_PENDING',DECISION='AUDIT',
      RATIONALE='Representation is calibrated; population association remains indeterminate pending >=30 version-aligned note-event rows.'))
    return {
      'schema':'HOOKLAB_STATISTICAL_DEDUCTION_MASTER_REGISTRY_v1.0',
      'framework':['OBSERVATION','ASSOCIATION','INTERPRETATION','HYPOTHESIS','CONDITIONED_DEDUCTION','MUSICAL_REALIZATION','HUMAN_EVALUATION'],
      'purpose':'DEDUCTION_NOT_PREDICTION','rows':rows,
      'summary':{
        'analysis_rows':len(rows),'promote':sum(r['DECISION']=='PROMOTE_TO_CONDITIONED_DEDUCTION' for r in rows),
        'hold':sum(r['DECISION']=='HOLD_FOR_REPLICATION' for r in rows),'no_promotion':sum(r['DECISION']=='NO_PROMOTION' for r in rows),
        'audit':sum(r['DECISION']=='AUDIT' for r in rows)
      },
      'scientific_d_state':'BLOCKED_NO_POSITIVE_ELIGIBLE_DEDUCTION',
      'boundary':'A null/non-promotion registry is a valid scientific result. Missing uncertainty can never be used to promote a positive deduction.'
    }

def main():
    ap=argparse.ArgumentParser()
    for x in ('mcgill','cosod','robustness','m300'): ap.add_argument(f'--{x}',required=True)
    ap.add_argument('--output',required=True); a=ap.parse_args()
    out=build(load(a.mcgill),load(a.cosod),load(a.robustness),load(a.m300))
    Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(out['summary']))
if __name__=='__main__': main()
