import { RawStorePort } from '../ports/raw_store.js';

export class MemoryRawStore extends RawStorePort {
  #rows = new Map();

  async append(envelope) {
    if (!envelope?.ingestionId || !envelope?.payloadHash) throw new TypeError('raw envelope requires ingestionId and payloadHash');
    const existing = this.#rows.get(envelope.ingestionId);
    if (existing) {
      if (existing.payloadHash !== envelope.payloadHash) throw new Error('IMMUTABILITY_VIOLATION');
      return Object.freeze({ inserted:false, ingestionId:envelope.ingestionId });
    }
    this.#rows.set(envelope.ingestionId, structuredClone(envelope));
    return Object.freeze({ inserted:true, ingestionId:envelope.ingestionId });
  }

  async getByIngestionId(ingestionId) {
    const row=this.#rows.get(ingestionId);
    return row ? structuredClone(row) : null;
  }

  get size(){ return this.#rows.size; }
}
