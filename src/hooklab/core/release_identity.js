import { createHash } from 'node:crypto';

export function sha256(content) {
  return createHash('sha256').update(content).digest('hex');
}

export function createReleaseIdentity(input) {
  if (!input?.releaseId || !input?.trackId || !input?.audioVersionId) {
    throw new TypeError('release identity requires releaseId, trackId and audioVersionId');
  }
  return Object.freeze({
    releaseId:String(input.releaseId),
    trackId:String(input.trackId),
    audioVersionId:String(input.audioVersionId),
    isrc:input.isrc??null,
    audioSha256:input.audioSha256??null,
    externalIds:Object.freeze({...input.externalIds}),
    releasedAt:input.releasedAt??null,
    schemaVersion:'1.0.0'
  });
}
