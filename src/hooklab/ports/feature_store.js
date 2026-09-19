export class FeatureStorePort {
  async putMany(_items){ throw new Error('FeatureStorePort.putMany not implemented'); }
  async findByAudioVersion(_trackId,_audioVersionId){ throw new Error('FeatureStorePort.findByAudioVersion not implemented'); }
  async findWindow(_trackId,_audioVersionId,_start,_end){ throw new Error('FeatureStorePort.findWindow not implemented'); }
}
