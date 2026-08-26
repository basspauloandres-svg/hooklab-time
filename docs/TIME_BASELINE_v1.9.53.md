# HookLab TIME — Baseline experimental v1.9.53

Fecha de congelación: 2026-08-25
Estado: baseline experimental de reloj audible / seguimiento local de tempo

## Decisión operativa

Se congela `app-v1.9.53-local-tempo-full-song-p0.html` como baseline experimental para la ruta audible y el seguimiento temporal local de TIME.

Esta decisión se apoya en la prueba completa con `Animal.mp3` (245.0209 s), evaluada auditivamente en iPhone y acompañada por el diagnóstico `HookLab_local_tempo_full_song_v1_9_53.json`.

## Arquitectura congelada

`audio fuente -> detección de ataques -> seguimiento local de periodo/fase -> posiciones de tactus -> render offline pista+click -> WAV único -> HTMLAudioElement nativo`

Invariantes:

- una sola corriente audible;
- `manual_offset_ms = 0`;
- sin salida Web Audio en tiempo real;
- sin iframe;
- pista y claqueta quedan impresas en el mismo render antes de la reproducción;
- el tempo se representa como trayectoria local, no como BPM global impuesto;
- el BPM global puede conservarse únicamente como descriptor resumen.

## Evidencia del caso Animal

- duración: 245.0209167 s;
- ataques detectados: 529;
- pulsos adaptativos: 488;
- BPM mediano adaptativo: 119.535;
- BPM mínimo observado por el seguidor: 118.896;
- BPM máximo observado por el seguidor: 121.414;
- render completo: 3937 ms en la ejecución registrada;
- WAV resultante: 47,044,060 bytes;
- evaluación auditiva del usuario: sincronía percibida como correcta con tempo variable a lo largo de la canción.

## Interpretación experimental

La prueba fija a 120 BPM mostró deriva perceptual aproximadamente hacia los 23 s. La ruta adaptativa corrigió esa deriva y permaneció auditivamente adherida al pulso. Por tanto, para este caso, una constante global de 120 BPM no representa adecuadamente la trayectoria temporal audible.

El valor histórico de -115.2 ms permanece descartado como compensación estructural. Los experimentos posteriores también mostraron que una corrección fija de fase no explica la deriva acumulativa.

## Límites

Este baseline todavía no constituye validación general del algoritmo TIME. La evidencia corresponde a una obra de referencia y a evaluación auditiva humana en el dispositivo de referencia. Antes de promoverlo a baseline general debe superar una prueba de regresión con obras de características temporales distintas.

El seguidor local de v1.9.53 conserva parámetros experimentales (`INIT_PERIOD=.5`, `INIT_ANCHOR=.57`, ventana de observación y ganancias de corrección) derivados durante el P0. Estos parámetros no deben presentarse todavía como universales.

## Próxima compuerta

Regresión mínima multicaso:

1. obra cercana a tempo estable;
2. obra con microvariación humana;
3. obra con introducción ambigua o sin pulso claro;
4. obra con cambio o ruptura métrica/temporal.

Criterios de evaluación:

- adquisición inicial del tactus;
- nivel métrico correcto;
- error de fase perceptual;
- deriva acumulativa;
- estabilidad ante ataques faltantes;
- reacquisición después de regiones ambiguas;
- ausencia de compensación manual de latencia;
- integridad de la ruta audible única.

## Regla de desarrollo

Toda modificación posterior debe compararse contra v1.9.53 y cambiar una variable experimental por vez. La integración con otras capas de TIME no debe alterar silenciosamente esta ruta de reproducción ni el principio de seguimiento local validado.
