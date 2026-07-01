# DECISIONS.md

# Architecture Decision Records (ADR)

This document records permanent technical decisions made during the project.

Its purpose is to:

- avoid reopening previously resolved discussions;
- maintain architectural consistency;
- document engineering rationale;
- preserve project knowledge between Claude sessions.

Only long-term architectural decisions belong here.

Implementation details, temporary notes or work logs must NOT be recorded here.

---

# ADR-001

## Title

Use Espressif's official esp-csi framework for CSI acquisition.

## Status

Accepted

## Context

The ESP32 firmware required to capture CSI can either be developed from scratch or built upon Espressif's official implementation.

The official framework is maintained by Espressif, widely used in the community and continuously updated.

## Decision

The project will use the official esp-csi framework as the acquisition layer.

Custom firmware will only be developed when strictly necessary.

## Rationale

Advantages:

- Official support.
- Better long-term maintenance.
- Reduced firmware complexity.
- Easier reproducibility.
- Better compatibility with future ESP-IDF releases.

## Alternatives Considered

Develop a custom CSI acquisition firmware.

Rejected because:

- unnecessary complexity;
- higher maintenance cost;
- no clear engineering benefit.

## Consequences

The project focuses on signal processing rather than firmware development.

---

# ADR-002

## Title

Use two ESP32 devices as the primary experimental platform.

## Status

Accepted

## Context

Two acquisition architectures are possible:

A.

Existing WiFi router.

B.

Dedicated ESP32 Access Point + ESP32 Station.

## Decision

The primary experimental platform will use two dedicated ESP32 boards.

Router-based experiments remain optional.

## Rationale

Advantages:

- full traffic control;
- deterministic packet generation;
- easier debugging;
- repeatable experiments;
- fewer external variables.

## Alternatives Considered

Single ESP32 + existing router.

Useful as a future validation scenario, but not as the main research platform.

## Consequences

All early experiments should assume the dual-ESP32 configuration.

---

# ADR-003

## Title

Signal understanding before Machine Learning.

## Status

Accepted

## Context

Many CSI projects immediately apply neural networks without understanding the underlying signal behaviour.

This often produces difficult-to-interpret results.

## Decision

The project will first characterise the CSI signal before implementing any classifier.

## Rationale

Priority order:

Signal

↓

Features

↓

Baseline

↓

Machine Learning

## Alternatives Considered

Deep Learning from the beginning.

Rejected because:

- poor explainability;
- unnecessary complexity;
- difficult to justify during technical interviews.

## Consequences

Machine Learning is postponed until signal behaviour is well understood.

---

# ADR-004

## Title

Always implement a classical baseline detector.

## Status

Accepted

## Context

A Machine Learning model has little value unless compared against a simpler alternative.

## Decision

Every ML model must be quantitatively compared against a classical detector.

## Candidate Baselines

- Adaptive Threshold
- Variance Detector
- PCA-based Detector

## Consequences

Machine Learning is never evaluated in isolation.

---

# ADR-005

## Title

Maintain immutable raw datasets.

## Status

Accepted

## Context

Raw experimental data should never be modified.

## Decision

The acquisition pipeline shall always follow:

Raw

↓

Processed

↓

Features

↓

Results

## Consequences

Every published result must be reproducible from the original acquisition.

---

# ADR-006

## Title

Prioritise reproducibility over benchmark performance.

## Status

Accepted

## Context

Small improvements in accuracy often come at the expense of increased complexity and reduced reproducibility.

## Decision

The project prioritises:

- reproducibility;
- explainability;
- engineering quality;

over achieving the highest possible accuracy.

## Consequences

A simpler model with fully understood behaviour is preferred over a more complex model with marginally better performance.

---

# ADR-007

## Title

Evaluation must be experimental.

## Status

Accepted

## Context

Simulation and theoretical expectations are insufficient for validating an RF sensing system.

## Decision

System performance must always be evaluated using experimentally collected data.

## Required Metrics

- Precision
- Recall
- F1-score
- ROC
- AUC
- Latency
- False Positive Rate
- False Negative Rate

## Consequences

Claims regarding system performance require supporting experimental evidence.

---

# ADR-008

## Title

Scientific honesty over positive results.

## Status

Accepted

## Context

Negative or unexpected experimental outcomes are common in RF sensing research.

Suppressing or ignoring them reduces the engineering value of the project.

## Decision

Unexpected or negative results shall be documented rather than hidden.

## Consequences

Repository documentation reflects actual engineering work instead of only successful demonstrations.

---

# ADR-009

## Title

Literature review before introducing new algorithms.

## Status

Accepted

## Context

CSI sensing is an active research area with a large body of existing work.

## Decision

Before implementing any significant signal processing or Machine Learning algorithm, review the relevant literature and justify the selected approach.

## Consequences

The project remains aligned with current engineering practice and avoids unnecessary reinvention.

---

# Adding New ADRs

Create a new ADR only when:

- an architectural decision is made;
- changing it later would significantly affect the project;
- future work depends on it.

Do NOT create ADRs for:

- bug fixes;
- implementation details;
- formatting;
- temporary experiments;
- refactoring;
- session notes.

New ADRs should be appended to the end of this document and should never silently modify previous accepted decisions.
