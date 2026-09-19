const LEVELS=new Set(['observation','statistical_result','association','prediction']);

export function createEvidenceRecord(input){
  if(!input?.evidenceId||!input?.releaseId||!input?.targetMetric||!input?.method||!input?.datasetVersion) throw new TypeError('evidence record requires evidenceId, releaseId, targetMetric, method and datasetVersion');
  const level=input.level ?? 'observation';
  if(!LEVELS.has(level)) throw new TypeError(`unsupported evidence level: ${level}`);
  return Object.freeze({
    evidenceId:String(input.evidenceId),releaseId:String(input.releaseId),trackId:input.trackId?String(input.trackId):null,
    targetMetric:String(input.targetMetric),level,method:String(input.method),estimate:input.estimate ?? null,
    intervalLow:input.intervalLow ?? null,intervalHigh:input.intervalHigh ?? null,sampleSize:input.sampleSize ?? null,
    datasetVersion:String(input.datasetVersion),featureSetVersion:input.featureSetVersion ?? null,modelVersion:input.modelVersion ?? null,
    conditions:Object.freeze({...input.conditions}),sourceRefs:Object.freeze([...(input.sourceRefs ?? [])]),
    createdAt:new Date(input.createdAt ?? Date.now()).toISOString(),schemaVersion:'1.0.0'
  });
}
