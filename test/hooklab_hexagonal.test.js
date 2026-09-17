import test from 'node:test';
import assert from 'node:assert/strict';
import { runVerticalSlice } from '../src/hooklab/application/run_vertical_slice.js';

test('M0 hexagonal vertical slice aligns response, retention and evidence', async () => {
  const out = await runVerticalSlice();
  assert.equal(out.retention.n, 3);
  assert.equal(out.hazard.length, 2);
  assert.ok(out.evidence.length >= 1);
  assert.equal(out.evidence[0].level, 'OBSERVATION');
  assert.ok(out.result.aligned.every(x => Array.isArray(x.coincidentStimulusEvents)));
});
