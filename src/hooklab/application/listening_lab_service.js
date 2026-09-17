import { listeningSession } from '../core/listening_session.js';

export class ListeningLabService {
  constructor({ audiencePort, experimentPort }) { this.audiencePort=audiencePort; this.experimentPort=experimentPort; }
  async start({sessionId,participantId,songId,experimentId}) {
    const versionId=await this.experimentPort.assign(experimentId,participantId);
    const session=listeningSession({sessionId,participantId,songId,versionId,experimentId});
    return Object.freeze({versionId, record:async(type,timestampMs,payload={})=>{
      const observation=session.record(type,timestampMs,payload);
      await this.audiencePort.append(observation);
      return observation;
    }, list:session.list, isTerminal:session.isTerminal});
  }
}
