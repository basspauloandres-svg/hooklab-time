# CHECKPOINT — HookLab MIE / Devuélveme el Amor

Fecha: 2026-08-26
Estado: checkpoint de continuidad para migración de chat

## Norte del producto
Construir un sistema automático capaz de analizar profundamente un corpus musical y convertir ese conocimiento en generación original de melodía + ritmo + armonía + texto con calidad comercial. El productor debe actuar principalmente como curador auditivo: aprobar/rechazar resultados, no corregir manualmente notas, pulsos o MIDI. Después, el pipeline debe permitir desarrollar un artista virtual con voz/interpretación, producción, identidad, branding, imagen, video y contenidos para redes/plataformas.

## Función del análisis/transcripción
La transcripción NO es el producto. Es una prueba instrumental de que la máquina escucha correctamente antes de aprender relaciones generativas del corpus.

Criterio:
`audio -> máquina -> eventos musicales -> resíntesis -> evaluación auditiva humana`

Si la resíntesis reproduce de forma suficientemente fiel la melodía percibida, la representación puede usarse para análisis posterior. La salida prioritaria para el evaluador es audio; MIDI/JSON/logs quedan para trazabilidad y diagnóstico.

## Golden case actual
Obra: **Devuélveme el Amor**
Intérprete de referencia: **Luis Miguel**
Archivo de trabajo aportado por el usuario en el chat actual: `Devuélveme El Amor(1).mp3`

Este es el caso correcto de Luis Miguel. No confundir con `Los Muchachos De Hoy`, que pertenece a otro registro previo.

## Decisión aprobada de beat / tactus — 2026-08-26
El motor actualmente considerado **mejor referencia operativa para detección de pulso en el corpus inicial** es:

`app-recovery-lm-neural-beatthis-v1.9.3.html`

URL de referencia:
`https://basspauloandres-svg.github.io/hooklab-time/app-recovery-lm-neural-beatthis-v1.9.3.html`

Evaluación auditiva del productor: **APROBADO**.
Observación posterior: el productor indica que esta versión reconoce correctamente el pulso en la gran mayoría de los temas probados.

Arquitectura recuperada:
`Beat This neuronal -> single-clock -> CTL conservador -> resolución de tactus -> deduplicación`

Esta versión queda como **baseline primario de beat/tactus** para el trabajo inmediato con Devuélveme el Amor y para las siguientes pruebas del corpus, hasta que una comparación controlada demuestre una mejora reproducible.

No sustituir este baseline por detectores simplificados de onsets/periodicidad sin una prueba comparativa aprobada.

## Golden case Animal
La máquina `app-v1.9.65-auto-acquisition-full-song-p0.html` permanece preservada como **golden case especializado de seguimiento temporal adaptativo** para `Animal.mp3`.

Evidencia aprobada de Animal:
- adquisición automática ~119.522 BPM;
- periodo inicial ~0.502 s;
- ancla ~0.507 s;
- score ~0.9205;
- 488 pulsos seguidos durante la canción;
- BPM mediano ~119.533;
- rango adaptativo ~118.896–120.430 BPM;
- una sola corriente audible;
- render offline;
- reproducción nativa;
- offset manual = 0 ms.

La transferencia directa de v1.9.65 a Devuélveme el Amor fue **RECHAZADA** auditivamente. Por tanto, v1.9.65 no es el baseline general de beat; se conserva como golden case especializado de seguimiento adaptativo una vez adquirido correctamente el reloj.

## Hipótesis métrica T / 2T
Se mantiene como hipótesis de trabajo que parte de los fallos de transferencia entre motores puede estar relacionada con selección del nivel métrico (`T`, `2T`, `T/2`) y no necesariamente con incapacidad del sensor acústico para detectar periodicidad.

Estado de esta hipótesis: **plausible, aún no cerrada**. No convertirla en regla del motor hasta una prueba controlada.

## Estado recuperado del entrenamiento anterior
- El trabajo previo llegó a una transcripción/reconstrucción melódica de Devuélveme el Amor que el usuario considera que puso la vara muy alta.
- La dimensión melódica estaba sustancialmente conseguida; la parte rítmica era la carencia principal percibida.
- P30-SCORE-002 fue recuperado como una representación melódica auditivamente cercana al resultado recordado y su versión no cuantizada fue preferida frente a la versión totalmente cuantizada.
- La estrategia actual es conservar la melodía interpretada intacta y usar un beat aprobado como sistema de coordenadas rítmicas.
- P16 v3 aparece documentado como `REPRODUCTION_PASS`, pero no debe confundirse automáticamente con el transcriptor específico de Devuélveme el Amor.

## Arquitectura conceptual para MIE
Separar:
1. **Tiempo físico**: segundos observables del audio.
2. **Tiempo musical**: beat/subdivisión/compás inferidos posteriormente.

La melodía debe representarse inicialmente como:
`pitch + onset_s + offset_s/duration_s + confidence`

Después se proyecta sobre el beat aprobado para derivar:
`beat_index + phase + deviation_ms + structural_position_candidate`

El error métrico no debe contaminar la extracción de alturas y duraciones físicas.

## Próximo objetivo operativo
**BEAT APROBADO -> COORDENADAS RÍTMICAS -> TRANSCRIPCIÓN -> ARMONÍA**

1. Mantener `app-recovery-lm-neural-beatthis-v1.9.3.html` como baseline primario de beat/tactus.
2. Obtener/registrar su salida temporal sobre Devuélveme el Amor.
3. Proyectar P30-SCORE-002 intacto sobre esa rejilla aprobada.
4. Derivar coordenadas rítmicas por nota sin mover físicamente la interpretación vocal.
5. Construir la transcripción melódico-rítmica.
6. Integrar la armonía ya disponible después de aprobar la transcripción.
7. Solo después avanzar al análisis relacional para reglas generativas.

## Restricciones permanentes
- No reiniciar TIME desde cero.
- No reabrir problemas ya resueltos sin evidencia de regresión.
- No acumular capas experimentales en el motor operativo.
- No hacer depender el resultado de correcciones manuales del productor.
- No generar canciones completas antes de que la máquina pueda escuchar/representar adecuadamente el material de referencia.
- Priorizar prototipos auditivos y máquinas sobre explicaciones teóricas extensas.
- Mantener trazabilidad técnica detrás de la experiencia auditiva.
- Todo resultado entra al baseline únicamente después de aprobación auditiva del productor.
- Los experimentos rechazados permanecen como genealogía y no como estado vigente.

## Ruta posterior al motor de escucha
`representación fiable -> análisis multicapa -> relaciones ritmo/melodía/armonía/texto/estructura -> reglas condicionadas -> generación de hooks -> curación aprobar/rechazar -> desarrollo de canción -> voz/artista virtual -> producción -> branding/imagen -> video/contenido -> distribución`

## Principio de producto
Tecnología al servicio del productor. La máquina analiza, propone y genera; el productor decide qué merece continuar.
