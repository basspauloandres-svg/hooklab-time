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
  const A=proportionInterval(a,nA,z),B=proportionInterval(b,nB,z);
  const pA=a/nA,pB=b/nB,difference=pA-pB;
  const lower=difference-Math.sqrt((pA-A.lower)**2+(B.upper-pB)**2);
  const upper=difference+Math.sqrt((A.upper-pA)**2+(pB-B.lower)**2);
  return Object.freeze({estimate:difference,lower:Math.max(-1,lower),upper:Math.min(1,upper),method:'Newcombe-Wilson 95% CI for independent risk difference'});
}

function precisionStatus(A,B,difference,minPerVariant){
  if(!difference) return 'UNAVAILABLE';
  if(A.n<minPerVariant||B.n<minPerVariant) return 'EXPLORATORY_SMALL_SAMPLE';
  if(difference.lower<=0&&difference.upper>=0) return 'UNCERTAIN_COMPATIBLE_WITH_NO_DIFFERENCE';
  return 'ESTIMATED_DIFFERENCE_WITH_95CI_EXCLUDING_ZERO';
}

export function compareBinaryOutcome({observations,versionA,versionB,outcomeTypes=['complete'],minPerVariant=20}){
  if(!Number.isInteger(minPerVariant)||minPerVariant<1) throw new TypeError('minPerVariant must be a positive integer');
  const summarize=versionId=>{
    const sessions=sessionsByVersion(observations,versionId);
    let successes=0;
    for(const events of sessions.values()) if(events.some(e=>outcomeTypes.includes(e.type))) successes++;
    return Object.freeze({versionId,n:sessions.size,successes,interval:proportionInterval(successes,sessions.size)});
  };
  const A=summarize(versionA),B=summarize(versionB);
  const difference=riskDifferenceInterval(A.successes,A.n,B.successes,B.n);
  return Object.freeze({outcomeTypes:Object.freeze([...outcomeTypes]),A,B,difference,precisionStatus:precisionStatus(A,B,difference,minPerVariant),minimumPerVariant:minPerVariant,inferenceLevel:'STATISTICAL_COMPARISON',causalClaim:false});
}
