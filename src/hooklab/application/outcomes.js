export function summarizeOutcomes(observations) {
  const sessions=new Map();
  for(const o of observations){ if(!sessions.has(o.sessionId)) sessions.set(o.sessionId,[]); sessions.get(o.sessionId).push(o.event); }
  let completed=0,skipped=0,replayed=0,saveIntent=0,shareIntent=0;
  for(const events of sessions.values()){
    const types=new Set(events.map(e=>e.type));
    if(types.has('complete')) completed++;
    if(types.has('skip')||types.has('stop')) skipped++;
    if(types.has('song_replay')||types.has('segment_replay')) replayed++;
    if(types.has('save_intent')) saveIntent++;
    if(types.has('share_intent')) shareIntent++;
  }
  const n=sessions.size; const rate=x=>n?x/n:null;
  return Object.freeze({sessions:n,completionRate:rate(completed),abandonmentRate:rate(skipped),replayRate:rate(replayed),saveIntentRate:rate(saveIntent),shareIntentRate:rate(shareIntent)});
}
