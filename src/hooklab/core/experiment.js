export function experiment({ experimentId, songId, variants, allocation='deterministic-balanced', hypothesis=null }) {
  if (!experimentId || !songId || !Array.isArray(variants) || variants.length < 2) throw new TypeError('experiment requires id, song and at least two variants');
  return Object.freeze({ experimentId, songId, variants:Object.freeze([...variants]), allocation, hypothesis });
}

export function deterministicAssignment(exp, participantId) {
  let h=2166136261;
  for (const ch of String(participantId)) { h ^= ch.charCodeAt(0); h = Math.imul(h,16777619); }
  return exp.variants[(h>>>0) % exp.variants.length];
}
