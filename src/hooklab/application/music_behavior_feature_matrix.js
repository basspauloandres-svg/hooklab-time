function finite(value){ return Number.isFinite(value)?value:null; }

function oneHot(types){
  const out={};
  for(const type of types) out[`music_${type}`]=0;
  return out;
}

export function buildMusicBehaviorFeatureMatrix({chains}){
  const musicTypes=[...new Set(chains.flatMap(chain=>Object.keys(chain?.musicalContext?.byType??{})))].sort();
  const rows=[];
  for(const chain of chains){
    if(!chain?.peak||!chain?.musicalContext) continue;
    const row={
      songId:chain.songId??null,
      versionId:chain.versionId??null,
      peakStartMs:chain.peak.startMs,
      peakEndMs:chain.peak.endMs,
      atRisk:chain.peak.atRisk,
      behavioralEvents:chain.peak.events,
      hazard:finite(chain.peak.hazard),
      nearestMusicType:chain.musicalContext.nearest?.type??null,
      nearestMusicOffsetMs:finite(chain.musicalContext.nearest?.offsetMs),
      musicEventCount:chain.musicalContext.eventCount,
      ...oneHot(musicTypes)
    };
    for(const [type,count] of Object.entries(chain.musicalContext.byType)) row[`music_${type}`]=count;
    rows.push(Object.freeze(row));
  }
  return Object.freeze({
    columns:Object.freeze(rows.length?Object.keys(rows[0]):[]),
    musicTypes:Object.freeze(musicTypes),
    rows:Object.freeze(rows),
    inferenceLevel:'ANALYTIC_FEATURE_MATRIX',
    causalClaim:false
  });
}
