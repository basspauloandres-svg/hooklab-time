# Dance-Pop T1 discovery queue — checkpoint

Date: 2026-08-31
Branch: `mie/golden-forensic-v0.3`
Layer: `T1_TARGET_DISCOVERY_QUEUE_v1`
State: `IMPLEMENTED / DISCOVERY_CORROBORATED / QUALIFICATION_PENDING`

## Purpose
Populate the discovery side of the existing TSDQP sufficiently to attempt T1=30 without treating symbolic-repository availability as the population.

## Corroboration
Candidate discovery was grounded in external genre/style editorial evidence, principally AllMusic Dance-Pop song/style pages and Dance-Pop compilation contexts. One high-mass-success candidate (`Blinding Lights`) was added from Billboard's 21st-century Hot 100 retrospective but remains explicitly pending independent Dance-Pop style confirmation.

## Artifact
`experiments/gate_b2/DANCE_POP_T1_DISCOVERY_QUEUE_v1.json`

The queue contains 25 new candidates in addition to the 5 already-qualified T0 rows. This creates 30 discovery targets, not 30 qualified rows.

## Scientific boundary
No candidate in this queue is promoted by inclusion. Each must pass the existing TSDQP gates independently:
1. mass-success evidence;
2. identity;
3. genre::style;
4. version;
5. legitimate/auditable symbolic-source resolution;
6. FULL_SONG;
7. provenance;
8. FULL_TMT;
9. Matrix X append;
10. later stability/scientific promotion gates.

Public short previews remain prototype evidence only and cannot satisfy FULL_SONG or robust Matrix-X admission.

## Next layer
Automate qualification-state tracking for these 25 candidates and resolve evidence/source availability in batch. Rejections must remain in provenance and do not get replaced silently merely to reach N=30.
