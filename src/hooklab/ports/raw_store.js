export class RawStorePort {
  async append(_envelope) { throw new Error('RawStorePort.append not implemented'); }
  async getByIngestionId(_ingestionId) { throw new Error('RawStorePort.getByIngestionId not implemented'); }
}
