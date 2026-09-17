import { kaplanMeier, discreteHazard } from './retention.js';

export function compareVariants({ observations, variants, durationMsByVersion }) {
  const result={};
  for (const versionId of variants) {
    const rows=observations.filter(x=>x.versionId===versionId);
    const km=kaplanMeier({observations:rows,durationMs:durationMsByVersion[versionId]});
    const completed=new Set(rows.filter(x=>x.event.type==='complete').map(x=>x.sessionId)).size;
    const sessions=new Set(rows.map(x=>x.sessionId)).size;
    result[versionId]=Object.freeze({sessions,completionRate:sessions?completed/sessions:null,retention:km,hazard:discreteHazard(km)});
  }
  return Object.freeze(result);
}
