# HookLab Producer Interface v0.3 — Delivery Guide

Public interface: https://basspauloandres-svg.github.io/hooklab-time/

## Purpose
Producer Interface v0.3 is the delivery-ready exploratory HookLab workstation. It captures a creative brief, isolates a local aesthetic reference, exposes current scientific evidence and limits, creates deterministic D0 exploratory MIDI/audio variants, measures decision time, records producer evaluation, and exports provenance/session data.

## Standard session
1. Select the musical section and enter text/intention.
2. Optionally load an authorized local aesthetic-reference audio file.
3. Review evidence, limits and provenance.
4. Select `Generar 3 propuestas D0`.
5. Compare thetic, anacrustic and syncopated variants with `Escuchar`.
6. Export a selected MIDI if useful.
7. Export the D0 manifest when provenance is required.
8. Record producer decision, rationale and 1-7 ratings.
9. Save locally and/or export the full session JSON.

## Interpretation
`D0_EXPLORATORY` is an engineering/creative prototype class. It is not `SCIENTIFIC_D` and cannot be interpreted as a scientifically promoted creative prescription.

The local aesthetic reference is isolated by contract:
`AESTHETIC_REFERENCE != M300_EVIDENCE != SUCCESS_EVIDENCE != GATE_A_ACQUISITION`.

## Delivery verification
Automated regression: GitHub Actions run `33446684849` — PASS.
Public deployment: GitHub Actions run `33446721720` — PASS.
Delivery checkpoint: `CHECKPOINTS/DELIVERY_CHECKPOINT_2026-08-31_v1.md`.

## Scientific gate still active
The representation calibration gate remains fail-closed until >=30 independent paired items are available, performance/identity alignment is established, and at least one musical feature reaches Spearman rho >= .80 with median error within its predeclared tolerance. Until then, `SCIENTIFIC_D` remains blocked by design.
