export class EvidenceStorePort {
  async put(_record){ throw new Error('EvidenceStorePort.put not implemented'); }
  async findByRelease(_releaseId){ throw new Error('EvidenceStorePort.findByRelease not implemented'); }
  async findByTarget(_targetMetric){ throw new Error('EvidenceStorePort.findByTarget not implemented'); }
}
