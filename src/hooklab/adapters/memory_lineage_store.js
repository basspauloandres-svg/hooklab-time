import { LineageStorePort } from '../ports/lineage_store.js';

export class MemoryLineageStore extends LineageStorePort {
  #rows=[];
  #keys=new Set();

  async append(lineage) {
    const identity=[lineage.ingestionId,lineage.canonicalKey,lineage.transformerVersion].join('|');
    if(this.#keys.has(identity)) return Object.freeze({inserted:false,identity});
    this.#keys.add(identity);
    this.#rows.push(structuredClone(lineage));
    return Object.freeze({inserted:true,identity});
  }

  async findByCanonicalKey(canonicalKey) {
    return Object.freeze(this.#rows.filter(row=>row.canonicalKey===canonicalKey).map(structuredClone));
  }

  get size(){ return this.#rows.length; }
}
