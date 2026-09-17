export function cognitiveDescriptor({ timestampMs, name, value, model, uncertainty=null, provenance={} }) {
  if(!Number.isFinite(timestampMs)||timestampMs<0||!name||!model||!Number.isFinite(value)) throw new TypeError('invalid cognitive descriptor');
  return Object.freeze({timestampMs,name,value,model,uncertainty,provenance:Object.freeze({...provenance})});
}

export const CognitiveClaimLevel=Object.freeze({ STIMULUS_DESCRIPTOR:'STIMULUS_DESCRIPTOR', BEHAVIOR_ASSOCIATION:'BEHAVIOR_ASSOCIATION', EXPERIMENTAL_EVIDENCE:'EXPERIMENTAL_EVIDENCE' });
