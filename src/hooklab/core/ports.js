export class StimulusAnalysisPort {
  async analyze(_input) { throw new Error('StimulusAnalysisPort.analyze not implemented'); }
}

export class AudienceEventPort {
  async append(_observation) { throw new Error('AudienceEventPort.append not implemented'); }
  async listByExperiment(_experimentId) { throw new Error('AudienceEventPort.listByExperiment not implemented'); }
}

export class EvidenceRepositoryPort {
  async save(_record) { throw new Error('EvidenceRepositoryPort.save not implemented'); }
  async find(_query) { throw new Error('EvidenceRepositoryPort.find not implemented'); }
}

export class ExperimentPort {
  async assign(_experimentId, _participantId) { throw new Error('ExperimentPort.assign not implemented'); }
}

export class PlatformAnalyticsPort {
  async observations(_releaseId) { throw new Error('PlatformAnalyticsPort.observations not implemented'); }
}

export class CognitiveDescriptorPort {
  async describe(_stimulus) { throw new Error('CognitiveDescriptorPort.describe not implemented'); }
}

export class CompositionPort {
  async propose(_constraints) { throw new Error('CompositionPort.propose not implemented'); }
}
