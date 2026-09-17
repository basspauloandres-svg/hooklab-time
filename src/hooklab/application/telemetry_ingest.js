import { assertDataMinimization } from '../core/privacy.js';
export class TelemetryIngestService {
 constructor({audiencePort}){this.audiencePort=audiencePort;}
 async ingest(envelope){ assertDataMinimization(envelope); if(!envelope.schemaVersion||!envelope.event) throw new TypeError('invalid telemetry envelope'); return this.audiencePort.append(Object.freeze({sessionId:envelope.sessionId,songId:envelope.songId,versionId:envelope.versionId,experimentId:envelope.experimentId,event:envelope.event})); }
}
