import test from 'node:test';
import assert from 'node:assert/strict';
import { temporalEvent, audienceObservation, musicalStimulus } from '../src/hooklab/core/contracts.js';
import { behavioralChangePoints } from '../src/hooklab/application/behavioral_change_points.js';
import { explainBehavioralPeak } from '../src/hooklab/application/explain_behavioral_peak.js';

const obs=(sessionId,t,type)=>audienceObservation({sessionId,songId:'S',versionId:'A',experimentId:'E',event:temporalEvent({timestampMs:t,type,source:'ListeningLab'})});

test('behavioral peak is detected before musical context is requested',()=>{
 const observations=[obs('1',0,'play'),obs('1',10000,'skip'),obs('2',0,'play'),obs('2',10500,'skip'),obs('3',0,'play'),obs('3',30000,'complete')];
 const changes=behavioralChangePoints({observations,binMs:1000});
 assert.equal(changes.peak.startMs,10000);
 assert.equal(changes.peak.events,2);
 const stimulus=musicalStimulus({songId:'S',versionId:'A',durationMs:30000,events:[temporalEvent({timestampMs:9500,type:'transition',source:'TIME-MIE'}),temporalEvent({timestampMs:10000,type:'chorus_entry',source:'TIME-MIE'})]});
 const explained=explainBehavioralPeak({changePointResult:changes,observations,stimulus,lookbackMs:1000,lookaheadMs:500});
 assert.equal(explained.audienceEvents.length,2);
 assert.ok(explained.musicalContext.every(x=>x.coincidentStimulusEvents.some(e=>e.type==='chorus_entry')));
 assert.equal(explained.inferenceLevel,'TEMPORAL_ASSOCIATION');
});
