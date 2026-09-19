import { behavioralChangePoints } from './behavioral_change_points.js';
import { explainBehavioralPeak } from './explain_behavioral_peak.js';
import { summarizeMusicalContext } from './musical_context_summary.js';

export function behaviorMusicChain({observations,stimulus,eventTypes=['skip','stop'],binMs=1000,minAtRisk=1,lookbackMs=5000,lookaheadMs=2000}){
  const relevant=observations.filter(o=>o.songId===stimulus.songId&&o.versionId===stimulus.versionId);
  const changePoints=behavioralChangePoints({observations:relevant,eventTypes,binMs,minAtRisk});
  const explanation=explainBehavioralPeak({changePointResult:changePoints,observations:relevant,stimulus,eventTypes,lookbackMs,lookaheadMs});
  if(!changePoints.peak) return Object.freeze({changePoints,peak:null,musicalContext:null,inferenceLevel:'NO_BEHAVIORAL_PEAK'});
  const behavioralTimestampMs=changePoints.peak.startMs+(changePoints.peak.endMs-changePoints.peak.startMs)/2;
  const musicalContext=summarizeMusicalContext({aligned:explanation.musicalContext,behavioralTimestampMs,lookbackMs,lookaheadMs});
  return Object.freeze({
    question:'What was occurring musically around the strongest observed behavioral hazard window?',
    changePoints,
    peak:changePoints.peak,
    audienceEvents:explanation.audienceEvents,
    musicalContext,
    inferenceLevel:'DESCRIPTIVE_TEMPORAL_ASSOCIATION',
    causalClaim:false
  });
}
