# HookLab TIME — Microbenchmark diagnóstico beat/tactus v0.1

Objetivo: someter B0 (Beat This directo) y B1 (HookLab) a perturbaciones controladas con ground truth matemáticamente exacto. Esta fase no evalúa metro, downbeat ni acento y no sustituye benchmarks musicales reales.

## Casos

| ID | Duración | Condición | Ground truth / criterio |
|---|---:|---|---|
| MB01 | 32 s | Pulso constante 120 BPM | Beat cada 0.5 s. Control basal. |
| MB02 | 40 s | Accelerando lineal 80→140 BPM | Fase obtenida por integración continua de tempo. |
| MB03 | 40 s | Ritardando lineal 140→70 BPM | Fase obtenida por integración continua de tempo. |
| MB04 | 40 s | Cambio abrupto 120→80 BPM en 20 s | Último beat pre-cambio y primer beat post-cambio definidos por dos relojes contiguos. |
| MB05 | 36 s | Silencio 12–18 s y reentrada a 120 BPM | No se puntúan beats dentro del silencio; se mide latencia de readquisición desde 18 s. |
| MB06 | 36 s | Fermata 12–15 s | El reloj se detiene: no hay beats durante la fermata. Tras 15 s inicia una nueva fase a 100 BPM. |
| MB07 | 36 s | Ataques explícitos retirados 12–20 s, actividad tonal sostenida | El tactus de 105 BPM continúa durante toda la zona; prueba continuidad sin transientes fuertes. |
| MB08 | 36 s | Ambigüedad half/double | Tactus objetivo 90 BPM; subdivisión explícita a 180 BPM y acento secundario cada 2 tactus. Penaliza saltos de nivel. |

## Principios

1. Los parámetros se fijan antes de observar resultados de HookLab.
2. El generador produce WAV + `.beats` + `manifest.json` automáticamente.
3. MB05 usa una máscara de evaluación para no considerar el silencio como error de omisión; la readquisición se evalúa por separado.
4. MB06 distingue fermata de silencio: el beat de referencia realmente se detiene y reinicia con nueva fase.
5. MB07 mantiene actividad sonora sin ataques de beat prominentes; aquí sí continúa el beat de referencia.
6. MB08 fija el tactus de referencia en 90 BPM; 180 BPM es subdivisión, no beat de referencia.
7. Ningún caso contiene información métrica destinada a abrir la compuerta de acento.

## Salidas

`generated/<ID>.wav` — estímulo mono PCM 44.1 kHz/16 bit.

`generated/<ID>.beats` — tiempos de beat de referencia en segundos.

`generated/<ID>.mask.json` — ventanas excluidas y eventos de transición, cuando corresponda.

`generated/manifest.json` — parámetros completos y versión del generador.

El benchmark es diagnóstico. Las afirmaciones de generalización requieren posteriormente SMC, ASAP, Mazurka u otros datasets con música real.