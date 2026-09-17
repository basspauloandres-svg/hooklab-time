import { alignStimulusResponse } from '../core/alignment.js';
import { evidenceRecord, EvidenceLevel } from '../core/contracts.js';

export async function observeBehavior({ stimulusPort, audiencePort, evidenceRepository, stimulusInput, experimentId, outcomeEventType, evidenceId, lookbackMs = 5000, lookaheadMs = 2000 }) {
  const stimulus = await stimulusPort.analyze(stimulusInput);
  const observations = await audiencePort.listByExperiment(experimentId);
  const target = observations.filter(o => o.event.type === outcomeEventType && o.songId === stimulus.songId && o.versionId === stimulus.versionId);
  const aligned = alignStimulusResponse({ stimulusEvents: stimulus.events, audienceEvents: target, lookbackMs, lookaheadMs });

  const featureCounts = new Map();
  for (const row of aligned) {
    for (const event of row.coincidentStimulusEvents) {
      featureCounts.set(event.type, (featureCounts.get(event.type) || 0) + 1);
    }
  }

  const records = [];
  for (const [feature, count] of featureCounts) {
    const record = evidenceRecord({
      evidenceId: `${evidenceId}:${feature}`,
      outcome: outcomeEventType,
      feature,
      level: EvidenceLevel.OBSERVATION,
      sampleSize: target.length,
      estimate: { coincidentCount: count, proportion: target.length ? count / target.length : null },
      context: { experimentId, songId: stimulus.songId, versionId: stimulus.versionId, lookbackMs, lookaheadMs },
      provenance: { method: 'temporal-window-alignment', inference: 'descriptive-observation' }
    });
    await evidenceRepository.save(record);
    records.push(record);
  }
  return Object.freeze({ stimulus, observations: Object.freeze(target), aligned: Object.freeze(aligned), evidence: Object.freeze(records) });
}
