const assert=require('assert');
const fs=require('fs');
const path=require('path');
const Stats=require('../app/prototype_v1/lyric_statistical_model_contract.js');

const registry=JSON.parse(fs.readFileSync(path.join(__dirname,'../data/lyric_modeling/lyric_narrative_feature_registry_v0_1.json'),'utf8'));
const audit=Stats.auditRegistry(registry);

assert.equal(registry.scope_authority.scope_conflict_status,'NO_CONFLICT_DETECTED');
assert.equal(registry.source_audit.status,'CANONICAL_SOURCE_RESOLVED_FEATURE_TABLE_NOT_BUILT');
assert.equal(registry.source_audit.source_revision,'72');
assert.equal(registry.source_audit.repository_history_checked,true);
assert.equal(registry.source_audit.podlc_process_reopened,false);
assert.equal(registry.source_audit.m9_process_reopened,false);
assert.deepEqual(registry.inventory_A_to_F.D_COMPUTATIONALLY_DERIVED.present_and_validated,[]);
assert.equal(audit.total_features,9);
assert.equal(audit.counts.AUDIT_FEATURE_NOT_DEFINED,7);
assert.equal(audit.counts.FROZEN_NO_REPROCESS,2);
assert.equal(audit.counts.FEATURE_ADMISSIBLE||0,0);
assert.equal(audit.analysis_registration_unlocked,false);

for(const feature of registry.features){
  for(const field of Stats.REQUIRED_FEATURE) assert(Object.prototype.hasOwnProperty.call(feature,field),`${feature.feature_id}: missing ${field}`);
  if(feature.inventory_class==='B_CANDIDATE_REQUIRES_OPERATIONALIZATION'){
    assert.equal(Stats.admitFeature(feature).status,'AUDIT_FEATURE_NOT_DEFINED');
    assert.notEqual(feature.provider,'POD-LC');
  }
}

assert.equal(registry.analysis_registration.status,'BLOCKED_NO_ADMISSIBLE_FEATURE');
assert.deepEqual(registry.analysis_registration.registered_analysis_ids,[]);
assert.deepEqual(registry.analysis_registration.blocked_analysis_candidates,['AN-LNR-POV-DESC-001']);
assert.equal(registry.analysis_registration.human_trend_override_allowed,false);
assert.equal(registry.analysis_registration.statistical_tests_executed,false);
assert.equal(registry.analysis_registration.conditioned_deductions_created,false);
assert.equal(registry.analysis_registration.evidence_assisted_story_brief_unlocked,false);
console.log('LYRIC_NARRATIVE_FEATURE_REGISTRY_AUDIT_PASS');
