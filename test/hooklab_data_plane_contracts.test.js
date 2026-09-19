import test from 'node:test';
import assert from 'node:assert/strict';
import { createPlatformObservation, platformObservationKey } from '../src/hooklab/core/platform_observation.js';
import { createReleaseIdentity, sha256 } from '../src/hooklab/core/release_identity.js';

test('canonical platform observation preserves provenance and stable identity fields',()=>{
  const input={releaseId:'C001',trackId:'T001',audioVersionId:'M1',platform:'YouTube',metric:'retention',value:.71,unit:'ratio',observedAt:'2026-09-19T12:00:00Z',periodStart:'2026-09-19',periodEnd:'2026-09-19',territory:'CO',source:'youtube_analytics',collectionMethod:'api'};
  const o=createPlatformObservation(input);
  assert.equal(o.platform,'youtube');
  assert.equal(o.canonicalSchemaVersion,'1.0.0');
  assert.match(platformObservationKey(o),/^C001\|T001\|M1\|youtube\|retention/);
});

test('invalid observations are rejected before curated analytics',()=>{
  assert.throws(()=>createPlatformObservation({releaseId:'C001'}),/requires/);
});

test('release identity distinguishes the exact audio stimulus',()=>{
  const digest=sha256(Buffer.from('master-v1'));
  const identity=createReleaseIdentity({releaseId:'C001',trackId:'T001',audioVersionId:'MASTER-01',audioSha256:digest,externalIds:{spotify:'sp1'}});
  assert.equal(identity.audioSha256,digest);
  assert.equal(identity.externalIds.spotify,'sp1');
});
