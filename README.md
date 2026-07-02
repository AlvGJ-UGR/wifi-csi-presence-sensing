# 📡👻 Sensado de presencia mediante WiFi CSI (a través de paredes, sin cámara)

> Detección de presencia y movimiento humano usando Channel State Information (CSI) de WiFi sobre ESP32 — sin cámaras, sin micrófonos, sin sensores dedicados. Solo las distorsiones que el cuerpo humano provoca en las señales de radio que ya están en el aire.

Proyecto personal de investigación aplicada en sensado RF, dentro de mi portfolio de Ingeniería de Telecomunicaciones. Repositorio principal del portfolio: [Telecom-portfolio](https://github.com/AlvGJ-UGR/Telecom-portfolio).

---

## Tabla de contenidos

1. [Motivación](#motivación)
2. [Fundamento técnico: qué es CSI y por qué funciona](#fundamento-técnico-qué-es-csi-y-por-qué-funciona)
3. [Trabajo relacionado y diferenciación](#trabajo-relacionado-y-diferenciación)
4. [Arquitectura del sistema](#arquitectura-del-sistema)
5. [Hardware](#hardware)
6. [Metodología](#metodología)
7. [Roadmap y fases](#roadmap-y-fases)
8. [Cómo empezar](#cómo-empezar-para-retomar-el-proyecto)
9. [Estructura del repositorio](#estructura-del-repositorio)
10. [Limitaciones y consideraciones honestas](#limitaciones-y-consideraciones-honestas)
11. [Referencias y trabajo relacionado (enlaces)](#referencias-y-trabajo-relacionado-enlaces)
12. [Contacto](#contacto)
13. [Licencia](#licencia)

---

## Motivación

Todo router WiFi llena el espacio de ondas de radio constantemente. Cuando una persona se mueve, respira o simplemente está de pie en una habitación, perturba esas ondas de forma medible — igual que mover la mano delante de una linterna cambia la sombra proyectada. **Channel State Information (CSI)** es la información de bajo nivel de la capa física WiFi (amplitud y fase por subportadora OFDM) que captura exactamente esa perturbación, y el ESP32 puede extraerla de forma nativa desde su chip WiFi sin hardware adicional.

Este proyecto busca dos cosas a la vez: (1) un sistema de detección de presencia realmente útil (sustituto de PIR para domótica en zonas donde una cámara no es aceptable — baños, dormitorios), y (2) sobre todo, una demostración rigurosa y bien documentada de procesamiento de señal aplicado a un problema de sensado RF real, con metodología de evaluación cuantitativa — el tipo de trabajo que un ingeniero de RF/telecom hace en su día a día.

## Fundamento técnico: qué es CSI y por qué funciona

En WiFi 802.11n/ac (OFDM), la señal se transmite en decenas de subportadoras simultáneas. El receptor necesita estimar cómo el canal afecta a cada subportadora (atenuación y desfase) para poder demodular correctamente — esa estimación por subportadora *es* el CSI, y normalmente se descarta después de usarla para ecualizar la señal. El ESP32 permite acceder a esos valores en crudo.

Cuando algo se mueve en el entorno (una persona, una puerta), cambia la trayectoria multicamino de la señal entre transmisor y receptor, lo que se traduce en variaciones medibles de amplitud y fase en un subconjunto de subportadoras a lo largo del tiempo. Presencia estática (alguien quieto) produce un patrón de CSI distinto pero también detectable (más sutil) que movimiento activo — esto es lo que hace que el problema sea interesante desde el punto de vista de procesamiento de señal: no es un simple detector de movimiento por umbral.

## Trabajo relacionado y diferenciación

Antes de empezar se hizo una revisión del ecosistema existente para evitar reinventar (mal) lo que ya existe, y para identificar honestamente en qué hueco se sitúa este proyecto:

| Proyecto | Qué es | Cómo se diferencia este proyecto |
|---|---|---|
| [`espressif/esp-csi`](https://github.com/espressif/esp-csi) | Framework oficial de Espressif, ejemplos de captura CSI y demos (RainMaker, detección de actividad) | Es la base/herramienta de referencia para la captura, no un proyecto de evaluación — este proyecto usa esp-csi como capa de captura, pero añade la parte de metodología de evaluación cuantitativa que el framework no incluye |
| [`francescopace/espectre`](https://github.com/francescopace/espectre) | Producto terminado para usuario final: detección de movimiento con integración directa a Home Assistant vía YAML, sin código | Es la herramienta "úsalo ya" para domótica — no publica métricas de precisión/recall cuantitativas ni el porqué de sus umbrales. Este proyecto es lo opuesto: no busca ser un producto plug-and-play, busca documentar y entender **por qué** funciona, con datos de validación propios |
| [`StevenMHernandez/ESP32-CSI-Tool`](https://github.com/StevenMHernandez/ESP32-CSI-Tool) | Toolkit académico de captura de CSI (activo/pasivo), sin pipeline de detección incluido | Resuelve solo la adquisición, deja todo el procesamiento y clasificación al usuario — este proyecto documenta esa parte que falta: extracción de características, detector estadístico y evaluación |
| Proyectos de pose estimation vía CSI (`WiFi DensePose` / `RuView`, basados en investigación académica) | Sistemas muy ambiciosos: pose de 17 puntos, ritmo cardíaco/respiratorio, todo vía CSI con redes neuronales grandes | Alcance deliberadamente mucho más modesto y honesto: presencia/movimiento binario o de baja dimensionalidad, con un pipeline explicable paso a paso, no una caja negra de deep learning. Preferible para un proyecto de portfolio individual: se puede explicar y defender cada decisión en una entrevista técnica |
| Papers de HAR (Human Activity Recognition) con CNN-BiLSTM-Attention u otros modelos complejos | Trabajo académico centrado en maximizar accuracy en datasets de investigación | Este proyecto prioriza la caracterización RF rigurosa (SNR vs distancia, comparación clásico vs. ML, coste computacional en el propio ESP32) por encima de perseguir el accuracy máximo — es un proyecto de **ingeniería de sistemas de sensado**, no de investigación en ML |

**Resumen de la diferenciación en una frase:** la mayoría de proyectos existentes son o bien herramientas de captura sin evaluación, o bien productos/demos sin metodología publicada, o bien investigación de ML muy compleja y difícil de replicar/defender individualmente. Este proyecto ocupa el hueco intermedio: **un pipeline completo, transparente y evaluado cuantitativamente**, con foco en la caracterización RF (igual que el resto de proyectos de este portfolio) más que en maximizar una métrica de ML.

## Arquitectura del sistema

```mermaid
flowchart LR
    subgraph M1["Modo A: router existente (mínimo hardware)"]
        R1[Router WiFi<br/>ya existente] -.señal 2.4GHz.-> A1[ESP32 único<br/>modo estación, hace ping al router]
    end
    subgraph M2["Modo B: dos ESP32 dedicados (más control, el elegido para empezar)"]
        A2[ESP32 AP<br/>dedicado] -.señal 2.4GHz.-> B2[ESP32 STA<br/>sniffer CSI]
    end
    A1 --> C[Pipeline Python<br/>analysis/]
    B2 --> C
    C --> D[Extracción de<br/>características]
    D --> E[Detector estadístico<br/>baseline]
    D --> F[Clasificador ligero<br/>ML, fase 2]
    E --> G[Evaluación cuantitativa<br/>precision/recall/latencia]
    F --> G
```

Los dos recuadros de arriba son **configuraciones alternativas**, no partes simultáneas del mismo sistema — se implementa primero el Modo B (control total sobre el tráfico, más fácil de depurar) y se documentará si el Modo A resulta viable como alternativa de menor coste de hardware.

Detalle de cada modo (se documentará cuál rinde mejor en la práctica):

- **Modo "router existente"**: un solo ESP32 en modo estación, haciendo ping al router y capturando el CSI de las respuestas — mínimo hardware, pero depende de la configuración del router.
- **Modo "dos ESP32"**: un ESP32 como AP dedicado + otro como estación, control total sobre el tráfico y el timing — más robusto para experimentación, y es el que ya encaja con el hardware que tengo disponible (2+ ESP32-WROOM).

## Hardware

| Elemento | Cantidad | Ya disponible |
|---|---|---|
| ESP32-WROOM | 2 (mínimo) | Sí |
| Router WiFi 2.4GHz (para modo alternativo) | 1 | Sí (doméstico) |
| Cable USB / fuente de alimentación | 2 | Sí |

Coste adicional: **0€** — este es el único proyecto del portfolio que no requiere ninguna compra, todo el hardware ya está disponible.

## Metodología

### 1. Protocolo de recolección de datos

- Escenarios controlados: habitación vacía (clase "ausente"), una persona quieta (clase "presente-estático"), una persona moviéndose (clase "presente-movimiento"), y opcionalmente varias personas.
- Variables a barrer sistemáticamente: distancia ESP32–router (1-8m), presencia de obstáculos (pared de tabique, pared de carga), posición de la persona en la habitación.
- Cada sesión se etiqueta con timestamp de inicio/fin y metadatos (distancia, entorno) — sin este etiquetado riguroso no se puede evaluar nada con seriedad después.

### 2. Extracción de características

- Amplitud y varianza por subportadora a lo largo de una ventana deslizante
- PCA para reducir dimensionalidad (decenas de subportadoras → pocas componentes principales, técnica estándar en la literatura de CSI sensing)
- Energía de la señal en banda de movimiento (baja frecuencia, típicamente <5Hz tras el PCA) vía STFT/varianza en ventana

### 3. Detector baseline (clásico, explicable)

Umbral adaptativo sobre la varianza de las componentes principales — simple, interpretable, y sirve de referencia para saber si un modelo de ML más complejo realmente aporta algo (evitar la trampa de "usar deep learning porque sí").

### 4. Clasificador ligero (fase 2)

Comparar el baseline contra un clasificador simple (SVM lineal o kNN sobre las características extraídas) evaluando el trade-off precisión vs. coste computacional — con el objetivo de que pueda correr en el propio ESP32 si el resultado lo justifica, no asumido de antemano.

### 5. Evaluación

- Matriz de confusión, precisión, recall, F1 por clase
- Curva ROC para el detector baseline (variando el umbral)
- Latencia de detección (tiempo desde que ocurre el evento hasta que se clasifica)
- Degradación de accuracy vs. distancia y vs. tipo de pared — este es el resultado más parecido en espíritu al resto del portfolio (caracterización RF con datos, no solo "funciona/no funciona")

### Métricas objetivo (punto de partida, no una promesa)

Para tener un criterio de éxito concreto en vez de solo "que funcione", estos son los objetivos iniciales de la Fase 3-4. Son estimaciones razonables basadas en lo reportado por proyectos similares (ver tabla de diferenciación), **no resultados garantizados** — la primera tarea real de la Fase 3 es comprobar si son alcanzables con mi entorno y hardware concretos, y corregir estos números con datos reales en cuanto existan:

| Métrica | Objetivo inicial | Se revisará tras |
|---|---|---|
| Recall (detección de presencia, <4m, sin obstáculos) | >90% | Fase 3 |
| Falsos positivos (habitación vacía, 1h) | <5% | Fase 3 |
| Latencia de detección | <2s | Fase 3 |
| Recall a través de pared de tabique | Desconocido — es una pregunta de investigación de la Fase 5, no una asunción | Fase 5 |

## Roadmap y fases

- [ ] **Fase 1 — Prueba de concepto de adquisición**: flashear `esp-csi` en un ESP32, confirmar que se puede capturar y guardar CSI crudo en ambas configuraciones (router existente / dos ESP32)
- [ ] **Fase 2 — Recolección de dataset propio**: ejecutar el protocolo de la sección de metodología, generar un dataset etiquetado propio (no usar solo datasets públicos, para poder caracterizar mi propio entorno real)
- [ ] **Fase 3 — Detector baseline + evaluación**: implementar el detector por varianza/umbral, generar matriz de confusión y curva ROC
- [ ] **Fase 4 — Clasificador ligero + comparación**: entrenar y evaluar SVM/kNN, comparar contra el baseline en accuracy, latencia y viabilidad de correr en el ESP32
- [ ] **Fase 5 — Caracterización sistemática**: barrido de distancia/pared/nº de personas, gráficas de degradación de accuracy
- [ ] **Fase 6 (opcional)** — Dashboard en tiempo real y/o integración con Home Assistant, una vez validado el pipeline

## Cómo empezar (para retomar el proyecto)

1. Flashear el firmware base de `esp-csi` en un ESP32 (Fase 1) — de momento no hay firmware propio en `firmware/`, se parte del ejemplo oficial de Espressif y se adapta según haga falta.
2. Confirmar captura de CSI crudo por serie, guardar unas muestras de prueba en `data/raw/` con el formato de sesión descrito en "Protocolo de recolección de datos".
3. Escribir el primer script de `analysis/` que simplemente cargue esas muestras y grafique amplitud por subportadora en el tiempo — antes de cualquier detector, hay que *ver* la señal primero.
4. A partir de ahí, seguir el roadmap de fases en orden; no saltar a clasificadores (Fase 4) sin tener el baseline (Fase 3) evaluado, o no habrá con qué comparar si el modelo complejo realmente aporta algo.

## Estructura del repositorio

```
wifi-csi-presence-sensing/
├── README.md                 (este documento)
├── firmware/                 firmware ESP32 (basado en esp-csi) para captura de CSI
├── analysis/                 pipeline Python: extracción de características, detector, ML, evaluación
├── data/
│   ├── raw/                  capturas CSI crudas, etiquetadas por sesión
│   └── labeled/               datasets procesados listos para entrenar/evaluar
├── docs/                     notas técnicas, protocolo de recolección, decisiones de diseño
└── results/                  gráficas y métricas de evaluación (matrices de confusión, ROC, etc.)
```

## Limitaciones y consideraciones honestas

- **No es identificación de personas**, solo presencia/movimiento — cualquier extensión hacia biometría CSI plantea consideraciones de privacidad que están fuera del alcance de este proyecto.
- **Requiere recalibración por entorno**: un modelo entrenado en una habitación no se espera que generalice directamente a otra sin reajuste — se documentará explícitamente si esto ocurre en la fase de evaluación, en vez de asumir que no.
- **Consumo energético**: la captura continua de CSI requiere el radio WiFi activo permanentemente, a diferencia de sensores PIR que duermen la mayor parte del tiempo — no es apta para nodos de batería de larga duración sin trabajo adicional de gestión de energía.
- **Multi-persona**: distinguir cuántas personas hay (no solo si hay alguna) es sustancialmente más difícil y se deja fuera del alcance inicial (posible extensión futura).

## Referencias y trabajo relacionado (enlaces)

- Espressif — [esp-csi](https://github.com/espressif/esp-csi) (framework y ejemplos oficiales)
- Francesco Pace — [ESPectre](https://github.com/francescopace/espectre) (producto de detección de movimiento con integración Home Assistant)
- Steven M. Hernandez — [ESP32-CSI-Tool](https://github.com/StevenMHernandez/ESP32-CSI-Tool) (toolkit de captura académico)
- [Wi-ESP / Wi-SafeHome y colección de papers relacionados](https://wrlab.github.io/Wi-ESP/) (grupo de investigación, revisión de literatura de CSI sensing)
- ruvnet — [RuView / WiFi DensePose](https://github.com/ruvnet/RuView) (sistema avanzado de pose estimation vía CSI, referencia de hasta dónde puede llegar la técnica)

## Contacto

- LinkedIn: [tu perfil aquí]
- Email: [tu-email@ejemplo.com]
- Repositorio principal del portfolio: [Telecom-portfolio](https://github.com/AlvGJ-UGR/Telecom-portfolio)

## Licencia

MIT — ver [`LICENSE`](LICENSE).

---

**Estado general del proyecto:** 🔵 Fase de diseño completada, pendiente de iniciar Fase 1 (prueba de concepto de adquisición).
