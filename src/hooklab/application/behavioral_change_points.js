export function behavioralChangePoints({ observations, eventTypes=['skip','stop'], binMs=1000, minAtRisk=1 }) {
  if(!Number.isFinite(binMs)||binMs<=0) throw new TypeError('binMs must be positive');
  const terminal=new Map();
  let maxT=0;
  for(const o of observations){
    maxT=Math.max(maxT,o.event.timestampMs);
    if(eventTypes.includes(o.event.type)) {
      const prev=terminal.get(o.sessionId);
      if(prev==null||o.event.timestampMs<prev) terminal.set(o.sessionId,o.event.timestampMs);
    }
  }
  const sessionIds=[...new Set(observations.map(o=>o.sessionId))];
  const bins=[];
  for(let start=0;start<=maxT;start+=binMs){
    const end=start+binMs;
    const atRisk=sessionIds.filter(id=>terminal.get(id)==null||terminal.get(id)>=start).length;
    const events=[...terminal.values()].filter(t=>t>=start&&t<end).length;
    if(atRisk>=minAtRisk) bins.push(Object.freeze({startMs:start,endMs:end,atRisk,events,hazard:events/atRisk}));
  }
  const positive=bins.filter(x=>x.events>0);
  const peak=positive.length?[...positive].sort((a,b)=>b.hazard-a.hazard||a.startMs-b.startMs)[0]:null;
  return Object.freeze({bins:Object.freeze(bins),peak});
}
