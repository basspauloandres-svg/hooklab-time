import { createRawIngestionEnvelope } from '../core/raw_ingestion_envelope.js';
import { createDataLineage } from '../core/data_lineage.js';
import { validateObservationBatch } from './observation_quality_gate.js';

export async function ingestPlatformBatch({source,sourceEntityId,collectedAt,sourceSchemaVersion,payload,observations,rawStore,observationStore,lineageStore}) {
  if (!rawStore || !observationStore) throw new TypeError('ingestion requires rawStore and observationStore');
  const envelope=createRawIngestionEnvelope({source,sourceEntityId,collectedAt,sourceSchemaVersion,payload});
  const rawResult=await rawStore.append(envelope);
  const quality=validateObservationBatch(observations ?? []);
  const curatedResult=await observationStore.putMany(quality.accepted);
  let lineageInserted=0;
  if(lineageStore) {
    for(const item of quality.accepted) {
      const result=await lineageStore.append(createDataLineage({
        ingestionId:envelope.ingestionId,
        payloadHash:envelope.payloadHash,
        canonicalKey:item.key,
        source:envelope.source,
        createdAt:envelope.collectedAt
      }));
      if(result.inserted) lineageInserted++;
    }
  }
  return Object.freeze({
    ingestionId:envelope.ingestionId,
    payloadHash:envelope.payloadHash,
    rawInserted:rawResult.inserted,
    quality,
    curated:curatedResult,
    lineage:Object.freeze({inserted:lineageInserted})
  });
}
