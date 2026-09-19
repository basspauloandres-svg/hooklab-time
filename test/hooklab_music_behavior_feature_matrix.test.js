import test from 'node:test';
import assert from 'node:assert/strict';
import { buildMusicBehaviorFeatureMatrix } from '../src/hooklab/application/music_behavior_feature_matrix.js';

const chain=(versionId,type,count,hazard,offset)=>({
 songId:'S',versionId,
 peak:{startMs:9000,endMs:10000,atRisk:20,events:Math.round(hazard*20),hazard},
 musicalContext:{eventCount:count,byType:{[type]:count},nearest:{type,offsetMs:offset}}
});

test('creates comparable rows with a stable music-event vocabulary',()=>{
 const result=buildMusicBehaviorFeatureMatrix({chains:[chain('A','hook_onset',2,.3,-200),chain('B','harmonic_change',1,.1,100)]});
 assert.deepEqual(result.musicTypes,['harmonic_change','hook_onset']);
 assert.equal(result.rows.length,2);
 assert.equal(result.rows[0].music_hook_onset,2);
 assert.equal(result.rows[0].music_harmonic_change,0);
 assert.equal(result.rows[1].music_harmonic_change,1);
 assert.equal(result.rows[1].music_hook_onset,0);
 assert.equal(result.causalClaim,false);
});

test('chains without a behavioral peak do not become analytic rows',()=>{
 const result=buildMusicBehaviorFeatureMatrix({chains:[{songId:'S',versionId:'A',peak:null,musicalContext:null}]});
 assert.equal(result.rows.length,0);
 assert.deepEqual(result.columns,[]);
});
