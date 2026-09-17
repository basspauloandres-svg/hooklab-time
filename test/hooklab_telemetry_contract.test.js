import test from 'node:test'; import assert from 'node:assert/strict';
import { temporalEvent,audienceObservation } from '../src/hooklab/core/contracts.js';
import { telemetryEnvelope } from '../src/hooklab/core/telemetry_envelope.js';
import { assertDataMinimization } from '../src/hooklab/core/privacy.js';

test('telemetry envelope preserves analytical IDs without direct identifiers',()=>{const event=temporalEvent({timestampMs:1000,type:'play',source:'ListeningLab'});const o=audienceObservation({sessionId:'s',songId:'song',versionId:'v1',experimentId:'e1',event});const env=telemetryEnvelope({observation:o,participantKey:'anon-123',context:{deviceClass:'mobile'}});assert.equal(env.versionId,'v1');assert.equal(assertDataMinimization(env),true);assert.throws(()=>assertDataMinimization({...env,email:'x@example.com'}));});
