const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '..');
const read = p => JSON.parse(fs.readFileSync(path.join(root, p), 'utf8'));

const registry = read('data/music_modeling/melody_beat_feature_registry_v0_1.json');
const melody = read('data/music_modeling/melody_measurement_protocol_v0_1.json');
const beat = read('data/music_modeling/beat_rhythm_measurement_protocol_v0_1.json');
const analyses = [
  read('data/music_modeling/analysis_registry/AN-MEL-DESC-001.json'),
  read('data/music_modeling/analysis_registry/AN-BEAT-DESC-001.json')
];

if (registry.status !== 'FAIL_CLOSED_NO_ADMISSIBLE_MUSIC_FEATURES') throw new Error('registry must fail closed');
if (registry.boundaries.scientific_d_unlocked !== false) throw new Error('scientific_d must remain false');
if (registry.modality_inventory.melody.coverage.indexed_cases !== 100) throw new Error('melody index coverage drift');
if (registry.modality_inventory.melody.coverage.selected_melody_candidates !== 67) throw new Error('melody candidate coverage drift');
if (registry.modality_inventory.beat_rhythm.coverage.canonical_case_linked_real_audio !== 0) throw new Error('unverified beat source promoted');
if (!registry.features.every(f => !String(f.lifecycle_status).includes('ADMISSIBLE'))) throw new Error('feature admitted prematurely');
if (registry.cross_modal_gate.status !== 'BLOCKED') throw new Error('cross-modal gate must remain blocked');
if (melody.scientific_d_unlocked !== false || beat.scientific_d_unlocked !== false) throw new Error('protocol scientific_d drift');
if (melody.calibration_design.minimum_independent_aligned_pairs !== 30) throw new Error('melody calibration target drift');
if (melody.calibration_design.required_at_least_one_relevant_feature_spearman_rho !== 0.8) throw new Error('melody rho target drift');
if (!analyses.every(a => a.registration_status.startsWith('BLOCKED_') && a.expected_direction === null && a.statistical_computation_executed === false)) throw new Error('blocked analysis contract drift');
if (!analyses.every(a => a.human_trend_override_allowed === false && a.ai_trend_override_allowed === false && a.literature_sets_empirical_direction === false && a.producer_preference_used_as_evidence === false)) throw new Error('trend override boundary drift');

console.log('MUSIC_MODELING_CONTRACT_PASS');
