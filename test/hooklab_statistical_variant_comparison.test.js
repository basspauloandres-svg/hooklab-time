import test from 'node:test';
import assert from 'node:assert/strict';
import { temporalEvent, audienceObservation } from '../src/hooklab/core/contracts.js';
import { compareBinaryOutcome } from '../src/hooklab/application/statistical_variant_comparison.js';

const row=(sessionId,versionId,type,t=0)=>audienceObservation({sessionId,songId:'S',versionId,experimentId:'E',event:temporalEvent({timestampMs:t,type,source:'ListeningLab'})});

test('variant comparison reports observed effect and uncertainty without causal interpretation',()=>{
 const observations=[
  row('a1','A','play'),row('a1','A','complete',30000),row('a2','A','play'),row('a2','A','complete',30000),row('a3','A','play'),row('a3','A','skip',10000),
  row('b1','B','play'),row('b1','B','complete',30000),row('b2','B','play'),row('b2','B','skip',9000),row('b3','B','play'),row('b3','B','skip',11000)
 ];
 const result=compareBinaryOutcome({observations,versionA:'A',versionB:'B',outcomeTypes:['complete']});
 assert.equal(result.A.n,3); assert.equal(result.A.successes,2);
 assert.equal(result.B.n,3); assert.equal(result.B.successes,1);
 assert.ok(Math.abs(result.difference.estimate-1/3)<1e-12);
 assert.ok(result.difference.lower<result.difference.estimate&&result.difference.upper>result.difference.estimate);
 assert.equal(result.causalClaim,false);
 assert.equal(result.inferenceLevel,'STATISTICAL_COMPARISON');
});

test('empty variant is represented as unavailable rather than invented evidence',()=>{
 const result=compareBinaryOutcome({observations:[row('a1','A','play')],versionA:'A',versionB:'B'});
 assert.equal(result.B.n,0); assert.equal(result.B.interval,null); assert.equal(result.difference,null);
});
