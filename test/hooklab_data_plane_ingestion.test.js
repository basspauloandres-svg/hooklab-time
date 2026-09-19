import test from 'node:test';
import assert from 'node:assert/strict';
import { createRawIngestionEnvelope } from '../src/hooklab/core/raw_ingestion_envelope.js';
import { validateObservationBatch } from '../src/hooklab/application/observation_quality_gate.js';
import { InMemoryIdempotentObservationStore } from '../src/hooklab/application/idempotent_observation_store.js';
import { MemoryRawStore } from '../src/hooklab/adapters/memory_raw_store.js';
import { ingestPlatformBatch } from '../src/hooklab/application/ingest_platform_batch.js';

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

test('curated store is idempotent across repeated ingestion',async()=>{
 const batch=validateObservationBatch([observation]);
 const store=new InMemoryIdempotentObservationStore();
 const first=await store.putMany(batch.accepted);
 const second=await store.putMany(batch.accepted);
 assert.equal(first.inserted,1);
 assert.equal(second.duplicates,1);
 assert.equal(store.size,1);
});

test('raw-to-curated ingestion preserves raw payload and avoids duplicate curated rows',async()=>{
 const rawStore=new MemoryRawStore();
 const observationStore=new InMemoryIdempotentObservationStore();
 const args={source:'youtube',sourceEntityId:'video-1',collectedAt:'2026-09-19T12:00:00Z',payload:{views:100},observations:[observation],rawStore,observationStore};
 const first=await ingestPlatformBatch(args);
 const second=await ingestPlatformBatch({...args,collectedAt:'2026-09-19T12:05:00Z'});
 assert.equal(first.rawInserted,true);
 assert.equal(second.rawInserted,false);
 assert.equal(first.curated.inserted,1);
 assert.equal(second.curated.duplicates,1);
 assert.equal(rawStore.size,1);
 assert.equal(observationStore.size,1);
 assert.equal((await observationStore.findByRelease('C001')).length,1);
});
