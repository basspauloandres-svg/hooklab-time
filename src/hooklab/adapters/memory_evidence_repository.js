import { EvidenceRepositoryPort } from '../core/ports.js';

export class MemoryEvidenceRepository extends EvidenceRepositoryPort {
  constructor() {
    super();
    this.records = new Map();
  }

  async save(record) {
    this.records.set(record.evidenceId, record);
    return record;
  }

  async find(query = {}) {
    return [...this.records.values()].filter(record =>
      Object.entries(query).every(([key, value]) => record[key] === value)
    );
  }
}
