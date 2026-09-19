import test from 'node:test';
import assert from 'node:assert/strict';
import { MemoryEvidenceStore } from '../src/hooklab/adapters/memory_evidence_store.js';

const evidence={evidenceId:'E-C001-001',releaseId:'C001',trackId:'T001',targetMetric:'youtube:retention',level:'association',method:'window-association',estimate:.31,intervalLow:.12,intervalHigh:.48,sampleSize:1000,datasetVersion:'D1',featureSetVersion:'tmie-v1',conditions:{territory:'CO'},sourceRefs:['obs:1','feature:1'],createdAt:'2026-09-19T12:00:00Z'};

test('evidence store is immutable and queryable',async()=>{
 const store=new MemoryEvidenceStore();
 assert.equal((await store.put(evidence)).inserted,true);
 assert.equal((await store.put(evidence)).inserted,false);
 await assert.rejects(()=>store.put({...evidence,estimate:.99}),/IMMUTABILITY/);
 assert.equal((await store.findByRelease('C001')).length,1);
 assert.equal((await store.findByTarget('youtube:retention')).length,1);
});
