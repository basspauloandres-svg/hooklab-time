import { createMetricDefinition, assertObservationMatchesMetric } from './metric_definition.js';

export class MetricRegistry {
  #definitions=new Map();

  register(input){
    const definition=createMetricDefinition(input);
    const key=`${definition.platform}:${definition.metricId}`;
    const existing=this.#definitions.get(key);
    if(existing && JSON.stringify(existing)!==JSON.stringify(definition)) throw new Error('METRIC_DEFINITION_CONFLICT');
    this.#definitions.set(key,definition);
    return definition;
  }

  get(platform,metricId){ return this.#definitions.get(`${String(platform).toLowerCase()}:${metricId}`) ?? null; }

  validate(observation){
    const definition=this.get(observation.platform,observation.metric);
    if(!definition) throw new Error('UNKNOWN_METRIC');
    assertObservationMatchesMetric(observation,definition);
    return definition;
  }

  values(){ return Object.freeze([...this.#definitions.values()]); }
}
