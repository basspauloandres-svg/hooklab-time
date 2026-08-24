# HookLab × DeepSeek Harness — Piloto v0.1

Estado: EXPERIMENTAL / NO OPERATIVO
Fecha: 2026-08-24

## Decisión

DeepSeek Harness no sustituye el runtime actual de HookLab TIME ni entra en la ruta de audio. Se evalúa como capa externa de orquestación, persistencia y trazabilidad.

## Razón

El proyecto necesita separar dos problemas:

1. estabilidad del motor TIME/audio en iPhone;
2. persistencia y trazabilidad del laboratorio entre sesiones, modelos y herramientas.

Harness solo se evalúa para el segundo problema. El baseline de audio seguirá siendo independiente.

## Principio de aislamiento

HookLab Core debe poder funcionar sin Harness.

Harness debe poder eliminarse sin modificar:
- algoritmos TIME;
- CTL;
- archivos HTML de prueba;
- formatos JSON de evidencia;
- corpus;
- reglas metodológicas;
- resultados auditivos.

## Arquitectura piloto

Usuario / investigador
        |
        v
DeepSeek Harness (orquestación experimental)
        |
        +-- session log append-only
        +-- estado experimental HookLab
        +-- selección de herramientas/modelos
        +-- ejecución/reanudación/fork
        |
        v
HookLab Adapter (futuro plugin o SDK bridge)
        |
        +-- leer manifiesto de experimento
        +-- ejecutar herramienta determinista
        +-- recoger artefactos
        +-- registrar hashes/versiones
        |
        v
HookLab Core / GitHub / artefactos

## Unidad mínima de estado experimental

Cada ejecución futura deberá poder representar:

- experiment_id
- timestamp
- device_target
- browser_target
- baseline_version
- commit_sha
- hypothesis
- independent_variable
- controlled_variables
- input_artifacts
- tool_or_engine
- model_if_any
- output_artifacts
- human_auditory_observation
- machine_observation
- decision
- next_experiment

## Primera prueba de valor

Harness se considerará útil para HookLab solo si un piloto demuestra que puede:

1. iniciar una sesión experimental;
2. registrar el baseline y commit exactos;
3. ejecutar o invocar una prueba sin alterar el Core;
4. registrar entradas y salidas;
5. reanudar la sesión sin reconstruir el estado desde un chat;
6. bifurcar una hipótesis conservando el linaje;
7. reconstruir posteriormente qué decisión produjo una versión concreta.

## Criterios de aceptación

- Cero cambios en la ruta de audio por instalar Harness.
- Cero dependencia metodológica de DeepSeek o de un modelo particular.
- Estado experimental recuperable después de cerrar la conversación.
- Linaje baseline -> experimento -> evidencia -> decisión verificable.
- Posibilidad de cambiar de modelo sin cambiar el protocolo experimental.
- Exportación o persistencia legible fuera de Harness.

## Criterios de rechazo

El piloto se detiene si:

- obliga a migrar HookLab Core;
- introduce una segunda fuente de verdad para versiones;
- modifica los HTML de audio para funcionar;
- dificulta reproducir un experimento sin Harness;
- sus cambios de API rompen repetidamente la trazabilidad;
- aumenta la complejidad sin reducir pérdida de contexto o trabajo manual.

## Alcance inicial

No desarrollar todavía un plugin TIME completo.

Orden propuesto:

P1. Congelar esquema de estado experimental.
P2. Instalar Harness en un entorno de desarrollo separado del iPhone.
P3. Crear una sesión de laboratorio de prueba sin audio.
P4. Conectar lectura del repositorio HookLab y artefactos JSON.
P5. Probar resume/fork/replay sobre un experimento ya cerrado.
P6. Solo si P1-P5 aportan valor, diseñar `hooklab-time` como plugin/bridge.

## Relación con el problema actual de audio

El diagnóstico de audio continúa por separado. La evidencia vigente indica:

- HTMLAudioElement nativo: audible en iPhone.
- Web Audio en las pruebas recientes: ejecución interna registrada, salida inaudible.
- v1.9.29 documentó la arquitectura de reloj común y A/B de compensación; la solución conceptual buscada mantiene un solo reloj audible y offset 0 ms.

Harness no se utilizará para corregir este fallo de audio.

## Estado de decisión

APROBADO PARA PILOTO AISLADO.
NO APROBADO PARA MIGRACIÓN DEL CORE.
