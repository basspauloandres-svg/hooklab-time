const assert=require('assert');
const fs=require('fs');
const path=require('path');
const Stats=require('../app/prototype_v1/lyric_statistical_model_contract.js');
const Narrative=require('../app/prototype_v1/narrative_state_engine.js');
const AI=require('../app/prototype_v1/ai_coherence_reasoning_layer.js');
const Assistant=require('../app/prototype_v1/hook_composition_assistant.js');

// Feature gate is fail-closed.
assert.equal(Stats.admitFeature({feature_id:'X'}).status,'AUDIT_FEATURE_NOT_DEFINED');
const feature={feature_id:'NARR_POV',inventory_class:'D_COMPUTATIONALLY_DERIVED',construct:'narrative point of view',analytic_layer:'TEXT',operational_definition:'coded grammatical/narrative perspective',unit:'song',provider:'validated_provider',version:'v1',measurement_error:{status:'ESTIMATED'},calibration:{status:'CALIBRATION_PASS'},textual_relevance:'lyric narrative organization',musical_relevance:'section continuity only',research_question_enabled:'RQ-NARR',outcome:'predeclared_outcome',population:'predeclared_population',confounders:['genre'],forbidden_interpretations:['causality'],provenance:{source:'mapped_hooklab_corpus'}};
assert.equal(Stats.admitFeature(feature).status,'FEATURE_ADMISSIBLE');
const registry={analysis_id:'AN-NARR-001',research_question:'Is POV associated with outcome?',population_scope:'predeclared_population',outcome:'predeclared_outcome',admissible_feature_ids:['NARR_POV'],primary_tests:['predeclared_test'],covariates:['genre'],multiplicity_family:'narrative_family',effect_size_criterion:'predeclared',robustness_plan:'sensitivity+robustness',replication_requirement:'required_if_promoted',stop_promotion_rule:'fail_closed',expected_direction:null,trend_origin_policy:'REGISTERED_DATA_AND_STATISTICS_ONLY',human_trend_override_allowed:false,ai_trend_override_allowed:false,literature_sets_empirical_direction:false,producer_preference_used_as_evidence:false,source_revision:'TEST_REVISION',feature_registry_id:'TEST_REGISTRY'};
assert.equal(Stats.registerAnalysis(registry,{NARR_POV:feature}).status,'ANALYSIS_REGISTERED');
assert.equal(Stats.registerAnalysis({...registry,expected_direction:'positive'},{NARR_POV:feature}).status,'AUDIT_ANALYSIS_NOT_REGISTERED');
const computedResult={analysis_id:'AN-NARR-001',analysis_class:'confirmatory',robustness_status:'PASS',multiplicity_control_status:'PASS',effect_size_status:'MEETS_PREDECLARED_CRITERION',uncertainty_status:'ACCEPTABLE',replication_required:false,replication_status:'NOT_REQUIRED',computation_origin:'REGISTERED_STATISTICAL_ENGINE',trend_origin_policy:'REGISTERED_DATA_AND_STATISTICS_ONLY',human_trend_override_applied:false,ai_trend_override_applied:false,literature_direction_applied:false,producer_preference_applied:false,registration_hash_sha256:'abc',normalized_input_hash_sha256:'def',engine_version:'test-engine'};
assert.equal(Stats.finalize(computedResult).disposition,'PROMOTE_TO_CONDITIONED_DEDUCTION');
assert.equal(Stats.finalize({...computedResult,human_trend_override_applied:true}).disposition,'AUDIT');
assert.equal(Stats.finalize({...computedResult,computation_origin:'MANUAL'}).disposition,'AUDIT');

// Narrative state persists prior approved section history.
const brief={brief_id:'B1',characters:'Ana, Luis',relationship:'pareja',conflict:'traición',point_of_view:'primera persona',emotional_trajectory:'sospecha a confrontación'};
let ns=Narrative.fromBrief(brief);
assert.equal(ns.characters.length,2);
ns=Narrative.update(ns,{section_id:'S1',part:'verse',candidate:{plain_text:'algo cambió entre los dos'}},{});
assert.equal(ns.section_history.length,1);
assert.equal(Narrative.continuity(ns,'hook').status,'PASS');

// AI consumes only promoted deductions.
const candidate={text_candidate_id:'T1',plain_text:'algo cambió entre los dos',prosody_status:'GENERATED_PROSODY_CANDIDATE',fit:{melody_capacity_penalty:0}};
const ai=AI.evaluate({session_id:'S',story_brief:brief,narrative_state:ns,section_function:'verse',approved_sections:[],conditioned_deductions:[{id:'D1',disposition:'NO_PROMOTION'},{id:'D2',disposition:'PROMOTE_TO_CONDITIONED_DEDUCTION'}]},candidate);
assert.deepEqual(ai.evidence_ids_consumed,['D2']);
assert.equal(ai.evidence_ids_excluded.length,1);

// SECTION_FUNCTION must not leak into lyric tokens.
const dummyD0={schema:'D0',variants:[{variant:'thetic',events:Array(16).fill({})},{variant:'anacrustic',events:Array(16).fill({})},{variant:'syncopated',events:Array(16).fill({})}]};
const set=Assistant.generateCandidates({language:'es',section_function:'verse',intention:'Traición',theme:'Traición',reference_analysis:{tempo_bpm_median:107,beat_count:299},d0_manifest:dummyD0},3);
assert.equal(set.section_function,'verse');
for(const c of set.candidates) assert(!/\bverso\b/i.test(c.plain_text),'SECTION label leaked into lyric: '+c.plain_text);

// Canonical Studio must be syntactically whole at the document level and load modeling layers.
const studio=fs.readFileSync(path.join(__dirname,'../app/prototype_v1/studio.html'),'utf8');
assert(studio.includes('</html>'));
assert(studio.includes('lyric_statistical_model_contract.js'));
assert(studio.includes('narrative_state_engine.js'));
assert(studio.includes('ai_coherence_reasoning_layer.js'));
assert(studio.includes('STORY_BRIEF ≠ SECTION_FUNCTION ≠ LYRIC_CONTENT'));
console.log('LYRIC_MODELING_COHERENCE_CONTRACT_PASS');
