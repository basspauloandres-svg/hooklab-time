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

## Estado recuperado del entrenamiento anterior
- El trabajo previo llegó a una transcripción/reconstrucción melódica de Devuélveme el Amor que el usuario considera que puso la vara muy alta.
- La dimensión melódica estaba sustancialmente conseguida; la parte rítmica era la carencia principal percibida.
- No existe todavía evidencia recuperada suficiente para afirmar que tenemos el código exacto del transcriptor anterior; no inventar ni reconstruir desde recuerdos parciales si aparecen artefactos recuperables.
- P16 v3 aparece documentado como `REPRODUCTION_PASS`, pero no debe confundirse automáticamente con el transcriptor específico de Devuélveme el Amor.

## TIME — conocimiento que se conserva
Baseline limpio operativo: **v1.9.65**.
Arquitectura validada: archivo -> decode -> ataques -> adquisición automática periodo/fase -> seguimiento local adaptativo -> render offline canción+click -> WAV único -> reproducción nativa; `manual_offset_ms = 0`.

Aprendizaje clave del caso Luis Miguel: periodicidad física y nivel métrico son distintos; evitar confundir aproximadamente 70 BPM en blancas con 140 BPM en negras.

Los experimentos v1.9.66–v1.9.72 son laboratorio/diagnóstico y NO deben heredarse como capas operativas. v1.9.72 fue FAIL perceptual: 12 reacquisiciones y saltos entre hipótesis de ~157, 120, 75, 105, 145, 213 y ~157 BPM. Regla arquitectónica: no construir capa sobre capa; volver a un baseline limpio y cambiar una variable cuando sea necesario.

TIME queda congelado temporalmente. No continuar desarrollando un beat tracker universal antes de avanzar en melodía.

## Arquitectura conceptual para MIE
Separar:
1. **Tiempo físico**: segundos observables del audio.
2. **Tiempo musical**: beat/subdivisión/compás inferidos posteriormente.

La melodía debe poder representarse inicialmente como:
`pitch + onset_s + offset_s/duration_s + confidence`

El error métrico no debe contaminar la extracción de alturas y duraciones físicas.

## Próximo objetivo operativo
**RECUPERAR -> REPRODUCIR -> VERIFICAR -> CONGELAR -> AVANZAR**

1. Localizar cualquier artefacto previo recuperable del transcriptor de Devuélveme el Amor: código, MIDI, representación de notas, audio resintetizado, parámetros o diagnósticos.
2. No construir un transcriptor nuevo hasta agotar esa recuperación.
3. Si el artefacto exacto no existe, construir desde arquitectura limpia una máquina mínima de escucha melódica.
4. Entrada: `Devuélveme El Amor(1).mp3`.
5. Salida: eventos `pitch + onset + duration` en tiempo físico y resíntesis audible.
6. Evaluación del productor: `APRUEBA / RECHAZA`.
7. Cuando la calidad iguale o supere el golden case anterior, congelar el motor melódico.
8. Atacar después exclusivamente la dimensión rítmica necesaria para relacionar la melodía con la rejilla musical.

## Restricciones permanentes
- No reiniciar TIME desde cero.
- No reabrir problemas ya resueltos sin evidencia de regresión.
- No acumular capas experimentales en el motor operativo.
- No hacer depender el resultado de correcciones manuales del productor.
- No generar canciones completas antes de que la máquina pueda escuchar/representar adecuadamente el material de referencia.
- Priorizar prototipos auditivos y máquinas sobre explicaciones teóricas extensas.
- Mantener trazabilidad técnica detrás de la experiencia auditiva.

## Ruta posterior al motor de escucha
`representación fiable -> análisis multicapa -> relaciones ritmo/melodía/armonía/texto/estructura -> reglas condicionadas -> generación de hooks -> curación aprobar/rechazar -> desarrollo de canción -> voz/artista virtual -> producción -> branding/imagen -> video/contenido -> distribución`

## Principio de producto
Tecnología al servicio del productor. La máquina analiza, propone y genera; el productor decide qué merece continuar.
