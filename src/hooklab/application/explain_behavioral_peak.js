import { alignStimulusResponse } from '../core/alignment.js';

export function explainBehavioralPeak({ changePointResult, observations, stimulus, eventTypes=['skip','stop'], lookbackMs=5000, lookaheadMs=2000 }) {
  const peak=changePointResult.peak;
  if(!peak) return Object.freeze({peak:null,audienceEvents:Object.freeze([]),musicalContext:Object.freeze([]),inferenceLevel:'NO_EVENT'});
  const audienceEvents=observations.filter(o=>eventTypes.includes(o.event.type)&&o.event.timestampMs>=peak.startMs&&o.event.timestampMs<peak.endMs);
  const musicalContext=alignStimulusResponse({stimulusEvents:stimulus.events,audienceEvents,lookbackMs,lookaheadMs});
  return Object.freeze({peak,audienceEvents:Object.freeze(audienceEvents),musicalContext:Object.freeze(musicalContext),inferenceLevel:'TEMPORAL_ASSOCIATION'});
}
