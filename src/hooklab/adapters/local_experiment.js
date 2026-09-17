import { ExperimentPort } from '../core/ports.js';
import { deterministicAssignment } from '../core/experiment.js';
export class LocalExperimentAdapter extends ExperimentPort {
  constructor(experiments=[]) { super(); this.experiments=new Map(experiments.map(x=>[x.experimentId,x])); }
  async assign(experimentId, participantId) { const exp=this.experiments.get(experimentId); if(!exp) throw new Error('experiment not found'); return deterministicAssignment(exp,participantId); }
}
