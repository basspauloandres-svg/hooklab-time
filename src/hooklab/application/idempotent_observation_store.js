import { ObservationStorePort } from '../ports/observation_store.js';

export class InMemoryIdempotentObservationStore extends ObservationStorePort {
  #rows=new Map();

  async put(item) {
    if(!item?.key || !item?.observation) throw new TypeError('store item requires key and observation');
    if(this.#rows.has(item.key)) return Object.freeze({inserted:false,key:item.key});
    this.#rows.set(item.key,structuredClone(item.observation));
    return Object.freeze({inserted:true,key:item.key});
  }

  async putMany(items) {
    const results=[];
    for (const item of items) results.push(await this.put(item));
    return Object.freeze({
      inserted:results.filter(r=>r.inserted).length,
      duplicates:results.filter(r=>!r.inserted).length,
      results:Object.freeze(results)
    });
  }

  async findByRelease(releaseId) {
    return Object.freeze([...this.#rows.values()].filter(row=>row.releaseId===releaseId).map(structuredClone));
  }

  values(){ return Object.freeze([...this.#rows.values()].map(structuredClone)); }
  get size(){ return this.#rows.size; }
}
