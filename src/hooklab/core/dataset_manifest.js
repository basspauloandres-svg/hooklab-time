export function createDatasetManifest(input){
  if(!input?.datasetId||!input?.version||!input?.createdAt) throw new TypeError('dataset manifest requires datasetId, version and createdAt');
  const createdAt=new Date(input.createdAt);
  if(Number.isNaN(createdAt.getTime())) throw new TypeError('dataset createdAt must be ISO-compatible');
  const releases=[...(input.releases??[])].map(String).sort();
  const sources=[...(input.sources??[])].map(String).sort();
  return Object.freeze({
    datasetId:String(input.datasetId),version:String(input.version),kind:String(input.kind??'curated'),
    releases:Object.freeze(releases),sources:Object.freeze(sources),observationCount:Number(input.observationCount??0),
    featureCount:Number(input.featureCount??0),parentVersion:input.parentVersion??null,
    cutoffAt:input.cutoffAt?new Date(input.cutoffAt).toISOString():null,
    createdAt:createdAt.toISOString(),schemaVersion:'1.0.0'
  });
}

export function datasetManifestKey(manifest){
  const m=createDatasetManifest(manifest);
  return `${m.datasetId}@${m.version}`;
}
