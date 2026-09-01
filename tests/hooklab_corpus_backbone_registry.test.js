const assert=require('assert');
const fs=require('fs');
const path=require('path');

const registry=JSON.parse(fs.readFileSync(path.join(__dirname,'../data/lyric_modeling/hooklab_corpus_backbone_registry_v1.json'),'utf8'));
const caseManifest=JSON.parse(fs.readFileSync(path.join(__dirname,'../data/lyric_modeling/hooklab_corpus_case_metadata_manifest_v1.json'),'utf8'));
const assets=registry.assets;
const byId=Object.fromEntries(assets.map(asset=>[asset.asset_id,asset]));

assert.equal(registry.schema,'HOOKLAB_CORPUS_BACKBONE_REGISTRY_v1');
assert.equal(registry.status,'CANONICAL_INTERNAL_RESEARCH_SOURCE_RESOLVED');
assert.equal(registry.source_resolution.canonical_source_resolved,true);
assert.equal(registry.source_resolution.canonical_asset_id,'HB-SRC-LYR-001');
assert.equal(registry.source_resolution.resolution_basis.provider_ids_exact_match,true);
assert.equal(registry.source_resolution.resolution_basis.canonical_source_revision,'72');
assert.equal(registry.canonical_identity_backbone.namespace,'HOOKLAB_C001_C100');
assert.equal(registry.canonical_identity_backbone.expected_case_count,100);
assert.equal(new Set(assets.map(asset=>asset.asset_id)).size,assets.length,'asset_id must be unique');

for(const asset of assets){
  assert.equal(asset.canonical_for_inference,false,`${asset.asset_id} must fail closed`);
  assert.equal(asset.contains_original_lyrics_in_registry,false,`${asset.asset_id} must not embed lyrics`);
  assert(Array.isArray(asset.classes)&&asset.classes.length>0,`${asset.asset_id} must have an A-F class`);
  assert(asset.boundary,`${asset.asset_id} must declare its boundary`);
}

assert.equal(byId['HB-SRC-LYR-001'].role,'CANONICAL_INTERNAL_RESEARCH_SOURCE');
assert.equal(byId['HB-SRC-LYR-001'].canonical_source,true);
assert.equal(byId['HB-SRC-LYR-001'].coverage.commercial_reference_cases,100);
assert.equal(byId['HB-VIEW-LYR-001'].role,'FROZEN_BASELINE_DOCUMENTARY_MIRROR');
assert.equal(byId['HB-VIEW-LYR-001'].mirrors_canonical_asset,'HB-SRC-LYR-001');
assert.equal(byId['HB-VIEW-LYR-001'].coverage.documentary_records_with_provider_ids,100);
assert.equal(byId['HB-VIEW-LYR-001'].coverage.editorial_authorization_status,'PENDING_VERIFICATION');
assert.equal(byId['HB-VIEW-LYR-001'].identity_namespace,byId['HB-SRC-LYR-001'].identity_namespace);
assert.equal(byId['HB-VIEW-OBS-001'].coverage.eligible_records,186);
assert.equal(byId['HB-MOD-MIDI-001'].coverage.indexed_cases,100);
assert.equal(byId['HB-MOD-MIDI-001'].coverage.recovered_midi,68);
assert.equal(byId['HB-MOD-MIDI-001'].coverage.selected_melody_candidates,67);
assert.equal(byId['HB-MOD-MIDI-001'].generation_class,'D0_EXPLORATORY');
assert.equal(byId['HB-MOD-MIDI-001'].scientific_d_unlocked,false);
assert.equal(byId['HB-PODLC-HISTORICAL-MATRICES-001'].role,'HISTORICAL_PODLC_DERIVED_VIEWS');
assert.equal(byId['HB-PODLC-HISTORICAL-MATRICES-001'].coverage.workbooks,3);
assert.equal(byId['HB-PODLC-M8-DRAFTS-001'].analysis_status,'HISTORICAL_DRAFT_NO_REPROCESS');
assert.equal(byId['HB-SAMPLE-TIME-001'].identity_namespace,'HOOKLAB_TIME_SAMPLE_1');
assert.equal(byId['HB-FROZEN-RESULTS-001'].analysis_status,'FROZEN_NO_REPROCESS');
assert.equal(byId['HB-AUX-CORPORA-001'].role,'AUXILIARY_CORPUS');
assert.equal(byId['HB-TEST-LAKH-001'].role,'TEST_LANE_ONLY');
assert.equal(byId['HB-TEST-LAKH-001'].scientific_d_unlocked,false);
assert.equal(byId['HB-NONCORPUS-OUTPUTS-001'].analysis_status,'EXCLUDED_FROM_CORPUS');

assert.equal(registry.analysis_gate.feature_admissibility_unlocked,false);
assert.equal(registry.analysis_gate.analysis_registration_unlocked,false);
assert.equal(registry.analysis_gate.statistical_engine_implemented,true);
assert.equal(registry.analysis_gate.human_trend_override_allowed,false);
assert.equal(registry.analysis_gate.statistical_tests_executed_by_this_registry,false);
assert.equal(registry.analysis_gate.conditioned_deductions_created,false);
assert.equal(registry.analysis_gate.evidence_assisted_story_brief_unlocked,false);
assert.equal(registry.analysis_gate.generation_class,'D0_EXPLORATORY');
assert.equal(registry.analysis_gate.scientific_d_unlocked,false);
assert.equal(registry.analysis_gate.next_gate,'HUMAN_REVIEW_LANGUAGE_PROPOSALS_AND_RESOLVE_DOCUMENT_VERSION_STATUS_FOR_99_ELIGIBLE_CASES');

for(const value of Object.values(registry.no_reprocess)) assert.equal(value,false);
assert(registry.ai_role.allowed.includes('map case identifiers across modalities'));
assert(registry.ai_role.forbidden.includes('create an empirical trend'));
assert.equal(registry.deduplication_rules.length,5);

assert.equal(caseManifest.schema,'HOOKLAB_CORPUS_CASE_METADATA_MANIFEST_v1');
assert.equal(caseManifest.status,'IDENTITY_MAPPING_COMPLETE_CANONICAL_SOURCE_RESOLVED');
assert.equal(caseManifest.source_workbook_revision,'72');
assert.equal(caseManifest.resolution_basis.canonical_asset_id,'HB-SRC-LYR-001');
assert.equal(caseManifest.coverage.expected_cases,100);
assert.equal(caseManifest.coverage.mapped_cases,100);
assert.deepEqual(caseManifest.coverage.missing_case_ids,[]);
assert.equal(caseManifest.coverage.lrclib_provider_records,100);
assert.equal(caseManifest.coverage.provider_ids_present,100);
assert.equal(caseManifest.coverage.editorial_status_pending,100);
assert.equal(caseManifest.coverage.editorial_alert_cases,10);
assert.equal(caseManifest.coverage.genre_pending,80);
assert.equal(caseManifest.coverage.year_pending,81);
assert.equal(caseManifest.coverage.document_incomplete_cases,1);
assert.equal(caseManifest.coverage.maximum_feature_calibration_frame_before_other_gates,99);
assert.equal(caseManifest.records.length,100);
assert.equal(new Set(caseManifest.records.map(record=>record.case_id)).size,100);
assert(!caseManifest.source_ranges_read.some(range=>range.includes('I:I')));
for(const record of caseManifest.records){
  assert.equal(record.lyric_text_in_manifest,false);
  assert.equal(record.internal_research_source_status,'CANONICAL_SOURCE_RECORD');
  assert.equal(record.public_redistribution_status,'BLOCKED_EDITORIAL_REVIEW');
  assert(record.provider_id);
  assert(!Object.prototype.hasOwnProperty.call(record,'lyrics'));
  assert(!Object.prototype.hasOwnProperty.call(record,'lyric_text'));
}
assert.equal(caseManifest.records.filter(record=>record.analysis_eligibility==='BLOCKED_FEATURE_ADMISSIBILITY').length,99);
const c077=caseManifest.records.find(record=>record.case_id==='C077');
assert.equal(c077.analysis_eligibility,'AUDIT_SOURCE_DOCUMENT_INCOMPLETE');
assert.equal(c077.integrity_audit.recovery_status,'NOT_RECOVERABLE_FROM_EXISTING_INTERNAL_COPIES');

console.log('HOOKLAB_CORPUS_BACKBONE_REGISTRY_PASS');
