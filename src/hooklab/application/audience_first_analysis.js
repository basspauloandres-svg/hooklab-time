import { kaplanMeier, discreteHazard } from './retention.js';
import { summarizeOutcomes } from './outcomes.js';
import { alignStimulusResponse } from '../core/alignment.js';

export function audienceFirstAnalysis({ observations, stimulus, targetEventTypes=['skip','stop'], lookbackMs=5000, lookaheadMs=2000 }) {
  const relevant = observations.filter(o => o.songId === stimulus.songId && o.versionId === stimulus.versionId);
  const retention = kaplanMeier({ observations: relevant, durationMs: stimulus.durationMs });
  const hazard = discreteHazard(retention);
  const outcomes = summarizeOutcomes(relevant);
  const target = relevant.filter(o => targetEventTypes.includes(o.event.type));
  const aligned = alignStimulusResponse({ stimulusEvents: stimulus.events, audienceEvents: target, lookbackMs, lookaheadMs });

  return Object.freeze({
    question: 'What audience behavior occurred, when did it occur, and what musical events coincided with it?',
    population: Object.freeze({ sessions: new Set(relevant.map(o=>o.sessionId)).size, observations: relevant.length }),
    outcomes,
    retention,
    hazard,
    behavioralEvents: Object.freeze(target),
    temporalAlignment: Object.freeze(aligned),
    inferenceLevel: 'DESCRIPTIVE_ASSOCIATION_ONLY'
  });
}
