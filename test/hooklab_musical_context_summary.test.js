import test from 'node:test';
import assert from 'node:assert/strict';
import { summarizeMusicalContext } from '../src/hooklab/application/musical_context_summary.js';

test('summarizes typed musical events around a behavioral timestamp',()=>{
 const aligned=[
  {stimulusEvent:{timestampMs:7000,type:'section_change',label:'pre'}},
  {stimulusEvent:{timestampMs:9500,type:'harmonic_change'}},
  {stimulusEvent:{timestampMs:10000,type:'hook_onset'}},
  {stimulusEvent:{timestampMs:11500,type:'harmonic_change'}},
  {stimulusEvent:{timestampMs:14000,type:'late'}}
 ];
 const result=summarizeMusicalContext({aligned,behavioralTimestampMs:10000,lookbackMs:2000,lookaheadMs:2000});
 assert.equal(result.eventCount,3);
 assert.equal(result.byType.harmonic_change,2);
 assert.equal(result.byType.hook_onset,1);
 assert.equal(result.nearest.type,'hook_onset');
 assert.equal(result.nearest.offsetMs,0);
 assert.equal(result.inferenceLevel,'DESCRIPTIVE_TEMPORAL_CONTEXT');
});

test('empty musical context stays explicit',()=>{
 const result=summarizeMusicalContext({aligned:[],behavioralTimestampMs:5000});
 assert.equal(result.eventCount,0);
 assert.equal(result.nearest,null);
 assert.deepEqual(result.byType,{});
});

test('accepts direct events and rejects invalid behavioral time',()=>{
 const result=summarizeMusicalContext({aligned:[{timeMs:900,type:'beat'}],behavioralTimestampMs:1000,lookbackMs:200,lookaheadMs:0});
 assert.equal(result.eventCount,1);
 assert.equal(result.nearest.offsetMs,-100);
 assert.throws(()=>summarizeMusicalContext({aligned:[],behavioralTimestampMs:-1}),/behavioralTimestampMs/);
});
