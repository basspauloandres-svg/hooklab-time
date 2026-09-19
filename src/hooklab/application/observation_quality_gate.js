import { createPlatformObservation, platformObservationKey } from '../core/platform_observation.js';

export function validateObservationBatch(inputs) {
  const accepted=[];
  const rejected=[];
  const seen=new Set();

  inputs.forEach((input,index)=>{
    try {
      const observation=createPlatformObservation(input);
      const key=platformObservationKey(observation);
      if(seen.has(key)) {
        rejected.push(Object.freeze({index,reason:'DUPLICATE_IN_BATCH',key}));
        return;
      }
      if(observation.value < 0 && observation.unit !== 'signed') {
        rejected.push(Object.freeze({index,reason:'NEGATIVE_VALUE',key}));
        return;
      }
      seen.add(key);
      accepted.push(Object.freeze({key,observation}));
    } catch(error) {
      rejected.push(Object.freeze({index,reason:'SCHEMA_INVALID',message:error.message}));
    }
  });

  return Object.freeze({
    accepted:Object.freeze(accepted),
    rejected:Object.freeze(rejected),
    stats:Object.freeze({received:inputs.length,accepted:accepted.length,rejected:rejected.length})
  });
}
