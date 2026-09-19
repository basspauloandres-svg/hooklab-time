export class ObservationStorePort {
  async put(_item) { throw new Error('ObservationStorePort.put not implemented'); }
  async putMany(_items) { throw new Error('ObservationStorePort.putMany not implemented'); }
  async findByRelease(_releaseId) { throw new Error('ObservationStorePort.findByRelease not implemented'); }
}
