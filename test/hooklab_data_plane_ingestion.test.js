import test from 'node:test';
import assert from 'node:assert/strict';
import { createRawIngestionEnvelope } from '../src/hooklab/core/raw_ingestion_envelope.js';
import { validateObservationBatch } from '../src/hooklab/application/observation_quality_gate.js';
import { InMemoryIdempotentObservationStore } from '../src/hooklab/application/idempotent_observation_store.js';

const observation={releaseId:'C001',trackId:'T001',audioVersionId:'M1',platform:'youtube',metric:'views',value:100,observedAt:'2026-09-19T12:00:00Z',source:'youtube_analytics'};

test('raw envelope produces deterministic payload lineage',()=>{
 const a=createRawIngestionEnvelope({source:'YouTube',collectedAt:'2026-09-19T12:00:00Z',payload:{b:2,a:1}});
 const b=createRawIngestionEnvelope({source:'YouTube',collectedAt:'2026-09-19T12:01:00Z',payload:{a:1,b:2}});
 assert.equal(a.payloadHash,b.payloadHash);
 assert.equal(a.ingestionId,b.ingestionId);
});

test('quality gate rejects duplicate observations inside one batch',()=>{
 const result=validateObservationBatch([observation,{...observation}]);
 assert.equal(result.stats.accepted,1);
 assert.equal(result.rejected[0].reason,'DUPLICATE_IN_BATCH');
});

test('curated store is idempotent across repeated ingestion',()=>{
 const batch=validateObservationBatch([observation]);
 const store=new InMemoryIdempotentObservationStore();
 const first=store.putMany(batch.accepted);
 const second=store.putMany(batch.accepted);
 assert.equal(first.inserted,1);
 assert.equal(second.duplicates,1);
 assert.equal(store.size,1);
});
