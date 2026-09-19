function sessionsByVersion(observations, versionId) {
  const sessions=new Map();
  for(const o of observations.filter(x=>x.versionId===versionId)){
    if(!sessions.has(o.sessionId)) sessions.set(o.sessionId,[]);
    sessions.get(o.sessionId).push(o.event);
  }
  return sessions;
}

function proportionInterval(successes,n,z=1.959963984540054){
  if(!n) return null;
  const p=successes/n;
  const d=1+z*z/n;
  const center=(p+z*z/(2*n))/d;
  const half=z*Math.sqrt((p*(1-p)+z*z/(4*n))/n)/d;
  return Object.freeze({estimate:p,lower:Math.max(0,center-half),upper:Math.min(1,center+half),method:'Wilson 95% CI'});
}

function riskDifferenceInterval(a,nA,b,nB,z=1.959963984540054){
  if(!nA||!nB) return null;
  const pA=a/nA,pB=b/nB,difference=pA-pB;
  const se=Math.sqrt(pA*(1-pA)/nA+pB*(1-pB)/nB);
  return Object.freeze({estimate:difference,lower:difference-z*se,upper:difference+z*se,standardError:se,method:'Wald 95% CI for risk difference'});
}

export function compareBinaryOutcome({observations,versionA,versionB,outcomeTypes=['complete']}){
  const summarize=versionId=>{
    const sessions=sessionsByVersion(observations,versionId);
    let successes=0;
    for(const events of sessions.values()) if(events.some(e=>outcomeTypes.includes(e.type))) successes++;
    return Object.freeze({versionId,n:sessions.size,successes,interval:proportionInterval(successes,sessions.size)});
  };
  const A=summarize(versionA),B=summarize(versionB);
  const difference=riskDifferenceInterval(A.successes,A.n,B.successes,B.n);
  return Object.freeze({outcomeTypes:Object.freeze([...outcomeTypes]),A,B,difference,inferenceLevel:'STATISTICAL_COMPARISON',causalClaim:false});
}
