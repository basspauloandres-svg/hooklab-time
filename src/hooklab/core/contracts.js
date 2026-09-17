export const EvidenceLevel = Object.freeze({
  OBSERVATION: 'OBSERVATION',
  ASSOCIATION: 'ASSOCIATION',
  REPLICATED_ASSOCIATION: 'REPLICATED_ASSOCIATION',
  EXPERIMENTAL_EFFECT: 'EXPERIMENTAL_EFFECT',
  REPLICATED_EFFECT: 'REPLICATED_EFFECT',
  PREDICTIVE_FEATURE: 'PREDICTIVE_FEATURE'
});

export function temporalEvent({ timestampMs, type, source, payload = {}, provenance = {} }) {
  if (!Number.isFinite(timestampMs) || timestampMs < 0) throw new TypeError('timestampMs must be a non-negative finite number');
  if (!type || !source) throw new TypeError('type and source are required');
  return Object.freeze({ timestampMs, type, source, payload: Object.freeze({ ...payload }), provenance: Object.freeze({ ...provenance }) });
}

export function audienceObservation({ sessionId, songId, versionId, experimentId = null, event }) {
  if (!sessionId || !songId || !versionId || !event) throw new TypeError('sessionId, songId, versionId and event are required');
  return Object.freeze({ sessionId, songId, versionId, experimentId, event });
}

export function musicalStimulus({ songId, versionId, durationMs, events, provenance = {} }) {
  if (!songId || !versionId || !Number.isFinite(durationMs) || durationMs <= 0) throw new TypeError('invalid musical stimulus');
  return Object.freeze({ songId, versionId, durationMs, events: Object.freeze([...events]), provenance: Object.freeze({ ...provenance }) });
}

export function evidenceRecord({ evidenceId, outcome, feature, level = EvidenceLevel.OBSERVATION, sampleSize, estimate = null, uncertainty = null, context = {}, provenance = {} }) {
  if (!evidenceId || !outcome || !feature || !Number.isInteger(sampleSize) || sampleSize < 1) throw new TypeError('invalid evidence record');
  return Object.freeze({ evidenceId, outcome, feature, level, sampleSize, estimate, uncertainty, context: Object.freeze({ ...context }), provenance: Object.freeze({ ...provenance }) });
}
