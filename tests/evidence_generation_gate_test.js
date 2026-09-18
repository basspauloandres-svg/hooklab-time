global.window=global;
require('../app/prototype_v1/evidence_generation_gate.js');
const G=global.HookLabEvidenceGate;
function assert(x,msg){if(!x)throw new Error(msg||'assertion failed');}
let r;
r=G.generationDecision({mode:'SCIENTIFIC',scientific_d_unlocked:false,rules:[]});assert(!r.allowed&&r.reason==='SCIENTIFIC_D_LOCKED','scientific lock must fail closed');
r=G.generationDecision({mode:'EXPLORATORY',source:'GENERAL_COMPOSITIONAL_INTUITION',claim_as_corpus_evidence:false});assert(!r.allowed&&r.reason==='UNSUPPORTED_GENERATIVE_SOURCE','untraced intuition must be blocked');
r=G.generationDecision({mode:'EXPLORATORY',source:'AUTHOR_PROVIDED',claim_as_corpus_evidence:false});assert(r.allowed&&r.scope==='D0_EXPLORATORY','exploratory human-grounded generation may run without scientific claim');
const rule={state:'CONDITIONED_RULE',strength:'STAT_SUPPORTED',source_case_ids:['C001','C002'],feature_ids:['MEL_X'],analysis_id:'AN-1',rule_id:'R-1',engine_version:'1.0',generative_eligible:true,validation_status:'PASS'};
r=G.validateRule(rule);assert(r.allowed,'admitted conditioned rule should pass');
const ev={epistemic_state:'CANONICAL_ADMITTED',provenance:{source_case_ids:['C001'],feature_ids:['MEL_X'],analysis_id:'AN-1',engine_version:'1.0'}};
r=G.generationDecision({mode:'SCIENTIFIC',scientific_d_unlocked:true,rules:[rule],evidence:[ev]});assert(r.allowed&&r.scope==='SCIENTIFIC_GENERATION','fully admitted scientific generation should pass');
r=G.lyricDecision({author_input:{source:'AUTHOR_PROVIDED',answers:{theme:'x'}},music_constraints:{melody_case_id:'C001',feature_ids:['MEL_X'],engine_version:'1.0'},claim_as_corpus_finding:false});assert(r.allowed,'lyric constrained assistance should pass');
r=G.lyricDecision({author_input:null,music_constraints:{melody_case_id:'C001',feature_ids:['MEL_X'],engine_version:'1.0'}});assert(!r.allowed&&r.reason==='AUTHOR_INPUT_REQUIRED','lyric generation must require author input');
console.log('HOOKLAB_EVIDENCE_GATE_TEST_PASS');