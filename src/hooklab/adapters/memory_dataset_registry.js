import { DatasetRegistryPort } from '../ports/dataset_registry.js';
import { createDatasetManifest,datasetManifestKey } from '../core/dataset_manifest.js';

export class MemoryDatasetRegistry extends DatasetRegistryPort{
  #rows=new Map();
  async register(input){
    const manifest=createDatasetManifest(input); const key=datasetManifestKey(manifest);
    const existing=this.#rows.get(key);
    if(existing){
      if(JSON.stringify(existing)!==JSON.stringify(manifest)) throw new Error('DATASET_VERSION_IMMUTABILITY_VIOLATION');
      return Object.freeze({inserted:false,key});
    }
    this.#rows.set(key,manifest); return Object.freeze({inserted:true,key});
  }
  async get(datasetId,version){return this.#rows.get(`${datasetId}@${version}`)??null;}
  async listVersions(datasetId){
    return Object.freeze([...this.#rows.values()].filter(x=>x.datasetId===datasetId).sort((a,b)=>a.createdAt.localeCompare(b.createdAt)));
  }
}
