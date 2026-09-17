import { AudienceEventType, validateAudienceEvent } from './event_schema.js';
import { audienceObservation, temporalEvent } from './contracts.js';

export function listeningSession({ sessionId, participantId, songId, versionId, experimentId, source='ListeningLab' }) {
  if(!sessionId||!participantId||!songId||!versionId||!experimentId) throw new TypeError('invalid listening session');
  let terminal=false;
  const observations=[];
  function record(type,timestampMs,payload={}) {
    if(terminal) throw new Error('session already terminal');
    const event=temporalEvent({timestampMs,type,source,payload});
    validateAudienceEvent(event);
    const obs=audienceObservation({sessionId,songId,versionId,experimentId,event});
    observations.push(obs);
    if([AudienceEventType.SKIP,AudienceEventType.STOP,AudienceEventType.COMPLETE].includes(type)) terminal=true;
    return obs;
  }
  return Object.freeze({sessionId,participantId,songId,versionId,experimentId,record,list:()=>Object.freeze([...observations]),isTerminal:()=>terminal});
}
