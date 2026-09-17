import test from 'node:test';
import assert from 'node:assert/strict';
import { experiment } from '../src/hooklab/core/experiment.js';
import { LocalExperimentAdapter } from '../src/hooklab/adapters/local_experiment.js';
import { MemoryAudienceEvents } from '../src/hooklab/adapters/memory_audience_events.js';
import { ListeningLabService } from '../src/hooklab/application/listening_lab_service.js';
import { summarizeOutcomes } from '../src/hooklab/application/outcomes.js';

test('Listening Lab captures immutable versioned audience telemetry', async()=>{
 const exp=experiment({experimentId:'M1',songId:'MANIZALES',variants:['P04','P05']});
 const audience=new MemoryAudienceEvents();
 const lab=new ListeningLabService({audiencePort:audience,experimentPort:new LocalExperimentAdapter([exp])});
 const s=await lab.start({sessionId:'s1',participantId:'anon-1',songId:'MANIZALES',experimentId:'M1'});
 await s.record('exposure',0); await s.record('play',200); await s.record('complete',40000);
 await assert.rejects(()=>s.record('play',41000));
 const rows=await audience.listByExperiment('M1');
 assert.equal(rows.length,3); assert.ok(['P04','P05'].includes(rows[0].versionId));
 assert.equal(summarizeOutcomes(rows).completionRate,1);
});
