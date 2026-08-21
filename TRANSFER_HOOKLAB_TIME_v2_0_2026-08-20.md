# HookLab TIME — Documento de evidencia y transferencia integral v2.0

**Corte operativo:** 20 de agosto de 2026, después de pruebas v1.9.9 y auditoría de `Animal.mp3`.

**Regla de restauración:** el nuevo chat debe leer este documento completo antes de proponer cambios. No debe reiniciar decisiones resueltas, borrar regresiones, ajustar parámetros a una sola canción ni reabrir metro/downbeat/acento antes de validar beat/tactus y reproducción audible.

## Estado ejecutivo

- Beat This small pretrained ONNX permanece como detector primario de eventos de beat.
- La capa HookLab implementa continuidad/CTL, selección de tactus, supresión de duplicados, abstención y auditoría de fase.
- Metro/downbeat/acento está congelado deliberadamente.
- Phase Restart v0.3 reconoce `CLOCK_CONTINUES`, `CLOCK_STOP_RESTART`, `SILENCE` y `UNCERTAIN`.
- El pipeline audio→clock distingue en benchmark sintético MB05/MB06b/MB07 sin usar la etiqueta del caso como decisión.
- Tactus Octave v0.1 resuelve el caso sintético 90/180 por saliencia alternante, no por umbral BPM rígido.
- v1.9.3 corrigió relojes superpuestos y deduplicó tactus.
- v1.9.6 corrigió la exportación de la auditoría fase/latencia.
- En `Dime ok salsa`, fase interna mediana = −0.6 ms, MAD = 6.08 ms; la compensación perceptual funcional en el dispositivo probado fue +115 ms.
- En `Animal`, tactus ≈119.52 BPM, fase mediana = 1.35 ms, MAD = 3.64 ms, p95 = 13.25 ms.
- **P0 actual:** v1.9.9 queda en “esperando” y no aplica compensación automática de salida.

## Decisiones consolidadas

1. No tocar beat/tactus para corregir latencia audible.
2. Latencia y compensación pertenecen a una capa separada de reproducción.
3. `UNCERTAIN` es un resultado válido cuando la evidencia es insuficiente.
4. Silencio, fermata/reinicio y pérdida de ataques son estados distintos.
5. Los cambios aproximados 1:2 no son automáticamente cambios de tempo.
6. Localización y confirmación de transición son conceptos separados.
7. No usar reglas rígidas como “si BPM > X dividir por dos”.
8. Metro/downbeat/acento no se reabre hasta cerrar beat/tactus + reproducción.

## Microbenchmark MB01–MB08

- MB01: tempo constante 120; control de estabilidad y duplicación local.
- MB02: accelerando 80→140; problema histórico de falsas transiciones. CTL posterior trata drift como continuo.
- MB03: ritardando 140→70; mismo problema histórico.
- MB04: salto 120→80; CTL v0.7 separa localización de confirmación.
- MB05: silencio 12–18; pipeline audio→clock v0.2 devuelve `SILENCE`.
- MB06b: fermata/reinicio; Phase Restart v0.3 + audio evidence devuelve `CLOCK_STOP_RESTART`.
- MB07: ataques ausentes; Phase Restart v0.3 + audio evidence devuelve `CLOCK_CONTINUES`.
- MB08: 90 vs subdivisión 180; Tactus Octave v0.1 selecciona ~89.28 desde ~178.55 BPM en el caso sintético.

## Phase Restart v0.3

Banco de estrés MB06b/MB07: 2.000 repeticiones por condición, jitter 0–20 ms, pérdida aleatoria 0–40%; 80.000 pruebas reportadas y 0 decisiones binarias incorrectas. Los casos de evidencia insuficiente pasan a `UNCERTAIN`.

Resultado: `evaluation/ctl/RESULTS_phase_restart_v0_3_EXECUTED.md`.

## Audio evidence y audio→clock

- `evaluation/ctl/audio_evidence_v0_1.py` fue corregido después de que v0.1 clasificara mal el tone bed sostenido de MB06b/MB07.
- `evaluation/ctl/run_audio_clock_pipeline_v0_1.py` integra WAV → actividad/onsets → estado del reloj.
- Resultado ejecutado: `evaluation/ctl/RESULTS_audio_clock_pipeline_v0_2_EXECUTED.md`.

## Tactus Octave

Código: `evaluation/ctl/tactus_octave_v0_1.py`.
Resultado: `evaluation/ctl/RESULTS_tactus_octave_v0_1_EXECUTED.md`.

## Serie móvil v1.9.x

- `app-v1.9.html`: PRETEST inicial; problemas de despliegue/herencia v1.7.
- `app-v1.9-test.html`: launcher cache-safe; no usar como evidencia porque seguía mostrando contenido v1.7.
- `app-v1.9-direct.html`: intento de eliminar iframes heredados.
- `app-v1.9-mixer.html`: primeros controles Pista/Beat/Acento; fallaron inicialmente.
- `app-v1.9.3-pretest.html`: single-clock + CTL conservador + tactus deduplicado + mezclador funcional.
- `app-v1.9.4-latency-audit.html`: primera auditoría; exportación devolvía null.
- `app-v1.9.5-latency-audit-fix.html`: fix incompleto.
- `app-v1.9.6-latency-audit-exportfix.html`: auditoría válida.
- `app-v1.9.7-offset-calibration.html`: calibración manual; +115 ms alineó Dime ok salsa.
- `app-v1.9.8-auto-output-comp.html`: primer intento automático.
- `app-v1.9.9-auto-comp-robust.html`: último intento; bug abierto porque queda “esperando”.

## Evidencia real: Dime ok salsa

### Fallo inicial v1.9

- raw beats: 542
- predictivos: 1179
- pulse runs: 7
- transiciones: 6
- tactus: 1138
- estimated tactus BPM: 473.493

Conclusión: relojes superpuestos y confusión de octava.

### Después de v1.9.3

- predictivos: 502
- tactus: 502
- pulse runs: 1
- transiciones: 0
- estimated tactus BPM: 167.882

### Auditoría v1.9.6

- phase median: −0.60 ms
- phase MAD: 6.08 ms
- p95 abs: 349.11 ms
- count-based BPM: 144.448
- median-IBI BPM: 167.879
- coverage: 208.102 s

Interpretación: alineación central interna muy buena; p95 alto y divergencia conteo/IBI indican huecos/outliers que todavía deben auditarse por segmentos.

### Reproducción

En v1.9.7, `playback_offset_ms = 115` produjo alineación perceptual. En pantalla se había observado ~115.2 ms de latencia WebAudio. Esto debe modelarse como compensación de salida, no como retraso del beat.

## Evidencia real: Animal

- duration: 245.0209 s
- raw beats: 483
- predictivos: 488
- pulse runs: 1
- transiciones: 0
- tactus: 488
- estimated tactus BPM: 119.519
- phase median: 1.35 ms
- phase MAD: 3.64 ms
- p95 abs: 13.25 ms
- count-based BPM: 119.524
- median-IBI BPM: 119.520
- coverage: 244.469 s

Animal es el control real limpio para regresión.

## Arquitectura de latencia requerida

Registrar por separado:

- `detected_output_latency_ms`
- `base_compensation_ms` (usar precisión decimal completa)
- `fine_adjustment_ms` (inicial 0.0)
- `total_compensation_ms = base + fine`
- fuente/API usada para medir (`baseLatency`, `outputLatency`, etc.)

No fijar +115 ms universalmente; fue la ruta/dispositivo probados.

## P0 — tarea inmediata

Corregir v1.9.9 para que la lectura de latencia se enganche al ciclo real de `play/resume` del `AudioContext`, con polling solo como fallback acotado. La UI debe salir de “esperando”, mostrar el valor decimal completo, aplicarlo a la claqueta sin alterar raw beat/tactus y dejar ajuste fino = 0.0.

Pruebas de aceptación:

1. Dime ok salsa: compensación automática cercana a la ruta observada (~115.2 ms si la ruta no cambia).
2. Animal: mantener ~119.52 BPM y fase interna ~1–4 ms.
3. Verificar que el JSON registre latencia base, fino y total.
4. Después probar ≥3 canciones nuevas contrastantes.
5. Solo entonces reconsiderar metro/downbeat/acento.

## Rutas persistentes

- Repositorio: https://github.com/basspauloandres-svg/hooklab-time
- GitHub Pages: https://basspauloandres-svg.github.io/hooklab-time/
- CTL: https://github.com/basspauloandres-svg/hooklab-time/tree/main/evaluation/ctl
- Phase Restart result: https://github.com/basspauloandres-svg/hooklab-time/blob/main/evaluation/ctl/RESULTS_phase_restart_v0_3_EXECUTED.md
- Audio clock result: https://github.com/basspauloandres-svg/hooklab-time/blob/main/evaluation/ctl/RESULTS_audio_clock_pipeline_v0_2_EXECUTED.md
- Tactus octave result: https://github.com/basspauloandres-svg/hooklab-time/blob/main/evaluation/ctl/RESULTS_tactus_octave_v0_1_EXECUTED.md

## Archivos de evidencia a conservar

- `Dime_ok_salsa_resumen.json` (varias iteraciones, incluyendo v1.9 fallida y v1.9.6 auditada)
- `Animal_resumen.json`
- `Dime ok salsa.mp3.LAB.summary (1).json`
- `HookLab_TIME_Documento_Evidencia_Migracion_v1_0.docx` (histórico; supersedido por v2.0)
- Consolas/labs previos subidos al chat: Beat Audit Console, Validation LAB v3.0, AUTO TRANSIENT→BEAT, Multiband Tactus & Meter.

## Frase de restauración

> Lee completamente el Documento de evidencia y transferencia integral HookLab TIME v2.0. Trátalo como estado oficial del desarrollo. No reinicies decisiones ni vuelvas a etapas ya cerradas. Continúa exactamente desde el bug P0 de compensación automática de salida posterior a v1.9.9, manteniendo intacto beat/tactus, conservando congelado metro/downbeat/acento y usando GitHub como fuente persistente de código y resultados.
