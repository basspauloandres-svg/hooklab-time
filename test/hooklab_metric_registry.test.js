import test from 'node:test';
import assert from 'node:assert/strict';
import { MetricRegistry } from '../src/hooklab/core/metric_registry.js';
import { curateObservations } from '../src/hooklab/application/curate_observations.js';

function registry(){
 const r=new MetricRegistry();
 r.register({metricId:'views',platform:'youtube',name:'Views',unit:'count',grain:'release',aggregation:'count',cumulative:true,temporalResolution:'snapshot'});
 r.register({metricId:'retention',platform:'youtube',name:'Audience retention',unit:'ratio',grain:'content_time',aggregation:'ratio',cumulative:false,temporalResolution:'second'});
 return r;
}

const base={releaseId:'C001',trackId:'T001',audioVersionId:'M1',platform:'youtube',observedAt:'2026-09-19T12:00:00Z',source:'youtube_analytics'};

test('registry preserves incompatible analytical grains as distinct definitions',()=>{
 const r=registry();
 assert.equal(r.get('youtube','views').grain,'release');
 assert.equal(r.get('youtube','retention').grain,'content_time');
});

test('curation rejects unknown metrics and unit mismatches',()=>{
 const result=curateObservations([
  {...base,metric:'views',value:100,unit:'count'},
  {...base,metric:'retention',value:.71,unit:'count'},
  {...base,metric:'mystery',value:1,unit:'count'}
 ],registry());
 assert.equal(result.stats.accepted,1);
 assert.equal(result.stats.rejected,2);
 assert.deepEqual(new Set(result.rejected.map(x=>x.reason)),new Set(['METRIC_UNIT_MISMATCH','UNKNOWN_METRIC']));
});
