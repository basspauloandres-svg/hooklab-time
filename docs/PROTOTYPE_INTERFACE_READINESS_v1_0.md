# Prototype Interface Readiness v1.0

Estado: congelado como criterio de activación.

La interfaz integral HookLab/TIME se construirá únicamente cuando Analyzer v1 demuestre generalización suficiente bajo parámetros globales congelados.

## Criterios mínimos de activación

La interfaz pasa de `DEFERRED` a `ELIGIBLE` cuando se cumplen simultáneamente:

1. al menos 5 canciones reales con `FULL_TMT_READY` o `STRICT_REPLAY_PASS`;
2. al menos 2 géneros representados entre los casos aprobados;
3. al menos 3 estilos representados entre los casos aprobados;
4. ausencia de ajustes de parámetros específicos por canción (`GLOBAL_FROZEN`);
5. conservación de todos los fallos como evidencia de límites de generalización.

Estos umbrales son criterios de ingeniería para justificar el costo de construir la interfaz. No constituyen validación estadística del modelo ni evidencia de éxito musical.

## Función prevista de la interfaz

La interfaz será una capa operativa delgada. No contendrá lógica analítica propia.

Flujo:

`identificar canción → género/estilo → Analyzer → compuertas → T/M/Texto/TMT → fingerprint → cohorte → referencia estadística → trazabilidad → exportación`

Modo generativo futuro, separado:

`género/estilo + historia/propósito → cohorte → restricciones estadísticas validadas → Texto+Melodía+Tiempo → audio prototipo → comparación contra cohorte`

## Regla de gobernanza

Mientras `prototype_interface_status = DEFERRED`, cualquier trabajo de interfaz queda subordinado a la batería de generalización. Cuando el reporte automático marque `ELIGIBLE`, se habilita la construcción del prototipo integral.
