import { AudienceEventPort } from '../core/ports.js';

export class MemoryAudienceEvents extends AudienceEventPort {
  constructor(seed = []) { super(); this.items = [...seed]; }
  async append(observation) { this.items.push(observation); return observation; }
  async listByExperiment(experimentId) { return this.items.filter(x => x.experimentId === experimentId); }
}
