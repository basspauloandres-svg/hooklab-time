import test from 'node:test';
import assert from 'node:assert/strict';
import { MemoryDatasetRegistry } from '../src/hooklab/adapters/memory_dataset_registry.js';

const d={datasetId:'hooklab-market',version:'D0.1',kind:'curated',releases:['C002','C001'],sources:['youtube','spotify'],observationCount:200,featureCount:900,cutoffAt:'2026-09-19T00:00:00Z',createdAt:'2026-09-19T12:00:00Z'};

test('dataset versions are immutable and reproducible',async()=>{
 const r=new MemoryDatasetRegistry();
 assert.equal((await r.register(d)).inserted,true);
 assert.equal((await r.register(d)).inserted,false);
 await assert.rejects(()=>r.register({...d,observationCount:201}),/IMMUTABILITY/);
 const saved=await r.get('hooklab-market','D0.1');
 assert.deepEqual(saved.releases,['C001','C002']);
});

test('registry keeps temporal dataset history',async()=>{
 const r=new MemoryDatasetRegistry();
 await r.register(d);
 await r.register({...d,version:'D0.2',parentVersion:'D0.1',observationCount:300,createdAt:'2026-09-20T12:00:00Z'});
 const versions=await r.listVersions('hooklab-market');
 assert.deepEqual(versions.map(x=>x.version),['D0.1','D0.2']);
});
