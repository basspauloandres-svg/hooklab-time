import { createRawIngestionEnvelope } from '../core/raw_ingestion_envelope.js';
import { validateObservationBatch } from './observation_quality_gate.js';

export async function ingestPlatformBatch({source,sourceEntityId,collectedAt,sourceSchemaVersion,payload,observations,rawStore,observationStore}) {
  if (!rawStore || !observationStore) throw new TypeError('ingestion requires rawStore and observationStore');
  const envelope=createRawIngestionEnvelope({source,sourceEntityId,collectedAt,sourceSchemaVersion,payload});
  const rawResult=await rawStore.append(envelope);
  const quality=validateObservationBatch(observations ?? []);
  const curatedResult=await observationStore.putMany(quality.accepted);
  return Object.freeze({
    ingestionId:envelope.ingestionId,
    payloadHash:envelope.payloadHash,
    rawInserted:rawResult.inserted,
    quality,
    curated:curatedResult
  });
}
