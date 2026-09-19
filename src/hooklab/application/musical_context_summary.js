function requireFiniteNonNegative(value,name){
  if(!Number.isFinite(value)||value<0) throw new TypeError(`${name} must be finite and non-negative`);
}

function eventTime(event){
  if(Number.isFinite(event?.timestampMs)) return event.timestampMs;
  if(Number.isFinite(event?.timeMs)) return event.timeMs;
  return null;
}

function eventLabel(event){
  return event?.type ?? event?.label ?? event?.kind ?? 'unknown';
}

function extractEvents(aligned){
  const events=[];
  for(const item of aligned??[]){
    if(Array.isArray(item?.coincidentStimulusEvents)) events.push(...item.coincidentStimulusEvents);
    else events.push(item?.stimulusEvent??item?.stimulus??item);
  }
  return events.filter(Boolean);
}

export function summarizeMusicalContext({aligned, behavioralTimestampMs, lookbackMs=5000, lookaheadMs=2000}){
  requireFiniteNonNegative(behavioralTimestampMs,'behavioralTimestampMs');
  requireFiniteNonNegative(lookbackMs,'lookbackMs');
  requireFiniteNonNegative(lookaheadMs,'lookaheadMs');
  const candidates=extractEvents(aligned)
    .map(event=>({event,timestampMs:eventTime(event)}))
    .filter(x=>x.timestampMs!=null&&x.timestampMs>=Math.max(0,behavioralTimestampMs-lookbackMs)&&x.timestampMs<=behavioralTimestampMs+lookaheadMs)
    .sort((a,b)=>a.timestampMs-b.timestampMs);
  const byType={};
  for(const {event} of candidates){ const key=eventLabel(event); byType[key]=(byType[key]??0)+1; }
  const nearest=candidates.length?[...candidates].sort((a,b)=>Math.abs(a.timestampMs-behavioralTimestampMs)-Math.abs(b.timestampMs-behavioralTimestampMs))[0]:null;
  return Object.freeze({
    behavioralTimestampMs,
    window:Object.freeze({startMs:Math.max(0,behavioralTimestampMs-lookbackMs),endMs:behavioralTimestampMs+lookaheadMs}),
    eventCount:candidates.length,
    byType:Object.freeze(byType),
    nearest:nearest?Object.freeze({timestampMs:nearest.timestampMs,offsetMs:nearest.timestampMs-behavioralTimestampMs,type:eventLabel(nearest.event),event:nearest.event}):null,
    events:Object.freeze(candidates.map(x=>x.event)),
    inferenceLevel:'DESCRIPTIVE_TEMPORAL_CONTEXT'
  });
}
