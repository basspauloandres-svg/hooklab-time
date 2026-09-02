const assert=require('assert');
const crypto=require('crypto');
const fs=require('fs');
const path=require('path');
const root=path.resolve(__dirname,'..');
const registry=require(path.join(root,'data/music_modeling/mie_canonical_component_registry_v1.json'));

function fileSha(relative){
  return crypto.createHash('sha256').update(fs.readFileSync(path.join(root,relative))).digest('hex');
}
function assertPinned(artifact){
  assert(fs.existsSync(path.join(root,artifact.path)),`missing canonical artifact: ${artifact.path}`);
  assert.equal(fileSha(artifact.path),artifact.sha256,`canonical artifact changed without registry update: ${artifact.path}`);
}

assert.equal(registry.status,'RECOVERY_GATE_ACTIVE');
assert.equal(registry.product_semantics.primary_goal,'MUSICAL_RECOGNITION_FROM_TRACEABLE_TRANSCRIPTION');
assert.equal(registry.product_semantics.scientific_d_unlocked,false);
assert.deepEqual(registry.components.M.required_chain,[
  'PROBABILISTIC_F0','OCTAVE_PLANE_RESOLVER','R1_1_CONTINUITY','R1_2_DURATION_SEGMENTATION','R1_3_PITCH_CLASSIFICATION'
]);
assert(registry.components.M.forbidden_replacements.includes('FULL_MIX_GOERTZEL_WITHOUT_PLANE_RESOLVER'));
assert.deepEqual(registry.components.H.required_chain.slice(-2),['RESIDUAL_REQUERY','LOCK_AMBIGUOUS_ABSTAIN']);
assert.equal(registry.components.H.ai_boundary.may_create_absent_pitch_evidence,false);
assert.equal(registry.components.H.audible_output_required,true);
assert.equal(registry.components.T.status,'FROZEN_ENGINEERING_BASELINE');
assert.deepEqual(registry.integration.required_audible_layers,['melody','harmony_lock','beat_tactus']);
assert.equal(registry.known_integrations.find(x=>x.path.endsWith('v0.2.html')).status,'REJECTED_ENGINE_REGRESSION');
assert.equal(registry.accuracy_evidence.general_accuracy_claim_allowed,false);

assertPinned(registry.components.M.reference_runtime);
registry.components.H.reference_artifacts.forEach(assertPinned);
assertPinned(registry.components.T.reference_runtime);
assertPinned(registry.integration.reference_engine);
console.log('MIE_CANONICAL_COMPONENT_REGISTRY_PASS');
