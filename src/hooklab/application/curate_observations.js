import { validateObservationBatch } from './observation_quality_gate.js';

export function curateObservations(inputs,metricRegistry){
  if(!metricRegistry) throw new TypeError('curation requires metricRegistry');
  const structural=validateObservationBatch(inputs);
  const accepted=[];
  const rejected=[...structural.rejected];
  for(const item of structural.accepted){
    try{
      const definition=metricRegistry.validate(item.observation);
      accepted.push(Object.freeze({...item,metricDefinition:definition}));
    }catch(error){
      rejected.push(Object.freeze({key:item.key,reason:error.message}));
    }
  }
  return Object.freeze({
    accepted:Object.freeze(accepted),
    rejected:Object.freeze(rejected),
    stats:Object.freeze({received:inputs.length,accepted:accepted.length,rejected:rejected.length})
  });
}
