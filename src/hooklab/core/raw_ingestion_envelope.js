import { createHash } from 'node:crypto';

function stableJson(value) {
  if (Array.isArray(value)) return `[${value.map(stableJson).join(',')}]`;
  if (value && typeof value === 'object') {
    return `{${Object.keys(value).sort().map(k => `${JSON.stringify(k)}:${stableJson(value[k])}`).join(',')}}`;
  }
  return JSON.stringify(value);
}

function digest(value) {
  return createHash('sha256').update(stableJson(value)).digest('hex');
}

export function createRawIngestionEnvelope(input) {
  if (!input?.source || !input?.collectedAt || input.payload === undefined) {
    throw new TypeError('raw ingestion envelope requires source, collectedAt and payload');
  }
  const collectedAt = new Date(input.collectedAt);
  if (Number.isNaN(collectedAt.getTime())) throw new TypeError('collectedAt must be ISO-compatible');
  const payloadHash = digest(input.payload);
  return Object.freeze({
    ingestionId: input.ingestionId ?? `${String(input.source).toLowerCase()}:${payloadHash}`,
    source: String(input.source).toLowerCase(),
    sourceEntityId: input.sourceEntityId ?? null,
    collectedAt: collectedAt.toISOString(),
    sourceSchemaVersion: input.sourceSchemaVersion ?? null,
    payloadHash,
    payload: structuredClone(input.payload),
    envelopeSchemaVersion: '1.0.0'
  });
}
