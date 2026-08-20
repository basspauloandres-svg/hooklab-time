# HookLab TIME — evaluación B0 vs B1

Fase cerrada a **beat/tactus**. No se evalúan ni ajustan metro, downbeat o acento.

## Baselines
- **B0**: salida directa `beats_s` de Beat This.
- **B1**: salida de tactus de HookLab (`tactus_s` o `single_tactus_s`; `beats_s` solo como compatibilidad si la versión aún no exporta tactus separado).

## Ground truth
Cada prueba debe registrar una correspondencia inequívoca entre audio, performance y archivo de anotación. En ASAP se usan únicamente filas `b` y `db` como tiempos de beat; las etiquetas de signatura se conservan para trazabilidad pero no corrigen el beat.

## Métricas
El script `beat_tactus_eval.py` usa `mir_eval.beat.evaluate` y conserva los nombres estándar: F-measure, Cemgil, Goto, P-score, Correct Metric Level Continuous/Total y Any Metric Level Continuous/Total.

Diagnósticos HookLab exploratorios:
- `BNM = AMLt - CMLt`: brecha de nivel métrico.
- cambios espurios `T↔2T↔3T` cuando el JSON exporta una traza explícita.

## Ejecución
```bash
python -m pip install -r evaluation/requirements.txt
python evaluation/beat_tactus_eval.py --reference REF.txt --estimate SALIDA.json --mode b0 --output b0.json
python evaluation/beat_tactus_eval.py --reference REF.txt --estimate SALIDA.json --mode b1 --output b1.json
```

## Regla de decisión
No se modifica el algoritmo por el resultado de una sola pista. Los cambios se consideran únicamente después de observar patrones repetidos por estrato y controles de no regresión.

## Primeros casos públicos
- ASAP-001: Chopin, Ballade 1, `BuiJL04M` + `BuiJL04M_annotations.txt` + audio MAESTRO enlazado en `metadata.csv`.
- ASAP-002: Chopin, Ballade 2, `Gasanov08M` + `Gasanov08M_annotations.txt` + audio MAESTRO enlazado en `metadata.csv`.

Los audios no se redistribuyen en este repositorio.