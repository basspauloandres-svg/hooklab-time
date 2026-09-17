export const AudienceEventType = Object.freeze({ EXPOSURE:'exposure', PLAY:'play', PAUSE:'pause', RESUME:'resume', SEEK_FORWARD:'seek_forward', SEEK_BACKWARD:'seek_backward', SKIP:'skip', STOP:'stop', COMPLETE:'complete', SEGMENT_REPLAY:'segment_replay', SONG_REPLAY:'song_replay', CONTINUE:'continue', SAVE_INTENT:'save_intent', SHARE_INTENT:'share_intent' });

export function validateAudienceEvent(event) {
  if (!event || !Object.values(AudienceEventType).includes(event.type)) throw new TypeError('unsupported audience event type');
  if (!Number.isFinite(event.timestampMs) || event.timestampMs < 0) throw new TypeError('invalid audience event timestamp');
  return true;
}
