const fs=require('fs');
const html=fs.readFileSync('app/prototype_v1/studio.html','utf8');
const beat=fs.readFileSync('app/prototype_v1/local_beat_this.js','utf8');
function must(cond,msg){if(!cond)throw new Error(msg)}
must(html.includes('id="ref" type="file"'),'STUDIO_AUDIO_INPUT_MISSING');
must(html.includes('.mp3')&&html.includes('.m4a')&&html.includes('.wav'),'COMMON_MOBILE_AUDIO_EXTENSIONS_MISSING');
must(html.includes('sha256:session.reference?.sha256'),'SHA_HANDOFF_MISSING');
must(html.includes('crypto.subtle.digest'),'STUDIO_SHA_CALCULATION_MISSING');
must(html.includes('Referencia cargada:'),'AUDIO_RECEIPT_UI_STATE_MISSING');
must(beat.includes("const VERSION='hooklab-local-beat-this-v0.3'"),'BEAT_THIS_V03_REQUIRED');
must(beat.includes('UNKNOWN_MIME')||beat.includes('audio/'),'AUDIO_TYPE_HANDLING_MISSING');
must(beat.includes('window.webkitAudioContext'),'IOS_AUDIO_CONTEXT_FALLBACK_MISSING');
console.log('HOOKLAB_STUDIO_AUDIO_INTAKE_CONTRACT_PASS');
