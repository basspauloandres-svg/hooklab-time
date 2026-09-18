export function synchronizeHazardWithMusic({ hazard, stimulusEvents, lookbackMs=5000, lookaheadMs=2000 }) {
  const music=[...stimulusEvents].sort((a,b)=>a.timestampMs-b.timestampMs);
  return Object.freeze(hazard.map(point=>{
    const start=Math.max(0,point.timeMs-lookbackMs);
    const end=point.timeMs+lookaheadMs;
    return Object.freeze({...point,windowStartMs:start,windowEndMs:end,musicalEvents:Object.freeze(music.filter(e=>e.timestampMs>=start&&e.timestampMs<=end)),inferenceLevel:'TEMPORAL_ASSOCIATION'});
  }));
}

export function peakHazardContext(rows) {
  const valid=rows.filter(x=>Number.isFinite(x.hazard));
  if(!valid.length) return null;
  return [...valid].sort((a,b)=>b.hazard-a.hazard||a.timeMs-b.timeMs)[0];
}
