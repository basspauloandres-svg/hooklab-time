export function alignStimulusResponse({ stimulusEvents, audienceEvents, lookbackMs = 5000, lookaheadMs = 2000 }) {
  if (lookbackMs < 0 || lookaheadMs < 0) throw new RangeError('alignment windows must be non-negative');
  const music = [...stimulusEvents].sort((a, b) => a.timestampMs - b.timestampMs);
  return [...audienceEvents]
    .sort((a, b) => a.event.timestampMs - b.event.timestampMs)
    .map(observation => {
      const t = observation.event.timestampMs;
      const windowStartMs = Math.max(0, t - lookbackMs);
      const windowEndMs = t + lookaheadMs;
      return Object.freeze({
        observation,
        windowStartMs,
        windowEndMs,
        coincidentStimulusEvents: Object.freeze(music.filter(e => e.timestampMs >= windowStartMs && e.timestampMs <= windowEndMs))
      });
    });
}
