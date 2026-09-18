import test from 'node:test';
import assert from 'node:assert/strict';
import { temporalEvent } from '../src/hooklab/core/contracts.js';
import { synchronizeHazardWithMusic, peakHazardContext } from '../src/hooklab/application/hazard_music_sync.js';

test('hazard is estimated first and musical context is attached afterwards',()=>{
 const hazard=[{timeMs:10000,hazard:0.2,atRisk:10,events:2},{timeMs:20000,hazard:0.5,atRisk:6,events:3}];
 const stimulusEvents=[temporalEvent({timestampMs:19000,type:'prechorus_end',source:'TIME-MIE'}),temporalEvent({timestampMs:20000,type:'chorus_entry',source:'TIME-MIE'})];
 const rows=synchronizeHazardWithMusic({hazard,stimulusEvents,lookbackMs:1500,lookaheadMs:500});
 const peak=peakHazardContext(rows);
 assert.equal(peak.timeMs,20000);
 assert.equal(peak.hazard,0.5);
 assert.deepEqual(peak.musicalEvents.map(x=>x.type),['prechorus_end','chorus_entry']);
 assert.equal(peak.inferenceLevel,'TEMPORAL_ASSOCIATION');
});
