export function createFeatureRecord(input){
  if(!input?.trackId || !input?.audioVersionId || !input?.featureName || !input?.extractorVersion) throw new TypeError('feature record requires trackId, audioVersionId, featureName and extractorVersion');
  if(!Number.isFinite(input.value)) throw new TypeError('feature value must be finite');
  const start=Number(input.timeStart ?? 0);
  const end=Number(input.timeEnd ?? start);
  if(!Number.isFinite(start)||!Number.isFinite(end)||start<0||end<start) throw new TypeError('invalid feature time range');
  return Object.freeze({
    trackId:String(input.trackId),audioVersionId:String(input.audioVersionId),featureSetId:String(input.featureSetId ?? 'default'),
    timeStart:start,timeEnd:end,featureName:String(input.featureName),value:input.value,unit:input.unit ?? null,
    confidence:input.confidence ?? null,extractor:String(input.extractor ?? 'time-mie'),extractorVersion:String(input.extractorVersion),
    createdAt:new Date(input.createdAt ?? Date.now()).toISOString(),schemaVersion:'1.0.0'
  });
}

export function featureRecordKey(record){
  const r=createFeatureRecord(record);
  return [r.trackId,r.audioVersionId,r.featureSetId,r.timeStart,r.timeEnd,r.featureName,r.extractor,r.extractorVersion].join('|');
}
