export function kaplanMeier({ observations, durationMs }) {
  const bySession = new Map();
  for (const o of observations) {
    const prior = bySession.get(o.sessionId) || [];
    prior.push(o.event);
    bySession.set(o.sessionId, prior);
  }
  const exits = [];
  for (const [sessionId, events] of bySession) {
    const sorted = [...events].sort((a,b) => a.timestampMs-b.timestampMs);
    const terminal = sorted.find(e => ['skip','stop'].includes(e.type));
    exits.push({ sessionId, timeMs: terminal ? terminal.timestampMs : durationMs, event: Boolean(terminal) });
  }
  const eventTimes = [...new Set(exits.filter(x=>x.event).map(x=>x.timeMs))].sort((a,b)=>a-b);
  let survival = 1;
  const curve = [{ timeMs: 0, survival: 1, atRisk: exits.length, events: 0 }];
  for (const t of eventTimes) {
    const atRisk = exits.filter(x=>x.timeMs >= t).length;
    const d = exits.filter(x=>x.event && x.timeMs === t).length;
    survival *= (1 - d / atRisk);
    curve.push({ timeMs: t, survival, atRisk, events: d });
  }
  return Object.freeze({ n: exits.length, curve: Object.freeze(curve), sessions: Object.freeze(exits) });
}

export function discreteHazard(km) {
  return Object.freeze(km.curve.slice(1).map(p => ({ timeMs: p.timeMs, hazard: p.atRisk ? p.events / p.atRisk : null, atRisk: p.atRisk, events: p.events })));
}
