export class LineageStorePort {
  async append(_lineage) { throw new Error('LineageStorePort.append not implemented'); }
  async findByCanonicalKey(_canonicalKey) { throw new Error('LineageStorePort.findByCanonicalKey not implemented'); }
}
