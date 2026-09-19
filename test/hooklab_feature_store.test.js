import test from 'node:test';
import assert from 'node:assert/strict';
import { MemoryFeatureStore } from '../src/hooklab/adapters/memory_feature_store.js';

const base={trackId:'T001',audioVersionId:'MASTER-01',featureSetId:'tmie-v1',extractor:'time-mie',extractorVersion:'1.0.0'};

test('feature store separates exact audio versions and supports temporal windows',async()=>{
 const store=new MemoryFeatureStore();
 await store.putMany([
  {...base,timeStart:18,timeEnd:19,featureName:'onset_density',value:.74},
  {...base,timeStart:20,timeEnd:21,featureName:'vocal_activity',value:1},
  {...base,audioVersionId:'MASTER-02',timeStart:18,timeEnd:19,featureName:'onset_density',value:.81}
 ]);
 assert.equal((await store.findByAudioVersion('T001','MASTER-01')).length,2);
 assert.equal((await store.findWindow('T001','MASTER-01',17.5,19.5)).length,1);
});

test('feature ingestion is idempotent by extractor version and temporal identity',async()=>{
 const store=new MemoryFeatureStore();
 const feature={...base,timeStart:18,timeEnd:19,featureName:'onset_density',value:.74};
 const first=await store.putMany([feature]);
 const second=await store.putMany([feature]);
 assert.equal(first.inserted,1);
 assert.equal(second.duplicates,1);
 assert.equal(store.size,1);
});
