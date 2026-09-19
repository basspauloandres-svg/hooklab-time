export class DatasetRegistryPort {
  async register(_manifest){throw new Error('DatasetRegistryPort.register not implemented');}
  async get(_datasetId,_version){throw new Error('DatasetRegistryPort.get not implemented');}
  async listVersions(_datasetId){throw new Error('DatasetRegistryPort.listVersions not implemented');}
}
