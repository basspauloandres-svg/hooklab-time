import test from 'node:test';
import assert from 'node:assert/strict';
import { temporalEvent, audienceObservation, musicalStimulus } from '../src/hooklab/core/contracts.js';
import { audienceFirstAnalysis } from '../src/hooklab/application/audience_first_analysis.js';

test('analysis begins with audience behavior and only then aligns musical events', () => {
  const songId='S'; const versionId='A';
  const stimulus=musicalStimulus({songId,versionId,durationMs:30000,events:[
    temporalEvent({timestampMs:9000,type:'vocal_entry',source:'TIME-MIE'}),
    temporalEvent({timestampMs:19000,type:'chorus_entry',source:'TIME-MIE'})
  ]});
  const observations=[
    audienceObservation({sessionId:'1',songId,versionId,experimentId:'E',event:temporalEvent({timestampMs:0,type:'play',source:'ListeningLab'})}),
    audienceObservation({sessionId:'1',songId,versionId,experimentId:'E',event:temporalEvent({timestampMs:20000,type:'skip',source:'ListeningLab'})}),
    audienceObservation({sessionId:'2',songId,versionId,experimentId:'E',event:temporalEvent({timestampMs:0,type:'play',source:'ListeningLab'})}),
    audienceObservation({sessionId:'2',songId,versionId,experimentId:'E',event:temporalEvent({timestampMs:30000,type:'complete',source:'ListeningLab'})})
  ];
  const result=audienceFirstAnalysis({observations,stimulus,lookbackMs:2000,lookaheadMs:1000});
  assert.equal(result.population.sessions,2);
  assert.equal(result.behavioralEvents.length,1);
  assert.equal(result.behavioralEvents[0].event.type,'skip');
  assert.equal(result.temporalAlignment[0].coincidentStimulusEvents[0].type,'chorus_entry');
  assert.equal(result.inferenceLevel,'DESCRIPTIVE_ASSOCIATION_ONLY');
});
