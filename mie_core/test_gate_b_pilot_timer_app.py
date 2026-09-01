from pathlib import Path

APP=Path(__file__).resolve().parents[1]/'app-gate-b-pilot-timer-v0.1.html'

def test_gate_b_timer_contract_present():
    s=APP.read_text(encoding='utf-8')
    required=[
        'performance.now()',
        'HOOKLAB_GATE_B_PILOT_APP_v0.3',
        'section_form_plan',
        'tempo_metric_recommendation',
        'harmonic_tonal_recommendation',
        'melodic_rhythmic_recommendation',
        'production_constraints',
        'experimenter_pause_seconds',
        'hooklab_candidates_seen_before_t1:false',
        'artifactReady()',
        'retained:true',
        'Exportar JSON'
    ]
    for token in required:
        assert token in s

def test_finish_requires_complete_contract_and_retained_artifact():
    s=APP.read_text(encoding='utf-8')
    assert 'if(!complete()||!artifactReady()||pauseStart)return' in s
    assert 'finish.disabled=!running||finished||!ok||!aok||!!pauseStart' in s

def test_plain_language_ux_contract():
    s=APP.read_text(encoding='utf-8')
    required_ux=[
        '¿Cómo se diligencia?',
        '¿Qué partes tendrá la canción y en qué orden?',
        'Verso (8)',
        'verso de 8 compases',
        'BPM significa pulsos por minuto',
        '¿Qué base de acordes o centro tonal propones?',
        '¿Cómo imaginas el hook o la idea melódica y rítmica principal?',
        '¿Cómo debería comenzar a producirse y sonar la canción?',
        'Nombre o referencia del trabajo guardado'
    ]
    for token in required_ux:
        assert token in s

def test_preflight_is_required_before_timer_start():
    s=APP.read_text(encoding='utf-8')
    required=[
        'Antes de comenzar',
        'preflightReady()',
        'Verificación de comprensión pendiente',
        'excluded_from_ttpf:true',
        'start.disabled=running||finished||!ok||!metadataReady()',
        'if(!metadataReady()||!preflightReady())'
    ]
    for token in required:
        assert token in s

def test_preflight_covers_all_five_scientific_outputs():
    s=APP.read_text(encoding='utf-8')
    for token in ['id="pf1"','id="pf2"','id="pf3"','id="pf4"','id="pf5"']:
        assert token in s
