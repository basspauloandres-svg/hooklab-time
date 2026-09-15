(function(g){'use strict';
const POLICY={
  schema:'HOOKLAB_EVIDENCE_GATE_POLICY_v1',
  fail_closed:true,
  allowed_epistemic_states:['OBSERVED_ACOUSTIC','MODEL_ESTIMATED','AI_INFERRED','HUMAN_AUDITED','CANONICAL_ADMITTED','AMBIGUOUS','BLOCKED'],
  allowed_rule_states:['CONDITIONED_RULE'],
  allowed_rule_strength:['STAT_SUPPORTED','MODEL_SUPPORTED'],
  required_provenance_fields:['source_case_ids','feature_ids','analysis_id','rule_id','engine_version'],
  forbidden_generation_sources:['MODEL_PRIOR_ONLY','GENERAL_COMPOSITIONAL_INTUITION','UNTRACED_AI_PROPOSAL'],
  human_input_sources:['AUTHOR_PROVIDED','PRODUCER_DECISION'],
  descriptive_only_states:['OBSERVED_ACOUSTIC','MODEL_ESTIMATED','AI_INFERRED','HUMAN_AUDITED','AMBIGUOUS'],
  scientific_generation_state:'CANONICAL_ADMITTED'
};
function fail(reason,details){return {status:'BLOCKED',allowed:false,reason,details:details||null,policy:POLICY.schema};}
function ok(scope,trace){return {status:'PASS',allowed:true,scope,trace,policy:POLICY.schema};}
function hasFields(o,fields){return fields.every(k=>o&&o[k]!=null&&o[k]!==''&&(!Array.isArray(o[k])||o[k].length>0));}
function validateEvidence(e){
  if(!e)return fail('MISSING_EVIDENCE');
  if(!POLICY.allowed_epistemic_states.includes(e.epistemic_state))return fail('UNKNOWN_EPISTEMIC_STATE',{state:e.epistemic_state});
  if(e.epistemic_state==='BLOCKED'||e.epistemic_state==='AMBIGUOUS')return fail('EVIDENCE_NOT_ADMISSIBLE',{state:e.epistemic_state});
  if(!e.provenance||!hasFields(e.provenance,['source_case_ids','feature_ids','analysis_id','engine_version']))return fail('INCOMPLETE_EVIDENCE_PROVENANCE');
  return ok('EVIDENCE_VALIDATED',{analysis_id:e.provenance.analysis_id,feature_ids:e.provenance.feature_ids});
}
function validateRule(r){
  if(!r)return fail('MISSING_CONDITIONED_RULE');
  if(!POLICY.allowed_rule_states.includes(r.state))return fail('RULE_STATE_NOT_GENERATIVE',{state:r.state});
  if(!POLICY.allowed_rule_strength.includes(r.strength))return fail('RULE_STRENGTH_NOT_GENERATIVE',{strength:r.strength});
  if(!hasFields(r,POLICY.required_provenance_fields))return fail('INCOMPLETE_RULE_PROVENANCE');
  if(r.generative_eligible!==true)return fail('RULE_NOT_MARKED_GENERATIVE_ELIGIBLE');
  if(r.validation_status!=='PASS')return fail('RULE_VALIDATION_NOT_PASS',{validation_status:r.validation_status});
  return ok('RULE_VALIDATED',{rule_id:r.rule_id,analysis_id:r.analysis_id});
}
function generationDecision(req){
  if(!req)return fail('EMPTY_GENERATION_REQUEST');
  if(req.mode==='SCIENTIFIC'){
    if(req.scientific_d_unlocked!==true)return fail('SCIENTIFIC_D_LOCKED');
    if(!Array.isArray(req.rules)||req.rules.length===0)return fail('NO_ADMITTED_RULES');
    const checked=[];
    for(const r of req.rules){const v=validateRule(r);if(!v.allowed)return v;checked.push(v.trace);}
    if(Array.isArray(req.evidence))for(const e of req.evidence){const v=validateEvidence(e);if(!v.allowed)return v;if(e.epistemic_state!==POLICY.scientific_generation_state)return fail('EVIDENCE_NOT_CANONICAL_ADMITTED',{state:e.epistemic_state});}
    return ok('SCIENTIFIC_GENERATION',{rule_trace:checked});
  }
  if(req.mode==='EXPLORATORY'){
    if(req.claim_as_corpus_evidence===true)return fail('EXPLORATORY_OUTPUT_CANNOT_BECOME_CORPUS_EVIDENCE');
    if(req.source==='MODEL_PRIOR_ONLY'||req.source==='GENERAL_COMPOSITIONAL_INTUITION'||req.source==='UNTRACED_AI_PROPOSAL')return fail('UNSUPPORTED_GENERATIVE_SOURCE',{source:req.source});
    return ok('D0_EXPLORATORY',{scientific_d_unlocked:false});
  }
  return fail('UNKNOWN_GENERATION_MODE',{mode:req.mode});
}
function lyricDecision(req){
  if(!req)return fail('EMPTY_LYRIC_REQUEST');
  if(!req.author_input||!hasFields(req.author_input,['source','answers']))return fail('AUTHOR_INPUT_REQUIRED');
  if(!POLICY.human_input_sources.includes(req.author_input.source))return fail('INVALID_AUTHOR_INPUT_SOURCE');
  if(!req.music_constraints||!hasFields(req.music_constraints,['melody_case_id','feature_ids','engine_version']))return fail('MUSIC_CONSTRAINTS_REQUIRED');
  if(req.claim_as_corpus_finding===true)return fail('AUTHOR_OR_AI_TEXT_CANNOT_BE_CORPUS_FINDING');
  return ok('LYRIC_CONSTRAINED_ASSISTANCE',{author_source:req.author_input.source,feature_ids:req.music_constraints.feature_ids});
}
function assertGeneration(req){const r=generationDecision(req);if(!r.allowed){const e=new Error('HOOKLAB_EVIDENCE_GATE:'+r.reason);e.gate=r;throw e;}return r;}
g.HookLabEvidenceGate={version:'1.0.0',POLICY,validateEvidence,validateRule,generationDecision,lyricDecision,assertGeneration};
})(window);