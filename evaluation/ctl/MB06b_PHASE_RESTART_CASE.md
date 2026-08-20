# MB06b — corrected phase-restart benchmark

Purpose: replace the invalid assumption that original MB06 contained a detectable phase restart.

Original MB06 is retained unchanged as an identifiability control. Its post-gap beat at 15.250 s is exactly 6 periods after the last pre-gap beat at 11.650 s for 100 BPM (IBI 0.600 s), so event timing alone cannot distinguish stopped-and-restarted clock from silent continuation.

MB06b pre-specification:
- tempo before gap: 100 BPM
- last pre-gap beat: 11.650 s
- active gap / fermata region: 12–15 s
- first post-gap beat: 15.400 s
- post-gap tempo: 100 BPM
- phase offset relative to silent continuation: +0.150 s = 0.25 cycle
- expected classification: `CLOCK_STOP_RESTART`
- no tempo transition should be emitted

The +0.25-cycle offset is fixed before stress testing and is not tuned to the detector output.
