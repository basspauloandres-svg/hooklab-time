export function createDataLineage(input) {
  if (!input?.ingestionId || !input?.payloadHash || !input?.canonicalKey) {
    throw new TypeError('data lineage requires ingestionId, payloadHash and canonicalKey');
  }
  return Object.freeze({
    ingestionId:String(input.ingestionId),
    payloadHash:String(input.payloadHash),
    canonicalKey:String(input.canonicalKey),
    source:String(input.source ?? 'unknown'),
    transformer:String(input.transformer ?? 'canonical-observation'),
    transformerVersion:String(input.transformerVersion ?? '1.0.0'),
    createdAt:new Date(input.createdAt ?? Date.now()).toISOString(),
    schemaVersion:'1.0.0'
  });
}
