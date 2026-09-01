# Bitácora de foco HookLab/TIME — Principio rector de decisión por datos v1.0

Fecha de formalización: 2026-08-29
Estado: CONGELADO / CHECKPOINT PERMANENTE

## Propósito
Este documento funciona como punto de retorno cuando el desarrollo pierda foco. Toda modificación del analizador, del modelo estadístico o del generador debe contrastarse contra este principio antes de incorporarse.

## Principio rector
**HookLab/TIME no decide previamente qué características debe tener una canción exitosa. Construye observaciones reproducibles y permite que la estructura estadística del corpus determine qué variables, combinaciones e interacciones contienen información discriminativa o predictiva.**

La dirección epistemológica obligatoria es:

`DATOS → ESTRUCTURA ESTADÍSTICA → PATRONES → CONTRASTE → VALIDACIÓN → DECISIÓN`

Nunca debe invertirse a:

`PREFERENCIA / INTUICIÓN → REGLA → BÚSQUEDA DE DATOS QUE LA CONFIRMEN`.

## Reglas operativas congeladas
1. Ninguna variable se considera favorable por anticipado. Repetición, saliencia, rango, intervalos, tempo, densidad, registro, prosodia y cualquier otra medida son inicialmente variables observadas.
2. No se asignan pesos humanos para determinar importancia predictiva. Los pesos exploratorios pueden utilizarse para diagnóstico, pero deben quedar identificados como provisionales y fuera de la inferencia final.
3. No existe un perfil de «canción ideal» definido a priori.
4. Una variable no se conserva como predictor porque resulte musicalmente plausible. Su capacidad informativa debe demostrarse en los datos y mantenerse en validación fuera de muestra.
5. Las interacciones Texto × Melodía × Tiempo deben ser evaluadas empíricamente; no se presupone su dirección ni magnitud.
6. Las anomalías se documentan antes de excluirse. Su contradicción con una expectativa humana no constituye criterio de eliminación.
7. La literatura científica orienta operacionalización, comparación e interpretación; no sustituye el resultado empírico del corpus.
8. Una discrepancia entre literatura y datos se conserva como hallazgo a contrastar y discutir.
9. No se construirá un `success score` antes de contar con corpus, variable de resultado independiente, análisis de generalización y validación fuera de muestra.
10. El sistema debe admitir que pueden existir múltiples configuraciones estadísticas asociadas con resultados semejantes. No se forzará una única fórmula del éxito.
11. La estadística restringirá posteriormente el espacio generativo; no compondrá mediante reglas arbitrarias introducidas por el equipo.
12. Toda decisión generativa deberá poder rastrearse hasta evidencia estadística validada o quedar explícitamente identificada como condición experimental.

## Separación entre X y Y
`X` = características observables y reproducibles de Texto, Melodía, Tiempo y sus relaciones.

`Y` = medida independiente del resultado que se decida estudiar posteriormente.

El objetivo inferencial se formulará como el estudio de `P(Y|X)` y no como la búsqueda retrospectiva de rasgos que confirmen una teoría previa.

## Secuencia científica
1. Construir Song Objects comparables.
2. Construir matriz X.
3. Evaluar calidad, distribuciones, asociaciones, redundancia y estructura multivariada.
4. Incorporar Y con definición independiente y trazable.
5. Entrenar modelos bajo separación estricta entre entrenamiento y validación.
6. Evaluar desempeño fuera de muestra.
7. Examinar estabilidad de variables e interacciones.
8. Retener únicamente patrones que sobrevivan al contraste definido.
9. Traducir patrones validados en restricciones generativas condicionadas.
10. Evaluar los prototipos generados como una nueva fase experimental.

## Pregunta de control permanente
Antes de introducir una regla, peso, umbral interpretativo o decisión compositiva, preguntar:

> **¿Esta decisión proviene de los datos o estamos introduciendo lo que esperamos encontrar?**

Si la respuesta es que procede de expectativa, intuición o conveniencia musical, la decisión no puede convertirse en regla inferencial. Debe permanecer como hipótesis o condición experimental explícita.

## Criterio de retorno al foco
Cuando el proyecto se disperse hacia transcripción, infraestructura, MIDI, modelos acústicos, interfaces o generación, recordar:

**Los sensores son medios. El objetivo analítico es producir datos comparables. Los datos deben revelar la estructura. La estructura validada debe orientar las decisiones. La generación ocurre después de la fase deductiva y estadística.**

## Estado del proyecto al congelar este principio
- Analyzer v1.0: en cierre de integración.
- Núcleo analítico: Texto ↔ Melodía ↔ Tiempo.
- Armonía: `FROZEN_CONTEXTUAL_ONLY`.
- Song Object TMT: definido.
- Structural Fingerprint: implementado.
- Distinción entre canciones: implementada por dimensiones; sin porcentaje global arbitrario.
- Corpus Reference Model: siguiente etapa después de disponer de Song Objects homogéneos.
- Predicción de éxito: hipótesis futura a someter a contraste; no resultado asumido.
- Generación: posterior a la fase deductiva y a la validación estadística.

## Regla de gobernanza
Cualquier modificación futura que contradiga este checkpoint requiere:
1. identificar explícitamente la regla que se propone modificar;
2. aportar evidencia empírica o metodológica suficiente;
3. documentar la razón del cambio;
4. versionar la nueva decisión;
5. conservar esta versión como antecedente trazable.
