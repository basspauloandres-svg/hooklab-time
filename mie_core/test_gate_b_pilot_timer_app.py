from pathlib import Path

APP=Path(__file__).resolve().parents[1]/'app-gate-b-pilot-timer-v0.1.html'

def test_gate_b_timer_contract_present():
    s=APP.read_text(encoding='utf-8')
    required=[
        'performance.now()',
        'HOOKLAB_GATE_B_PILOT_APP_v0.1',
        'section_form_plan',
        'tempo_metric_recommendation',
        'harmonic_tonal_recommendation',
        'melodic_rhythmic_recommendation',
        'production_constraints',
        'experimenter_pause_seconds',
        'hooklab_candidates_seen_before_t1:false',
        "document.getElementById('finish').disabled=!running||finished||!ok||!!pauseStart",
        'Exportar JSON'
    ]
    for token in required:
        assert token in s

def test_finish_requires_complete_contract():
    s=APP.read_text(encoding='utf-8')
    assert 'if(!complete()||pauseStart)return' in s
    assert "if(!metadataReady())" in s
