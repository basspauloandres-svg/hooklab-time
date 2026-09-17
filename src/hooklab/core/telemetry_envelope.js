export const TELEMETRY_SCHEMA_VERSION='hooklab.audience-event.v1';
export function telemetryEnvelope({observation,participantKey,clientTimeMs=null,context={}}){
 if(!observation||!participantKey) throw new TypeError('observation and anonymous participantKey required');
 return Object.freeze({schemaVersion:TELEMETRY_SCHEMA_VERSION,participantKey,sessionId:observation.sessionId,songId:observation.songId,versionId:observation.versionId,experimentId:observation.experimentId,event:observation.event,clientTimeMs,context:Object.freeze({...context})});
}
