# MASTER_PLAN.md

# WiFi CSI Presence Sensing
## Research Master Plan

---

# Project Objective

Develop a professional RF sensing system capable of detecting human presence using WiFi Channel State Information (CSI) acquired with ESP32 devices.

The objective is **not** simply to obtain a working detector.

The objective is to:

- understand the underlying RF phenomena,
- characterise system behaviour,
- compare multiple detection approaches,
- validate results experimentally,
- document the complete engineering process.

The repository should represent the work quality expected from a Telecommunications Engineer.

---

# Project Principles

Throughout the project:

- Scientific methodology always takes priority over implementation speed.
- Reproducibility is mandatory.
- Every important decision must be justified.
- Every experiment must answer a technical question.
- Every result must be supported by data.

---

# Global Workflow

The project follows the following engineering pipeline:

Literature Review

↓

System Design

↓

Hardware Validation

↓

Raw Data Acquisition

↓

Signal Characterisation

↓

Feature Engineering

↓

Baseline Detector

↓

Machine Learning

↓

Experimental Evaluation

↓

System Characterisation

↓

Documentation

No stage should be skipped.

---

# Phase 0 — Repository Preparation

## Objective

Prepare the repository structure and validate the project architecture.

---

Tasks

- Repository organisation
- Documentation
- Folder structure
- Development workflow
- Hardware inventory
- Architecture validation

Deliverables

- Repository ready
- README complete
- CLAUDE documentation
- Folder structure

Completion Criteria

Repository can be used to begin experimentation immediately.

Status

Completed.

---

# Phase 1 — CSI Acquisition

## Objective

Demonstrate that CSI can be reliably captured.

This phase is exclusively about acquisition.

No processing.

No Machine Learning.

No detection.

---

Tasks

Flash ESP32 with Espressif esp-csi.

Validate serial output.

Capture CSI packets.

Store raw sessions.

Define storage format.

Organise datasets.

Document hardware configuration.

---

Deliverables

Raw CSI files

Hardware documentation

Acquisition procedure

Initial plots

---

Completion Criteria

Reliable CSI acquisition.

Repeatable capture sessions.

No packet corruption.

---

# Phase 2 — Signal Characterisation

## Objective

Understand the signal before designing detectors.

---

Tasks

Visualise CSI.

Study amplitude.

Study phase.

Study packet rate.

Estimate noise.

Estimate stability.

Detect outliers.

Compare static vs movement.

Compare environments.

---

Deliverables

Signal plots

Noise analysis

Initial observations

Documentation

---

Completion Criteria

Clear understanding of signal behaviour.

Known limitations.

---

# Phase 3 — Dataset Generation

## Objective

Build a reproducible labelled dataset.

---

Tasks

Design acquisition protocol.

Define labels.

Collect sessions.

Document metadata.

Store timestamps.

Validate labels.

Generate processed dataset.

---

Dataset Variables

Distance

Orientation

Environment

Wall type

Human state

Timestamp

ESP32 configuration

Packet rate

---

Deliverables

Raw dataset

Processed dataset

Collection protocol

Metadata documentation

---

Completion Criteria

Dataset sufficiently representative.

Dataset reproducible.

---

# Phase 4 — Classical Detection

## Objective

Develop an interpretable baseline detector.

---

Candidate Methods

Variance

Moving variance

Adaptive threshold

PCA

Energy estimation

Sliding window statistics

---

Evaluation

Precision

Recall

F1

ROC

AUC

Latency

False positives

False negatives

---

Deliverables

Baseline detector

Evaluation report

Confusion matrix

ROC curves

---

Completion Criteria

Working detector.

Performance fully documented.

---

# Phase 5 — Feature Engineering

## Objective

Extract meaningful information from CSI.

---

Candidate Features

Amplitude variance

Subcarrier variance

PCA

Temporal energy

STFT

Moving statistics

Correlation

Entropy

---

Deliverables

Feature extraction library

Feature comparison

Documentation

---

Completion Criteria

Feature set justified.

---

# Phase 6 — Machine Learning

## Objective

Determine whether ML provides measurable improvements.

---

Candidate Models

Linear SVM

kNN

Random Forest

Lightweight Neural Network (only if justified)

---

Every model must be compared against:

Baseline detector.

---

Evaluation

Accuracy

Precision

Recall

F1

ROC

Latency

Memory

CPU cost

Inference time

---

Completion Criteria

Quantitative comparison completed.

Best model selected.

---

# Phase 7 — RF Characterisation

## Objective

Understand system limitations.

---

Variables

Distance

Wall type

Multiple people

Furniture

Orientation

Packet rate

ESP32 placement

Environmental changes

---

Deliverables

Accuracy degradation plots

Sensitivity analysis

Limitations

Engineering conclusions

---

Completion Criteria

System operating limits documented.

---

# Phase 8 — Integration

## Objective

Build a complete demonstrator.

Possible targets

Home Assistant

Dashboard

MQTT

REST API

Desktop visualiser

---

Completion Criteria

Complete working system.

---

# Phase 9 — Final Documentation

## Objective

Produce professional engineering documentation.

---

Deliverables

Architecture diagrams

Pipeline diagrams

Experimental methodology

Results

Discussion

Limitations

Future work

---

Completion Criteria

Repository suitable for publication.

---

# Project Priorities

Always prioritise:

1. Scientific validity
2. Correct measurements
3. Documentation
4. Signal understanding
5. Robust implementation
6. Performance optimisation
7. Additional features

---

# Risks

Possible risks include:

Low CSI stability

ESP32 firmware limitations

Environmental variability

Router incompatibility

Dataset bias

Poor generalisation

Hardware failures

Every identified risk must be documented.

---

# Future Extensions

Possible future work:

Breathing detection

Occupancy estimation

Multiple-person detection

TinyML deployment

Cross-room evaluation

5 GHz evaluation

MIMO evaluation

CSI fingerprinting

Respiration monitoring

Radar comparison

These extensions are optional.

They must never delay completion of the core project.

---

# Definition of Project Completion

The project is complete when:

✓ Reliable CSI acquisition exists

✓ Dataset collected

✓ Baseline detector implemented

✓ ML comparison completed

✓ Experimental validation completed

✓ RF characterisation completed

✓ Documentation complete

✓ Repository suitable for technical interviews
