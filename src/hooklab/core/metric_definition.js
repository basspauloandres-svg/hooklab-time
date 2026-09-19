const GRAINS=new Set(['release','audience_segment','content_time','session','unknown']);
const AGGREGATIONS=new Set(['count','sum','mean','ratio','rate','duration','distribution','unknown']);

export function createMetricDefinition(input){
  if(!input?.metricId || !input?.platform || !input?.name) throw new TypeError('metric definition requires metricId, platform and name');
  const grain=input.grain ?? 'unknown';
  const aggregation=input.aggregation ?? 'unknown';
  if(!GRAINS.has(grain)) throw new TypeError(`unsupported metric grain: ${grain}`);
  if(!AGGREGATIONS.has(aggregation)) throw new TypeError(`unsupported metric aggregation: ${aggregation}`);
  return Object.freeze({
    metricId:String(input.metricId),
    platform:String(input.platform).toLowerCase(),
    name:String(input.name),
    description:input.description ?? null,
    unit:input.unit ?? 'count',
    grain,
    aggregation,
    cumulative:Boolean(input.cumulative),
    temporalResolution:input.temporalResolution ?? null,
    sourceDefinition:input.sourceDefinition ?? null,
    schemaVersion:'1.0.0'
  });
}

export function assertObservationMatchesMetric(observation,definition){
  if(observation.platform!==definition.platform) throw new Error('METRIC_PLATFORM_MISMATCH');
  if(observation.metric!==definition.metricId) throw new Error('METRIC_ID_MISMATCH');
  if(observation.unit!==definition.unit) throw new Error('METRIC_UNIT_MISMATCH');
  return true;
}
