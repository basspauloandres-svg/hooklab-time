/* HookLab Lyric→Prosody→MIDI browser bridge v0.1
 * Mirrors the approved Python bridge contract for Producer Interface.
 * Curated prosody is mandatory. This adapter is D0_EXPLORATORY only.
 */
(function(root,factory){
  const api=factory();
  if(typeof module==='object'&&module.exports) module.exports=api;
  root.HookLabLyricProsody=api;
})(typeof globalThis!=='undefined'?globalThis:this,function(){
  'use strict';
  const VERSION='hooklab-lyric-prosody-ui-bridge-v0.1';
  const PPQ=480;

  function validateHook(h){
    const reasons=[];
    if(!h||h.schema!=='HOOKLAB_CURATED_HOOK_PROSODY_v1.0') reasons.push('INVALID_HOOK_SCHEMA');
    if(!h||h.prosody_status!=='CURATED_PROSODY_PASS') reasons.push('PROSODY_NOT_CURATED_PASS');
    if(!h||!String(h.hook_id||'').trim()) reasons.push('MISSING_HOOK_ID');
    if(!h||!String(h.language||'').trim()) reasons.push('MISSING_LANGUAGE');
    if(!h||!h.provenance) reasons.push('MISSING_PROVENANCE');
    const lines=h&&Array.isArray(h.lines)?h.lines:[];
    if(!lines.length) reasons.push('NO_LINES');
    lines.forEach((line,li)=>{
      const words=Array.isArray(line.words)?line.words:[];
      if(!words.length){reasons.push(`LINE_${li+1}_NO_WORDS`);return;}
      words.forEach((w,wi)=>{
        const sylls=Array.isArray(w.syllables)?w.syllables:[];
        if(!sylls.length) reasons.push(`LINE_${li+1}_WORD_${wi+1}_NO_SYLLABLES`);
        if(sylls.length&&!sylls.some(s=>Boolean(s.stressed))) reasons.push(`LINE_${li+1}_WORD_${wi+1}_NO_STRESS_DECLARED`);
        sylls.forEach((s,si)=>{if(!String(s.text||'').trim()) reasons.push(`LINE_${li+1}_WORD_${wi+1}_SYLL_${si+1}_EMPTY`);});
      });
    });
    return {status:reasons.length?'AUDIT_PROSODY_CONTRACT':'PASS',reasons};
  }

  function flatten(h){
    const out=[];
    (h.lines||[]).forEach((line,li)=>(line.words||[]).forEach((w,wi)=>(w.syllables||[]).forEach((s,si)=>out.push({
      line_index:li+1,word_index:wi+1,word:String(w.text||'').trim(),syllable_index_in_word:si+1,
      syllable:String(s.text||'').trim(),stressed:Boolean(s.stressed)
    }))));
    return out;
  }

  function bindVariant(variant,hook){
    const sylls=flatten(hook), events=variant&&Array.isArray(variant.events)?variant.events:[];
    if(!sylls.length) throw new Error('NO_CURATED_SYLLABLES');
    if(events.length<sylls.length) throw new Error(`INSUFFICIENT_EVENTS:${events.length}<${sylls.length}`);
    const mappings=[],nE=events.length,nS=sylls.length;
    sylls.forEach((sy,si)=>{
      let a=Math.floor(si*nE/nS),b=Math.floor((si+1)*nE/nS); if(b<=a)b=a+1;
      events.slice(a,b).forEach((e,ni)=>mappings.push({...sy,melisma_note_index:ni+1,onset_s:+e.onset_s,pitch_midi:+e.midi,duration_s:+(e.duration_s||0)}));
    });
    return mappings;
  }

  function vlq(n){let b=n&0x7f,out=[b];while((n>>=7)){b=(n&0x7f)|0x80;out.unshift(b);}return out;}
  function u16(n){return [(n>>8)&255,n&255];}
  function u32(n){return [(n>>>24)&255,(n>>>16)&255,(n>>>8)&255,n&255];}
  function strBytes(s){return Array.from(new TextEncoder().encode(s));}

  function midiBytes(variant,mappings){
    const bpm=+variant.tempo_bpm||120,us=Math.round(60000000/bpm),track=[];
    track.push(...vlq(0),0xff,0x51,0x03,(us>>16)&255,(us>>8)&255,us&255);
    track.push(...vlq(0),0xff,0x58,0x04,0x04,0x02,0x18,0x08);
    const name=strBytes('HookLab Lyric Prosody '+variant.variant);track.push(...vlq(0),0xff,0x03,name.length,...name);
    const ev=[];
    mappings.forEach(m=>{
      const on=Math.max(0,Math.round(m.onset_s*bpm/60*PPQ));
      const dur=Math.max(1,Math.round(Math.max(.05,m.duration_s||60/bpm*.8)*bpm/60*PPQ));
      if(m.melisma_note_index===1){const t=strBytes(m.syllable);ev.push({tick:on,ord:0,data:[0xff,0x05,...vlq(t.length),...t]});}
      ev.push({tick:on,ord:1,data:[0x90,m.pitch_midi,84]},{tick:on+dur,ord:2,data:[0x80,m.pitch_midi,0]});
    });
    ev.sort((a,b)=>a.tick-b.tick||a.ord-b.ord);let last=0;
    ev.forEach(e=>{track.push(...vlq(e.tick-last),...e.data);last=e.tick;});
    track.push(...vlq(0),0xff,0x2f,0x00);
    return new Uint8Array([...strBytes('MThd'),...u32(6),...u16(0),...u16(1),...u16(PPQ),...strBytes('MTrk'),...u32(track.length),...track]);
  }

  function build(d0Manifest,hook){
    const gate=validateHook(hook);if(gate.status!=='PASS')return {status:gate.status,blocking_reasons:gate.reasons};
    if(!d0Manifest||d0Manifest.stimulus_class!=='D0_EXPLORATORY'||d0Manifest.scientific_d!=='BLOCKED')return {status:'AUDIT_D0_CONTRACT',blocking_reasons:['D0_CONTRACT_NOT_PRESERVED']};
    const variants=(d0Manifest.variants||[]).map(v=>{const mapping=bindVariant(v,hook);return {variant:v.variant,mapping,mapping_count:mapping.length,midi_bytes:midiBytes(v,mapping)};});
    return {schema:'HOOKLAB_LYRIC_PROSODY_MIDI_UI_BRIDGE_v1.0',adapter_version:VERSION,status:'LYRIC_PROSODY_MIDI_BRIDGE_PASS',generation_class:'D0_EXPLORATORY',scientific_d_unlocked:false,hook_id:hook.hook_id,language:hook.language,prosody_status:hook.prosody_status,traceability_chain:['WORD','SYLLABLE','STRESS','ONSET','DURATION','PITCH','MIDI','HUMAN_EVALUATION'],mapping_policy:'MONOTONIC_SYLLABLE_TO_EXISTING_EVENTS; EXTRA_EVENTS_FORM_EXPLICIT_MELISMA',prosody_policy:'CURATED_INPUT_REQUIRED; NO_AUTOMATIC_STRESS_OR_SYLLABIFICATION_INFERENCE',provenance:hook.provenance,variants};
  }

  function midiBlob(item){return new Blob([item.midi_bytes],{type:'audio/midi'});}
  function portableManifest(result){return {...result,variants:(result.variants||[]).map(v=>({variant:v.variant,mapping_count:v.mapping_count,mapping:v.mapping}))};}
  return {VERSION,validateHook,flatten,bindVariant,midiBytes,midiBlob,portableManifest,build};
});
