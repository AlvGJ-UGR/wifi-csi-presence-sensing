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
