/* HookLab multimodal hook composition assistant v0.1
 * D0 exploratory compositional assistance.
 * Produces original text/prosody candidate scaffolds conditioned on abstract
 * reference/beat constraints. It does NOT claim scientific promotion.
 */
(function(root,factory){
  const api=factory();
  if(typeof module==='object'&&module.exports) module.exports=api;
  root.HookLabCompositionAssistant=api;
})(typeof globalThis!=='undefined'?globalThis:this,function(){
  'use strict';
  const VERSION='hooklab-multimodal-hook-assistant-v0.1';
  function id(prefix){return `${prefix}-${Date.now()}-${Math.random().toString(16).slice(2,10)}`;}
  function constraints(input){
    const a=input&&input.reference_analysis||{};
    const tempo=Number.isFinite(+a.tempo_bpm_median)?+a.tempo_bpm_median:120;
    const beatCount=Number.isFinite(+a.beat_count)?+a.beat_count:null;
    return {
      schema:'HOOKLAB_COMPOSITIONAL_CONSTRAINT_SET_v1.0',
      constraint_set_id:id('CS'),
      source_role:'AESTHETIC_REFERENCE',
      scientific_success_evidence:false,
      tempo_bpm:tempo,
      beat_count_observed:beatCount,
      meter_assumption:'4/4_D0_EXPLORATORY',
      target_hook_bars:2,
      target_phrase_count:2,
      target_syllables_per_phrase:[4,8],
      permitted_variants:['thetic','anacrustic','syncopated'],
      provenance:{reference_sha256:input&&input.reference_sha256||null,analysis_mode:a.analysis_mode||null,assistant_version:VERSION}
    };
  }
  function parseCandidate(text){
    const lines=String(text||'').split(/\n+/).map(x=>x.trim()).filter(Boolean);
    if(!lines.length)return {status:'AUDIT_TEXT_REQUIRED',blocking_reasons:['NO_TEXT_CANDIDATE']};
    const parsed=lines.map((line,li)=>({line_index:li+1,words:line.split(/\s+/).map((w,wi)=>({word_index:wi+1,text:w}))}));
    return {status:'GENERATED_TEXT_CANDIDATE',lines:parsed};
  }
  function candidate(input){
    const c=constraints(input),p=parseCandidate(input&&input.text_candidate);
    if(p.status!=='GENERATED_TEXT_CANDIDATE')return p;
    return {
      schema:'HOOKLAB_MULTIMODAL_HOOK_CANDIDATE_v1.0',
      assistant_version:VERSION,
      status:'GENERATED_CANDIDATE_REQUIRES_PRODUCER_CURATION',
      generation_class:'D0_EXPLORATORY',
      scientific_d_unlocked:false,
      hook_id:input.hook_id||id('HOOK'),
      text_candidate_id:id('TXT'),
      language:input.language||'es',
      intention:input.intention||'',
      constraint_set:c,
      text:p.lines,
      prosody_status:'GENERATED_PROSODY_CANDIDATE',
      required_next_gate:'PRODUCER_CURATES_SYLLABIFICATION_AND_STRESS',
      integration_targets:['TEXT','PROSODY','VOCAL_RHYTHM','MELODY','BEAT_RELATION'],
      forbidden_claims:['SUCCESS_PREDICTION','SCIENTIFIC_D','REFERENCE_COPYING'],
      provenance:{source:'HOOKLAB_GENERATIVE_ASSISTANCE',created_at:new Date().toISOString(),reference_sha256:input.reference_sha256||null}
    };
  }
  function validate(c){
    const r=[];
    if(!c||c.schema!=='HOOKLAB_MULTIMODAL_HOOK_CANDIDATE_v1.0')r.push('INVALID_SCHEMA');
    if(!c||c.generation_class!=='D0_EXPLORATORY'||c.scientific_d_unlocked!==false)r.push('SCIENTIFIC_BOUNDARY_BROKEN');
    if(!c||!c.constraint_set||c.constraint_set.source_role!=='AESTHETIC_REFERENCE')r.push('REFERENCE_ROLE_INVALID');
    if(!c||c.prosody_status!=='GENERATED_PROSODY_CANDIDATE')r.push('PROSODY_STATUS_INVALID');
    return {status:r.length?'AUDIT':'PASS',reasons:r};
  }
  return {VERSION,constraints,parseCandidate,candidate,validate};
});