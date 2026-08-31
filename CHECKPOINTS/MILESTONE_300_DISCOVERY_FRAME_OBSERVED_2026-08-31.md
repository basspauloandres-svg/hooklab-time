# Milestone 300 — observed discovery frame checkpoint

Date: 2026-08-31
Branch: `mie/golden-forensic-v0.3`
State: `300/300 DISCOVERY FRAME OBSERVED / QUALIFICATION IN PROGRESS`

## Observed execution
GitHub Actions run `33408688491` executed `milestone-300-discovery-frame.yml` successfully and produced artifact `milestone-300-discovery-frame` (artifact id `9764206828`, digest `sha256:024460d8bf81b736c02a1101b5fc3f07432cb5b9cfcde6bfccfd60e83a8bd056`).

Observed frame result:
- candidate_count = 300
- frame_complete = true
- 20 chart years represented (2006-2025)
- exactly 15 Billboard Year-End ranks per year
- Spotify >=100M snapshot: 298/300
- Spotify below 100M snapshot: 2/300

The two below-threshold/mismatch cases are retained for identity/version audit rather than silently rejected because one observed metadata row (`Cheerleader`) maps to a mismatched artist and therefore demonstrates why identity must precede final failure classification.

## Scientific boundary
These 300 rows are a mass-success discovery frame, not 300 Dance-Pop rows and not 300 scientifically promoted Matrix-X observations. Genre/style, YouTube threshold, identity/version, symbolic source, FULL_SONG, provenance and FULL_TMT remain independent gates.

## Code
- `mie_core/milestone_300_sampling_frame_builder.py`
- `mie_core/test_milestone_300_sampling_frame_builder.py`
- `.github/workflows/milestone-300-discovery-frame.yml`

## Next active operation
Complete dual-platform success qualification and then genre/style stratification before symbolic-source promotion. No row may enter Matrix X solely because it belongs to this 300-song frame.
