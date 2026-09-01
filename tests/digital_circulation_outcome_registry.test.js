const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '..');
const read = p => JSON.parse(fs.readFileSync(path.join(root, p), 'utf8'));

const registry = read('data/engagement_modeling/digital_circulation_outcome_registry_v0_1.json');
const analyses = [
  read('data/engagement_modeling/analysis_registry/AN-CIRC-MULTIMODAL-001.json'),
  read('data/engagement_modeling/analysis_registry/AN-RET-CHORUS-001.json'),
  read('data/engagement_modeling/analysis_registry/AN-THEME-TRAFFIC-001.json')
];

if (registry.status !== 'PROSPECTIVE_SOURCE_PARTIALLY_MAPPED_OUTCOME_NOT_ADMISSIBLE') throw new Error('circulation registry status drift');
if (registry.source_audit.records_collected !== 15) throw new Error('pilot snapshot coverage drift');
if (registry.source_audit.vidiq_total_credits !== 0) throw new Error('vidIQ credit audit drift');
if (registry.source_audit.verified_youtube_video_identities !== 15) throw new Error('YouTube identity coverage drift');
if (registry.source_audit.alternative_provider_status !== 'ACTIVE_QUOTA_FREE_15_OF_15_VERIFIED_SNAPSHOT_COMPLETE') throw new Error('public provider status drift');
if (registry.source_audit.complete_snapshot_series_points !== 1) throw new Error('pilot time-series count drift');
if (registry.source_audit.pilot_snapshot_in_inferential_window !== false) throw new Error('pilot/inference boundary drift');
if (registry.source_audit.provider_fields_forbidden.join(',') !== 'dislikes,rawDislikes,rawLikes,rating') throw new Error('estimated provider fields boundary drift');
if (registry.scientific_boundary.circulation_is_outcome_not_compositional_feature !== true) throw new Error('circulation role drift');
if (registry.scientific_boundary.public_view_count_is_traffic_peak !== false) throw new Error('snapshot/peak conflation');
if (registry.scientific_boundary.association_is_causal_incidence !== false) throw new Error('causal boundary drift');
if (registry.scientific_boundary.scientific_d_unlocked !== false) throw new Error('scientific_d must remain false');
if (!registry.outcomes.every(o => !['FEATURE_ADMISSIBLE', 'PROMOTE_TO_CONDITIONED_DEDUCTION'].includes(o.lifecycle_status))) throw new Error('outcome admitted prematurely');
if (!analyses.every(a => a.registration_status.startsWith('BLOCKED_') && a.expected_direction === null && a.causal_claim_allowed === false && a.statistical_computation_executed === false)) throw new Error('analysis must remain blocked');
if (!analyses.every(a => a.human_trend_override_allowed === false && a.ai_trend_override_allowed === false && a.literature_sets_empirical_direction === false && a.producer_preference_used_as_evidence === false)) throw new Error('trend override boundary drift');

console.log('DIGITAL_CIRCULATION_OUTCOME_REGISTRY_PASS');
