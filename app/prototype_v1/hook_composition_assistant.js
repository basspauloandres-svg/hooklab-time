/* HookLab multimodal hook composition assistant v0.3
 * D0 exploratory compositional assistance.
 * Generates original hook-text candidates and ranks fit against abstract
 * reference/beat/melody-capacity constraints. No success prediction.
 */
(function(root,factory){
  const api=factory();
  if(typeof module==='object'&&module.exports) module.exports=api;
  root.HookLabCompositionAssistant=api;
})(typeof globalThis!=='undefined'?globalThis:this,function(){
  'use strict';
  const VERSION='hooklab-multimodal-hook-assistant-v0.3';
  function id(prefix){return `${prefix}-${Date.now()}-${Math.random().toString(16).slice(2,10)}`;}
  function clean(s){return String(s||'').trim().replace(/\s+/g,' ');}
  function constraints(input){
    const a=input&&input.reference_analysis||{}, d=input&&input.d0_manifest||{};
    const tempo=Number.isFinite(+a.tempo_bpm_median)?+a.tempo_bpm_median:120;
    const beatCount=Number.isFinite(+a.beat_count)?+a.beat_count:null;
    const capacities=(d.variants||[]).map(v=>({variant:v.variant,event_count:Array.isArray(v.events)?v.events.length:0}));
    const maxEvents=capacities.reduce((m,x)=>Math.max(m,x.event_count),0)||8;
    const tempoClass=tempo<90?'SLOW':tempo>130?'FAST':'MID';
    const target=tempoClass==='FAST'?[3,6]:tempoClass==='SLOW'?[5,9]:[4,8];
    return {
      schema:'HOOKLAB_COMPOSITIONAL_CONSTRAINT_SET_v1.1',constraint_set_id:id('CS'),source_role:'AESTHETIC_REFERENCE',
      scientific_success_evidence:false,tempo_bpm:tempo,tempo_class:tempoClass,beat_count_observed:beatCount,
      meter_assumption:'4/4_D0_EXPLORATORY',target_hook_bars:2,target_phrase_count:2,target_syllables_per_phrase:target,
      melody_event_capacity:maxEvents,variant_capacities:capacities,permitted_variants:['thetic','anacrustic','syncopated'],
      provenance:{reference_sha256:input&&input.reference_sha256||null,analysis_mode:a.analysis_mode||null,d0_schema:d.schema||null,assistant_version:VERSION}
    };
  }
  function parseCandidate(text){
    const lines=String(text||'').split(/\n+/).map(x=>x.trim()).filter(Boolean);
    if(!lines.length)return {status:'AUDIT_TEXT_REQUIRED',blocking_reasons:['NO_TEXT_CANDIDATE']};
    return {status:'GENERATED_TEXT_CANDIDATE',lines:lines.map((line,li)=>({line_index:li+1,words:line.split(/\s+/).map((w,wi)=>({word_index:wi+1,text:w}))}))};
  }
  function syllablesApprox(word){
    const w=clean(word).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-záéíóúüñ]/g,'');
    if(!w)return 0; const g=w.match(/[aeiouy]+/g); return Math.max(1,g?g.length:1);
  }
  function lineSyllables(line){return clean(line).split(/\s+/).filter(Boolean).reduce((n,w)=>n+syllablesApprox(w),0);}
  function textFit(text,c){
    const lines=String(text).split(/\n+/).map(clean).filter(Boolean), lo=c.target_syllables_per_phrase[0],hi=c.target_syllables_per_phrase[1];
    const syllableCounts=lines.map(lineSyllables), total=syllableCounts.reduce((a,b)=>a+b,0);
    const phrasePenalty=Math.abs(lines.length-c.target_phrase_count)*2;
    const rangePenalty=syllableCounts.reduce((p,n)=>p+(n<lo?lo-n:n>hi?n-hi:0),0);
    const capacityPenalty=Math.max(0,total-c.melody_event_capacity);
    const score=Math.max(0,100-(phrasePenalty*12+rangePenalty*7+capacityPenalty*5));
    return {score,syllable_counts:syllableCounts,total_syllables:total,phrase_penalty:phrasePenalty,range_penalty:rangePenalty,melody_capacity_penalty:capacityPenalty};
  }
  function themeTokens(input){
    const src=clean(input&&input.intention||input&&input.theme||'');
    const xs=src.toLowerCase().split(/[^\p{L}\p{N}]+/u).filter(x=>x.length>2).slice(0,3);
    return xs.length?xs:['aquí'];
  }
  function rawTemplates(theme){
    const t=theme[0],u=theme[1]||theme[0];
    return [
      `vuelvo hacia ${t}\n${t} vuelve a mí`,
      `quédate en ${t}\nquiero quedarme aquí`,
      `late ${t} en mí\nlo vuelvo a sentir`,
      `dime ${t} otra vez\nque yo vuelvo también`,
      `hoy elijo ${t}\nmañana sigo aquí`,
      `${t} cerca de mí\n${u} dentro de mí`,
      `voy detrás de ${t}\n${t} viene hacia mí`,
      `si dices ${t}\nyo digo vuelve aquí`
    ];
  }
  function makeEnvelope(input,text,c,rank){
    const p=parseCandidate(text);
    return {schema:'HOOKLAB_MULTIMODAL_HOOK_CANDIDATE_v1.1',assistant_version:VERSION,status:'GENERATED_CANDIDATE_REQUIRES_PRODUCER_CURATION',
      generation_class:'D0_EXPLORATORY',scientific_d_unlocked:false,hook_id:input.hook_id||id('HOOK'),text_candidate_id:id('TXT'),candidate_rank:rank,
      language:input.language||'es',intention:input.intention||'',constraint_set:c,text:p.lines,plain_text:text,
      fit:textFit(text,c),prosody_status:'GENERATED_PROSODY_CANDIDATE',required_next_gate:'PRODUCER_CURATES_SYLLABIFICATION_AND_STRESS',
      integration_targets:['TEXT','PROSODY','VOCAL_RHYTHM','MELODY','BEAT_RELATION'],forbidden_claims:['SUCCESS_PREDICTION','SCIENTIFIC_D','REFERENCE_COPYING'],
      provenance:{source:'HOOKLAB_GENERATIVE_ASSISTANCE',created_at:new Date().toISOString(),reference_sha256:input.reference_sha256||null,template_family:'ORIGINAL_GENERIC_COMPOSITIONAL_SCAFFOLD'}};
  }
  function generateCandidates(input,count){
    const c=constraints(input), theme=themeTokens(input), custom=clean(input&&input.text_candidate);
    let texts=rawTemplates(theme); if(custom)texts.unshift(custom.replace(/\s*\|\s*/g,'\n'));
    texts=[...new Set(texts)];
    const ranked=texts.map(t=>({text:t,fit:textFit(t,c)})).sort((a,b)=>b.fit.score-a.fit.score||a.text.localeCompare(b.text));
    return {schema:'HOOKLAB_MULTIMODAL_CANDIDATE_SET_v1.0',assistant_version:VERSION,status:'CANDIDATE_SET_READY_FOR_PRODUCER_CURATION',generation_class:'D0_EXPLORATORY',scientific_d_unlocked:false,
      constraint_set:c,candidates:ranked.slice(0,Math.max(3,Math.min(+count||6,8))).map((x,i)=>makeEnvelope(input,x.text,c,i+1)),
      scoring_policy:'FIT_TO_PREDECLARED_PHRASE_SYLLABLE_RANGE_AND_EXISTING_D0_MELODY_EVENT_CAPACITY; NOT SUCCESS SCORE',
      producer_decision_required:true};
  }
  function candidate(input){
    const c=constraints(input),p=parseCandidate(input&&input.text_candidate); if(p.status!=='GENERATED_TEXT_CANDIDATE')return p;
    return makeEnvelope(input,input.text_candidate,c,1);
  }
  function validate(c){
    const r=[];
    if(!c||!String(c.schema||'').startsWith('HOOKLAB_MULTIMODAL_HOOK_CANDIDATE_'))r.push('INVALID_SCHEMA');
    if(!c||c.generation_class!=='D0_EXPLORATORY'||c.scientific_d_unlocked!==false)r.push('SCIENTIFIC_BOUNDARY_BROKEN');
    if(!c||!c.constraint_set||c.constraint_set.source_role!=='AESTHETIC_REFERENCE')r.push('REFERENCE_ROLE_INVALID');
    if(!c||c.prosody_status!=='GENERATED_PROSODY_CANDIDATE')r.push('PROSODY_STATUS_INVALID');
    return {status:r.length?'AUDIT':'PASS',reasons:r};
  }
  return {VERSION,constraints,parseCandidate,syllablesApprox,lineSyllables,textFit,candidate,generateCandidates,validate};
});

/* Browser provenance instrumentation. This records creative evaluation linkage;
 * it does not convert producer preference into scientific evidence. */
(function(){
  if(typeof document==='undefined'||typeof localStorage==='undefined')return;
  function val(id){const e=document.getElementById(id);return e?e.value:null;}
  document.addEventListener('click',ev=>{
    const b=ev.target.closest&&ev.target.closest('.useHookCandidate');
    if(b&&window.__hooklabCandidateSet){
      const c=window.__hooklabCandidateSet.candidates[+b.dataset.i];
      if(c){
        window.__hooklabSelectedCandidate=c;
        localStorage.setItem('hooklab_current_candidate',JSON.stringify({text_candidate_id:c.text_candidate_id,hook_id:c.hook_id,constraint_set_id:c.constraint_set.constraint_set_id,reference_sha256:c.provenance.reference_sha256,selected_at:new Date().toISOString()}));
      }
    }
    const save=ev.target.closest&&ev.target.closest('#save');
    if(save&&window.__hooklabSelectedCandidate){
      const c=window.__hooklabSelectedCandidate;
      const session=document.getElementById('sessionId')?.textContent||localStorage.getItem('hooklab_session_id')||null;
      const variant=val('variant');
      const trace={schema:'HOOKLAB_PRODUCER_EVALUATION_TRACE_v1.0',evaluation_id:id('EVAL'),session_id:session,hook_id:val('hookId')||c.hook_id,text_candidate_id:c.text_candidate_id,constraint_set_id:c.constraint_set.constraint_set_id,reference_sha256:c.provenance.reference_sha256,variant_id:variant,generation_class:'D0_EXPLORATORY',scientific_evidence:false,producer_evaluation:{decision:val('decision'),reason:val('reason'),hook_strength:+val('hook'),singability:+val('sing'),memorability:+val('mem'),creative_usefulness:+val('use')},saved_at:new Date().toISOString()};
      const key=`hooklab_trace_${session}_${c.text_candidate_id}_${variant}`;
      localStorage.setItem(key,JSON.stringify(trace));
      window.__hooklabLastEvaluationTrace=trace;
    }
  });
})();
