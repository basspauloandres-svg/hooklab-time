const REQUIRED = ['releaseId','trackId','platform','metric','value','observedAt','source'];

function required(input, key) {
  const value = input?.[key];
  if (value === undefined || value === null || value === '') throw new TypeError(`platform observation requires ${key}`);
  return value;
}

export function createPlatformObservation(input) {
  for (const key of REQUIRED) required(input, key);
  if (!Number.isFinite(input.value)) throw new TypeError('platform observation value must be finite');
  const observedAt = new Date(input.observedAt);
  if (Number.isNaN(observedAt.getTime())) throw new TypeError('platform observation observedAt must be ISO-compatible');

  return Object.freeze({
    releaseId: String(input.releaseId),
    trackId: String(input.trackId),
    audioVersionId: input.audioVersionId ? String(input.audioVersionId) : null,
    platform: String(input.platform).toLowerCase(),
    metric: String(input.metric),
    value: input.value,
    unit: input.unit ?? 'count',
    observedAt: observedAt.toISOString(),
    periodStart: input.periodStart ?? null,
    periodEnd: input.periodEnd ?? null,
    territory: input.territory ?? null,
    audienceSegment: input.audienceSegment ?? null,
    exposureContext: input.exposureContext ?? null,
    source: String(input.source),
    collectionMethod: input.collectionMethod ?? 'unknown',
    sourceSchemaVersion: input.sourceSchemaVersion ?? null,
    canonicalSchemaVersion: '1.0.0'
  });
}

export function platformObservationKey(observation) {
  const o = createPlatformObservation(observation);
  return [o.releaseId,o.trackId,o.audioVersionId??'-',o.platform,o.metric,o.periodStart??'-',o.periodEnd??'-',o.territory??'-',o.audienceSegment??'-',o.observedAt].join('|');
}
