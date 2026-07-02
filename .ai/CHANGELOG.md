# CHANGELOG.md

# WiFi CSI Presence Sensing
## Development Log

---

# Purpose

This document records completed development sessions.

Its purpose is to provide short-term project memory between Claude sessions.

It is **not** a Git commit history.

It is **not** a technical report.

Only concise summaries of completed work belong here.

Detailed architectural decisions must be stored in:

DECISIONS.md

Current project status must be stored in:

PROJECT_STATE.md

---

# Entry Template

---

## YYYY-MM-DD

### Objective

Brief description of the intended task.

### Completed

- Item
- Item
- Item

### Files Modified

- file1
- file2

### Files Created

- file3
- file4

### Notes

Important observations.

Problems encountered.

Unexpected behaviour.

Anything useful for future sessions.

### Next Recommended Task

Describe the logical next engineering task.

---

# Session History

---

## 2026-07-02

### Objective

Initial repository design and project planning.

### Completed

- Repository architecture designed.
- README completed.
- Scientific methodology defined.
- Development workflow established.
- AI documentation created.

### Files Modified

- README.md

### Files Created

- .ai/CLAUDE.md
- .ai/MASTER_PLAN.md
- .ai/PROJECT_STATE.md
- .ai/DECISIONS.md
- .ai/CHANGELOG.md

### Notes

The repository architecture has been frozen.

No firmware has been developed yet.

No datasets exist yet.

No experiments have been performed.

Project is ready to begin hardware validation.

### Next Recommended Task

Begin Phase 1.

Flash Espressif's official esp-csi firmware and validate stable CSI acquisition.

---

## 2026-07-02 (session 2)

### Objective

Prepare the repository for the first physical CSI acquisition session (Phase 1), and clean up outstanding repo hygiene issues.

### Completed

- Resolved unmerged Git conflict markers left in README.md and LICENSE from prior branches.
- Merged the two divergent architecture-diagram versions in the README into a single Modo A / Modo B mermaid diagram.
- Wrote firmware/README.md: steps to clone esp-csi, flash Modo B (priority) and Modo A (secondary), and Phase 1 exit criteria.
- Wrote docs/acquisition_protocol.md: raw session naming convention, required metadata.json schema, raw CSV format, labelling discipline, immutability rule.
- Updated PROJECT_STATE.md to reflect Phase 1 in-progress status and the hardware-dependent next task.

### Files Modified

- README.md
- LICENSE
- .ai/PROJECT_STATE.md

### Files Created

- firmware/README.md
- docs/acquisition_protocol.md

### Notes

No physical hardware capture was performed in this session — flashing firmware and capturing CSI requires hands-on access to the ESP32 boards, which is outside what a documentation session can perform. Scope was strictly the documentation/infrastructure needed so the next hands-on session can proceed without design decisions pending.

The README and LICENSE merge conflicts were a real defect, not cosmetic — as committed, GitHub would have rendered raw conflict markers instead of the intended content. Worth checking other files for the same issue before the next push.

### Next Recommended Task

Physical session: flash Modo B firmware, validate serial CSI output, capture the first three labelled raw sessions per docs/acquisition_protocol.md. Only after that should analysis/ gain its first script (load + plot amplitude vs. time, no detection logic yet, per ADR-003).

---

## 2026-07-02 (session 3)

### Objective

Continue Phase 1 preparation to the point where no further documentation-only work remains, per session-start protocol (PROJECT_STATE.md read first; no architectural decision needed, so DECISIONS.md and MASTER_PLAN.md were not re-read this session).

### Completed

- Wrote docs/hardware_configuration.md: template for board/router/channel-specific configuration (deliberately left as TBD pending the physical session, not guessed) plus a pre-flight checklist sequencing flash → associate → verify-CSI-stream → test-capture before any labelled session is recorded.
- Confirmed this closes out every Phase 1 deliverable that does not require physical hardware access.

### Files Modified

- .ai/PROJECT_STATE.md

### Files Created

- docs/hardware_configuration.md

### Notes

Stopped here deliberately. Every remaining Phase 1 task (flashing, serial validation, labelled capture) requires physical access to the ESP32 boards, which meets the explicit "hardware validation is impossible" exception for pausing rather than improvising further. Did not write analysis/ scripts or fabricate any capture data — both are explicitly out of scope until real raw sessions exist (ADR-003, ADR-005, and the standing note in PROJECT_STATE.md).

### Next Recommended Task

Hands-on session: run the docs/hardware_configuration.md pre-flight checklist, flash Modo B, fill in the hardware config fields with real values, then capture the first three labelled raw sessions per docs/acquisition_protocol.md.

---

# Maintenance Rules

Keep this document concise.

One entry per completed work session.

Avoid implementation details.

Avoid large code descriptions.

Do not duplicate information already stored in:

- PROJECT_STATE.md
- DECISIONS.md

If a session produces no meaningful progress, do not create a new entry.

---

# Completion Checklist

Before closing a work session, ensure:

✓ Code committed (if applicable)

✓ Documentation updated

✓ PROJECT_STATE.md updated

✓ CHANGELOG.md updated

✓ Any architectural decision recorded in DECISIONS.md

✓ Next recommended task identified

---

# Maximum Length

This document should remain compact.

If it grows beyond approximately 150–200 entries, archive older entries into:

docs/archive/CHANGELOG_2026.md

docs/archive/CHANGELOG_2027.md

etc.

The active CHANGELOG.md should always contain recent development history only.
