import { EvidenceStorePort } from '../ports/evidence_store.js';
import { createEvidenceRecord } from '../core/evidence_record.js';

export class MemoryEvidenceStore extends EvidenceStorePort {
  #rows=new Map();
  async put(input){
    const record=createEvidenceRecord(input);
    const existing=this.#rows.get(record.evidenceId);
    if(existing){
      if(JSON.stringify(existing)!==JSON.stringify(record)) throw new Error('EVIDENCE_IMMUTABILITY_VIOLATION');
      return Object.freeze({inserted:false,evidenceId:record.evidenceId});
    }
    this.#rows.set(record.evidenceId,record);
    return Object.freeze({inserted:true,evidenceId:record.evidenceId});
  }
  async findByRelease(releaseId){return Object.freeze([...this.#rows.values()].filter(r=>r.releaseId===releaseId));}
  async findByTarget(targetMetric){return Object.freeze([...this.#rows.values()].filter(r=>r.targetMetric===targetMetric));}
  get size(){return this.#rows.size;}
}
