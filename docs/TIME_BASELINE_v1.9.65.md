# HookLab TIME — Baseline experimental v1.9.65

Fecha: 2026-08-25
Estado: baseline experimental candidato para reloj audible automático

## Resultado de la compuerta

`app-v1.9.65-auto-acquisition-full-song-p0.html` supera la prueba auditiva completa del caso de referencia `Animal.mp3` en iPhone, sin error percibido a lo largo de la obra.

## Arquitectura

`audio fuente -> decode -> ataques -> adquisición automática de periodo/fase (primeros 12 s) -> seguimiento local adaptativo -> tactus -> render offline pista+click -> WAV único -> HTMLAudioElement nativo`

Invariantes preservados:

- una sola corriente audible;
- salida Web Audio en tiempo real desactivada;
- render offline;
- reproducción nativa;
- `manual_offset_ms = 0`;
- tempo modelado como trayectoria local;
- sin parámetros manuales de periodo o ancla específicos de Animal.

## Evidencia del diagnóstico v1.9.65

- fuente: `Animal.mp3`;
- duración: 245.0209167 s;
- ataques detectados: 529;
- adquisición automática: periodo 0.502 s;
- ancla automática: 0.507 s;
- BPM inicial: 119.521912;
- score de adquisición: 0.920466;
- hits de adquisición: 25;
- pulsos adaptativos: 488;
- BPM mediano adaptativo: 119.533;
- rango adaptativo: 118.896–120.430 BPM;
- offset manual: 0 ms;
- render registrado: 4363 ms;
- WAV: 47,044,060 bytes;
- evaluación auditiva humana: PASS, canción completa sin error percibido.

## Cambio respecto de v1.9.53

v1.9.53 dependía de `INIT_PERIOD=.5` e `INIT_ANCHOR=.57`, derivados experimentalmente del caso Animal. v1.9.65 elimina ambos valores de la inicialización operativa y los obtiene automáticamente desde la evidencia de ataques de los primeros 12 s.

El seguidor local posterior conserva la lógica validada previamente. Por tanto, la variable experimental modificada entre ambos baselines es la inicialización del periodo/fase.

## Observaciones de robustez interna

La trayectoria contiene regiones con observaciones faltantes y correcciones locales relativamente grandes. El seguidor mantiene continuidad y recupera el pulso sin compensación manual. En el diagnóstico aparecen, entre otras, perturbaciones alrededor de 58 s, 122 s, 143–149 s, 186–193 s y 216–230 s.

El mayor error local registrado en la trayectoria es aproximadamente -81.59 ms alrededor de 216.84 s; el seguidor reajusta el periodo y continúa la trayectoria. Este comportamiento debe considerarse evidencia del caso, no todavía una garantía de reacquisición general.

## Decisión

v1.9.65 reemplaza a v1.9.53 como **candidato de baseline automático para regresión multicaso**. v1.9.53 se conserva como baseline histórico de referencia para comprobar que futuras modificaciones no deterioren la ruta audible ni el seguimiento local.

## Próxima compuerta

No añadir nuevas capas funcionales antes de una regresión con canciones distintas. La siguiente etapa debe evaluar generalización de:

1. selección del nivel métrico;
2. adquisición automática de periodo;
3. adquisición automática de fase;
4. seguimiento local;
5. reacquisición tras regiones ambiguas;
6. estabilidad de la corriente audible única.

Casos mínimos:

- tempo aproximadamente estable distinto de ~120 BPM;
- interpretación con microvariación humana;
- introducción ambigua o sin pulso claro;
- cambio temporal o métrico.

Toda prueba debe conservar `manual_offset_ms = 0` y comparar los resultados contra v1.9.65 y, cuando corresponda, contra v1.9.53.
