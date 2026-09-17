# HookLab Local — Hexagonal Contract

## Scientific order
Audience datum -> behavioral pattern -> temporal localization -> statistical result -> coincident musical event -> explanatory hypothesis -> validation.

## Dependency rule
The domain never imports platform, database, UI, audio-provider, TIME-MIE implementation, or cognitive-model implementation details. External systems implement ports.

## Core scientific objects
MusicalStimulus, AudienceObservation, TemporalEvent, Experiment, EvidenceRecord, CompositionConstraint, Prediction.

## Claim discipline
Behavioral observations and musical descriptors remain separate until an explicit analytical operation relates them. Cognitive descriptors describe model-derived properties of the stimulus; they are not measurements of neural activity. Temporal coincidence is descriptive evidence, not causality.

## Canonical clock
All stimulus and response events use non-negative milliseconds from the start of the analyzed version. Every version has an immutable versionId.

## M0 acceptance criterion
At least two versions can pass through ports, generate audience events, produce retention/hazard outputs, align behavioral events with musical windows, and persist evidence without the core depending on any concrete adapter.
