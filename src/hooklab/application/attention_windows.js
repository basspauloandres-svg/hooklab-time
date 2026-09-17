export function detectHazardWindows(hazard,{minimumAtRisk=2,minimumHazard=0.1}={}){
 return Object.freeze(hazard.filter(x=>x.atRisk>=minimumAtRisk&&x.hazard>=minimumHazard).map(x=>Object.freeze({timeMs:x.timeMs,hazard:x.hazard,atRisk:x.atRisk,classification:'observed-abandonment-window'})));
}
