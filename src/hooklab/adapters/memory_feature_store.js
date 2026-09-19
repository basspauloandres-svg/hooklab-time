import { FeatureStorePort } from '../ports/feature_store.js';
import { createFeatureRecord, featureRecordKey } from '../core/feature_record.js';

export class MemoryFeatureStore extends FeatureStorePort {
  #rows=new Map();
  async putMany(inputs){
    let inserted=0,duplicates=0;
    for(const input of inputs){
      const record=createFeatureRecord(input); const key=featureRecordKey(record);
      if(this.#rows.has(key)){ duplicates++; continue; }
      this.#rows.set(key,record); inserted++;
    }
    return Object.freeze({inserted,duplicates});
  }
  async findByAudioVersion(trackId,audioVersionId){
    return Object.freeze([...this.#rows.values()].filter(r=>r.trackId===trackId&&r.audioVersionId===audioVersionId));
  }
  async findWindow(trackId,audioVersionId,start,end){
    return Object.freeze([...this.#rows.values()].filter(r=>r.trackId===trackId&&r.audioVersionId===audioVersionId&&r.timeEnd>=start&&r.timeStart<=end));
  }
  get size(){return this.#rows.size;}
}
