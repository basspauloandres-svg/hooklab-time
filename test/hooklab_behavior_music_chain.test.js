import test from 'node:test';
import assert from 'node:assert/strict';
import { temporalEvent, audienceObservation, musicalStimulus } from '../src/hooklab/core/contracts.js';
import { behaviorMusicChain } from '../src/hooklab/application/behavior_music_chain.js';

const obs=(sessionId,type,t)=>audienceObservation({sessionId,songId:'S',versionId:'A',experimentId:'E',event:temporalEvent({timestampMs:t,type,source:'ListeningLab'})});

test('behavioral peak is located before musical context is summarized',()=>{
 const stimulus=musicalStimulus({songId:'S',versionId:'A',durationMs:30000,events:[
  temporalEvent({timestampMs:8500,type:'transition',source:'TIME-MIE'}),
  temporalEvent({timestampMs:9500,type:'hook_onset',source:'TIME-MIE'}),
  temporalEvent({timestampMs:12000,type:'section_change',source:'TIME-MIE'})
 ]});
 const observations=[
  obs('1','play',0),obs('1','skip',9600),
  obs('2','play',0),obs('2','skip',9700),
  obs('3','play',0),obs('3','complete',30000),
  obs('4','play',0),obs('4','complete',30000)
 ];
 const result=behaviorMusicChain({observations,stimulus,binMs:1000,lookbackMs:2000,lookaheadMs:1000});
 assert.equal(result.peak.startMs,9000);
 assert.equal(result.peak.events,2);
 assert.equal(result.audienceEvents.length,2);
 assert.equal(result.musicalContext.byType.hook_onset,2);
 assert.equal(result.musicalContext.byType.transition,2);
 assert.equal(result.causalClaim,false);
 assert.equal(result.inferenceLevel,'DESCRIPTIVE_TEMPORAL_ASSOCIATION');
});

test('absence of abandonment produces no invented musical explanation',()=>{
 const stimulus=musicalStimulus({songId:'S',versionId:'A',durationMs:10000,events:[temporalEvent({timestampMs:5000,type:'hook',source:'TIME-MIE'})]});
 const result=behaviorMusicChain({observations:[obs('1','play',0),obs('1','complete',10000)],stimulus});
 assert.equal(result.peak,null);
 assert.equal(result.musicalContext,null);
 assert.equal(result.inferenceLevel,'NO_BEHAVIORAL_PEAK');
});
