import { StimulusAnalysisPort } from '../core/ports.js';

export class StaticStimulusAdapter extends StimulusAnalysisPort {
  constructor(stimulus) { super(); this.stimulus = stimulus; }
  async analyze(input = {}) {
    if (input.songId && input.songId !== this.stimulus.songId) throw new Error('songId mismatch');
    if (input.versionId && input.versionId !== this.stimulus.versionId) throw new Error('versionId mismatch');
    return this.stimulus;
  }
}
