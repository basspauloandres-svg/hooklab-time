import { temporalEvent, audienceObservation, musicalStimulus } from '../core/contracts.js';
import { StaticStimulusAdapter } from '../adapters/static_stimulus.js';
import { MemoryAudienceEvents } from '../adapters/memory_audience_events.js';
import { MemoryEvidenceRepository } from '../adapters/memory_evidence_repository.js';
import { observeBehavior } from './observe_behavior.js';
import { kaplanMeier, discreteHazard } from './retention.js';

export async function runVerticalSlice() {
  const songId='MANIZALES'; const versionId='P04'; const experimentId='M0';
  const stimulus = musicalStimulus({ songId, versionId, durationMs: 40000, events:[
    temporalEvent({timestampMs:12000,type:'vocal_entry',source:'TIME-MIE'}),
    temporalEvent({timestampMs:27000,type:'density_drop',source:'TIME-MIE'}),
    temporalEvent({timestampMs:29000,type:'section_transition',source:'TIME-MIE'})
  ]});
  const seed = [
    audienceObservation({sessionId:'s1',songId,versionId,experimentId,event:temporalEvent({timestampMs:28000,type:'skip',source:'ListeningLab'})}),
    audienceObservation({sessionId:'s2',songId,versionId,experimentId,event:temporalEvent({timestampMs:30000,type:'skip',source:'ListeningLab'})}),
    audienceObservation({sessionId:'s3',songId,versionId,experimentId,event:temporalEvent({timestampMs:40000,type:'complete',source:'ListeningLab'})})
  ];
  const audiencePort = new MemoryAudienceEvents(seed);
  const evidenceRepository = new MemoryEvidenceRepository();
  const result = await observeBehavior({ stimulusPort:new StaticStimulusAdapter(stimulus), audiencePort, evidenceRepository, stimulusInput:{songId,versionId}, experimentId, outcomeEventType:'skip', evidenceId:'M0-SKIP' });
  const km = kaplanMeier({ observations:seed, durationMs:stimulus.durationMs });
  return { result, retention:km, hazard:discreteHazard(km), evidence:await evidenceRepository.find({outcome:'skip'}) };
}
