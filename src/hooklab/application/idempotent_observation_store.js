export class InMemoryIdempotentObservationStore {
  #rows=new Map();

  put(item) {
    if(!item?.key || !item?.observation) throw new TypeError('store item requires key and observation');
    if(this.#rows.has(item.key)) return Object.freeze({inserted:false,key:item.key});
    this.#rows.set(item.key,item.observation);
    return Object.freeze({inserted:true,key:item.key});
  }

  putMany(items) {
    const results=items.map(item=>this.put(item));
    return Object.freeze({
      inserted:results.filter(r=>r.inserted).length,
      duplicates:results.filter(r=>!r.inserted).length,
      results:Object.freeze(results)
    });
  }

  values(){ return Object.freeze([...this.#rows.values()]); }
  get size(){ return this.#rows.size; }
}
