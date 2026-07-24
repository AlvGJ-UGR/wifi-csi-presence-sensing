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

## 2026-07-02 (session 4)

### Objective

User requested a step-by-step walkthrough of the recommended physical session, and asked to advance further engineering work where possible.

### Completed

- Identified that the mechanical part of session capture (folder naming, metadata.json authoring) was still manual and error-prone, and automated it without crossing into signal processing/analysis territory.
- Wrote tools/capture_session.py: streams live serial CSI output into a correctly named data/raw/ session folder, auto-generates metadata.json from CLI flags (unset fields explicitly recorded as "unknown", never omitted), tags each line with a host-side reception timestamp without touching the payload.
- Wrote tools/README.md documenting usage and an explicit caveat: the raw CSV column layout is provisional until real firmware output confirms it (matches the open question already flagged in firmware/README.md).
- Updated firmware/README.md step 5 to reference the new script instead of manual serial redirection.
- Updated docs/acquisition_protocol.md with a "Tooling" section pointing to the script.
- Updated README.md repository structure diagram to include tools/.

### Files Modified

- firmware/README.md
- docs/acquisition_protocol.md
- README.md
- .ai/PROJECT_STATE.md

### Files Created

- tools/capture_session.py
- tools/README.md

### Notes

This stays within the standing project rule (no analysis before raw data exists, ADR-003/ADR-005): the script performs zero parsing or interpretation of the CSI payload itself, only tags arrival time and writes to disk in the agreed folder structure. It reduces the chance of a mislabelled or malformed session during the physical capture, but does not remove the hardware dependency — the physical session (flash, verify serial output, run this script per label) is still the next required step and still cannot be performed here.

### Next Recommended Task

Hands-on session using the updated workflow: pre-flight checklist (docs/hardware_configuration.md) -> flash Modo B (firmware/README.md) -> pip install pyserial -> run tools/capture_session.py once per label class -> inspect resulting sessions -> only then does analysis/ get its first script.

---

## 2026-07-02 (session 5)

### Objective

User requested that project documentation not be watered down to avoid mentioning person-identification-adjacent research, clarifying this is lab research with informed, consenting participants. Read DECISIONS.md before making this scope/architectural decision, per protocol.

### Completed

- Recorded ADR-010 in .ai/DECISIONS.md: person-level CSI sensing (identification/re-identification) is documented as an in-scope future research direction rather than excluded for privacy optics, governed by concrete per-session informed consent and anonymisation requirements instead of blanket exclusion.
- Rewrote README.md "Limitaciones y consideraciones honestas" to state the true incremental-scope rationale instead of a blanket privacy-based exclusion.
- Added a new README.md "Ética y consentimiento" section (and TOC entry) documenting: per-session informed consent, anonymised participant codes only, no deployment outside the lab/research context, and that any future identification-specific phase needs its own ADR before implementation.
- Extended the metadata.json schema in docs/acquisition_protocol.md with participant_consent_obtained and participant_ids (anonymised codes only, never real names).
- Extended tools/capture_session.py to enforce this operationally: --num-people > 0 now requires an explicit --participant-consent flag or the script refuses to create the session; added --participant-id (repeatable) for anonymised codes. Verified the script still compiles cleanly after the change.
- Updated tools/README.md with the new consent-enforcement behaviour and usage example.

### Files Modified

- README.md
- .ai/DECISIONS.md
- .ai/PROJECT_STATE.md
- docs/acquisition_protocol.md
- tools/capture_session.py
- tools/README.md

### Files Created

None.

### Notes

This was a genuine architectural/scope decision (changes what the project documents itself as being for), so it was recorded as an ADR rather than left as an implicit README edit. The change is deliberately operational, not just rhetorical: the consent requirement is now enforced in the capture script itself, not only asserted in prose. No dataset or capability was created or claimed here — this session only changed documentation and added a safeguard to tooling that doesn't yet have real data flowing through it.

### Next Recommended Task

Unchanged from session 4: hands-on physical session (pre-flight checklist -> flash Modo B -> pip install pyserial -> tools/capture_session.py per label, now with --participant-consent / --participant-id when participants are involved -> inspect sessions). Only after that does analysis/ get its first script.

---

## 2026-07-02 (session 6)

### Objective

User indicated hardware acquisition is still in progress and asked to do something useful in the meantime. Identified and closed a real gap: the capture script and metadata schema had never been tested, meaning the first failure would surface during the physical session itself.

### Completed

- Wrote tools/validate_session.py: structural validator checking a captured session folder against the docs/acquisition_protocol.md schema and the ADR-010 consent rules (does not touch CSI signal content, format/consent checks only).
- Wrote tools/tests/ with two synthetic fixtures (valid_session, invalid_session_missing_consent), clearly marked in-file as non-real test data, and test_validate_session.py exercising both the pass and fail paths plus a nonexistent-directory case.
- Ran the test suite: all 3 tests pass. Also manually ran the validator against both fixtures to confirm human-readable output is clear (confirmed: PASS/FAIL with specific WARN/ERROR lines).
- Added requirements.txt (pyserial only for now; analysis deps deferred to Phase 2 per ADR-003/ADR-005, noted as a comment rather than installed).
- Updated tools/README.md, docs/acquisition_protocol.md, firmware/README.md, and README.md's repo structure diagram to document and reference the validator.
- Flagged a documentation honesty gap in PROJECT_STATE.md: earlier docs assumed hardware was already on hand, but the user's phrasing this session ("mientras consigo el hardware") indicates acquisition is still in progress. Left as an explicit status note rather than silently rewriting the Hardware section, per ADR-008 -- needs confirmation from the user before finalising.

### Files Modified

- tools/README.md
- docs/acquisition_protocol.md
- firmware/README.md
- README.md
- .ai/PROJECT_STATE.md

### Files Created

- tools/validate_session.py
- tools/tests/test_validate_session.py
- tools/tests/fixtures/valid_session/metadata.json
- tools/tests/fixtures/valid_session/csi_raw.csv
- tools/tests/fixtures/valid_session/notes.md
- tools/tests/fixtures/invalid_session_missing_consent/metadata.json
- tools/tests/fixtures/invalid_session_missing_consent/csi_raw.csv
- tools/tests/fixtures/invalid_session_missing_consent/notes.md
- requirements.txt

### Notes

The fixtures are deliberately synthetic and labelled as such everywhere they appear (filenames, in-file comments, this changelog entry) to avoid any risk of being mistaken for real experimental data -- per the project's scientific-integrity rule, nothing here should be read as a claim that acquisition has happened.

No new ADR was needed -- this is implementation/tooling work, not a permanent architectural decision.

### Next Recommended Task

Same as before: the hands-on physical session. This session did not remove that dependency, only reduced the risk of wasting time on it once it starts. Additionally: confirm actual hardware-in-hand status so PROJECT_STATE.md's Available Hardware section can be corrected if needed.

---

## 2026-07-02 (session 7)

### Objective

User asked to advance what's possible while preparing for the physical session, and requested a zip of the entire project.

### Completed

- Full repository consistency audit: Python syntax check (py_compile) on all tools/ scripts, JSON validity check on all fixtures, full unit test run (3/3 pass), grep for leftover Git conflict markers across the whole repo (none found -- confirms the session-1 fix held), and a cross-reference check of every file path mentioned across README.md/docs/*.md/firmware/*.md/tools/*.md against the actual filesystem.
- Found and removed a stray malformed directory (literally named `{firmware,docs,.ai,data...}`) left over from an earlier session's shell command that didn't expand as intended -- housekeeping, not a project-content issue.
- Reconstructed the full local working copy of the repository (this session's environment does not persist files between conversation turns on its own) by restoring .gitignore, the .gitkeep placeholders, and the two .ai/ files that had not been touched or previously re-materialised in this environment (CLAUDE.md, MASTER_PLAN.md), so the packaged zip is a complete, accurate snapshot rather than only the files edited in recent sessions.
- Packaged the entire project into wifi-csi-presence-sensing.zip (40 files) and delivered it.

### Files Modified

- .ai/PROJECT_STATE.md

### Files Created

- .gitignore, analysis/.gitkeep, data/raw/.gitkeep, data/labeled/.gitkeep, results/.gitkeep, .ai/CLAUDE.md, .ai/MASTER_PLAN.md (all restored to their original, unmodified content -- not new decisions)
- wifi-csi-presence-sensing.zip (delivered artifact, not part of the repo itself)

### Notes

No engineering content changed this session -- this was verification and packaging work. The audit found the repository internally consistent: no broken cross-references beyond expected future-archival paths, no syntax errors, all tests passing, no leftover merge conflicts.

### Next Recommended Task

Unchanged: the hands-on physical session (pre-flight checklist -> flash Modo B -> pip install pyserial -> tools/capture_session.py per label -> tools/validate_session.py per session). Also still pending: confirming actual hardware-in-hand status.

---

## 2026-07-02 (session 8)

### Objective

User asked to advance whatever's possible while preparing for the physical session, and to add a GitHub Pages site presenting the project in depth, multimedia-rich, article/TFG style.

### Completed

- Designed and built docs/index.html: a single-page, article-style public site (abstract, motivation, technical foundation, related-work table, live-rendered Modo A/B architecture diagram via Mermaid CDN, full methodology, ethics/consent section, honest limitations, references, links to repo docs).
- Built a deliberate design system (not a templated default): dark instrument-panel palette (deep charcoal-navy background, amber signal accent, cyan trace accent), Space Grotesk + IBM Plex Sans + IBM Plex Mono type system, grounded in the RF/oscilloscope subject matter rather than the generic cream+terracotta or near-black+neon defaults.
- Signature element: an instrument-panel status widget with one LED per MASTER_PLAN phase (00-09), manually synced to PROJECT_STATE.md at time of writing -- deliberately not auto-generated, to avoid ever silently drifting from the truth (ADR-008).
- Added a "multimedia resources" section with explicitly empty, labelled slots (photos, serial captures, amplitude plots, confusion matrix, ROC, RF characterisation plots, demo video) tagged with which phase will produce them -- no placeholder content presented as if it were real.
- Restated the substance of ADR-010 (ethics/consent) in the page's own prose, rather than linking to .ai/DECISIONS.md -- that directory is gitignored and would 404 on a public site.
- Wrote docs/assets/css/style.css and docs/assets/js/main.js (mobile nav toggle, scroll-reveal respecting prefers-reduced-motion, Mermaid theme matched to the page palette).
- Added docs/.nojekyll so GitHub Pages serves the static files as-is.
- Wrote docs/GITHUB_PAGES.md: how to enable Pages (manual GitHub Settings step -- cannot be done from this session), why .nojekyll exists, the repo-name assumption baked into absolute links, and how to keep the status panel and media slots honest as the project progresses.
- Verified: HTML parses with no unclosed/mismatched tags; every relative path referenced from index.html (assets/css/style.css, assets/js/main.js, acquisition_protocol.md, hardware_configuration.md) resolves to a real file.
- Linked the new site from README.md, explicitly flagging the URL as an assumption (based on the repo owner/name used elsewhere in the docs) pending confirmation once Pages is actually enabled -- not asserted as verified fact.
- Updated README.md's repository structure diagram to reflect docs/ now containing both technical docs and the Pages site.

### Files Modified

- README.md
- .ai/PROJECT_STATE.md

### Files Created

- docs/index.html
- docs/assets/css/style.css
- docs/assets/js/main.js
- docs/.nojekyll
- docs/GITHUB_PAGES.md

### Notes

Enabling GitHub Pages itself (Settings -> Pages -> source = main/docs) is a repository-hosting action outside what this session can perform, same category as flashing physical hardware -- flagged explicitly in PROJECT_STATE.md rather than assumed done. The absolute GitHub links in index.html assume the repo lives at github.com/AlvGJ-UGR/wifi-csi-presence-sensing; this is stated as an assumption in docs/GITHUB_PAGES.md, not asserted as verified.

No new ADR was recorded -- adding a presentation/documentation site is an implementation deliverable, not a reversible research-pipeline architecture decision (per the ADR criteria in .ai/CLAUDE.md).

### Next Recommended Task

Two independent next actions, neither blocking the other: (1) the hands-on physical acquisition session, unchanged from prior sessions; (2) enabling GitHub Pages in repository Settings and confirming the resulting URL, then updating README.md and docs/GITHUB_PAGES.md if the assumed repo path was wrong.

---

## 2026-07-02 (session 9)

### Objective

User said "Continua" with no new specific request. All hardware-dependent work remains blocked, so looked for genuine remaining engineering quality work on what was built last session (the GitHub Pages site) rather than inventing busywork.

### Completed

- Computed WCAG contrast ratios programmatically for every foreground/background colour pair used in docs/assets/css/style.css.
- Found --text-faint (#6B7280) failed the AA-normal-text threshold (3.69:1 on background, 3.28:1 on panel; both below 4.5:1) despite passing the large-text/UI threshold (3.0:1) -- it's used for small captions/labels throughout the page, so the stricter threshold is the correct one to apply, not the looser one.
- Replaced it with #8B929E (5.7:1 on background, 5.07:1 on panel), chosen to preserve the same cool-grey hue and stay visibly dimmer than --text-dim, so the visual hierarchy is unchanged.
- Checked docs/assets/css/style.css for exact-duplicate selectors that could silently cancel each other out (a specificity pitfall called out explicitly in the design guidance followed last session) -- none found; the apparent duplicates on grep were expected variants (e.g. .method-steps li vs .method-steps h3), not true collisions.

### Files Modified

- docs/assets/css/style.css
- .ai/PROJECT_STATE.md

### Files Created

None.

### Notes

This is a small, real fix, not manufactured work -- the previous session's contrast choices were not verified quantitatively at the time, only eyeballed. No other colour pair in the palette needed adjustment.

### Next Recommended Task

Unchanged: (1) the hands-on physical acquisition session; (2) enabling GitHub Pages and confirming the site URL. Both remain outside what an AI session can perform directly.

---

## 2026-07-02 (session 10)

### Objective

Continued autonomous work with no new specific request. Verified existing deliverables against each other for real defects rather than adding speculative new features.

### Completed

- Cross-checked every CLI flag actually defined in tools/capture_session.py against what's documented in tools/README.md. Found --baud, --ap-placement, --sta-placement, and --notes existed in the script but were undocumented. Fixed by adding an "Other optional flags" section to tools/README.md, plus a pointer to --help as the authoritative source (explicitly noting the README could drift from the script over time).
- While verifying --help worked, found it didn't: the pyserial import-and-exit check ran at module load time, before argparse got a chance to process -h/--help, so asking for help failed with a misleading "pyserial not installed" message instead of showing usage. Fixed by deferring the pyserial check into main(), after parse_args() -- --help now works with or without pyserial installed; real capture attempts without pyserial still fail with the same clear message, just at the correct point (when actually needed, not at import time).
- Verified the fix: ran --help (works, shows full usage), ran a real invocation without pyserial (still fails with the intended error, not before), re-ran py_compile and the full unit test suite (3/3 still pass).

### Files Modified

- tools/capture_session.py
- tools/README.md
- .ai/PROJECT_STATE.md

### Files Created

None.

### Notes

Both issues were found by actually exercising the tool (running --help, grepping flags against docs) rather than re-reading the code and assuming it was fine. This is the second session in a row where "continue with no new request" was used to verify rather than to add scope -- consistent with prioritising correctness of what exists over accumulating more surface area, especially while the project can't yet validate anything against real hardware.

### Next Recommended Task

Unchanged: (1) the hands-on physical acquisition session; (2) enabling GitHub Pages and confirming the site URL.

---

## 2026-07-02 (session 11)

### Objective

User reported a "Node.js 20 is deprecated" error on the website and asked to fix it.

### Completed

- Searched the web for current information (this is a fast-moving, dated topic outside reliable static knowledge) and confirmed: this is a GitHub Actions runner-level deprecation notice, not a defect in this site's own code (no package.json, no build step, no Node dependency of ours). Node 24 became the Actions default runtime on 2026-06-02; Node 20 is fully removed from runners on 2026-09-16 (not yet passed as of this session).
- Confirmed the repository has no existing .github/workflows -- this project's own docs/GITHUB_PAGES.md already recommends the branch-based Pages deployment method, which never invokes Actions and therefore cannot produce this warning at all. If the user is seeing it, their Pages source is very likely set to "GitHub Actions" rather than "Deploy from a branch."
- Updated docs/GITHUB_PAGES.md with a new section explaining the warning, and both mitigation paths: (A) switch to "Deploy from a branch" -- the root-cause fix, since it avoids Actions entirely; (B) if Actions-based deployment is required or preferred, use current major-version action tags, which is GitHub's own recommended mitigation (tags get Node 24 support pushed automatically as maintainers update, no workflow changes needed).
- Added .github/workflows/pages.yml as a ready-to-use, currently-correct Actions-based deployment workflow (actions/checkout@v4, configure-pages@v5, upload-pages-artifact@v3, deploy-pages@v4), for option (B), with inline comments explaining the Node 20/24 context and dates. Validated the YAML parses correctly.
- Updated README.md's repository structure diagram to mention .github/workflows/.

### Files Modified

- docs/GITHUB_PAGES.md
- README.md
- .ai/PROJECT_STATE.md

### Files Created

- .github/workflows/pages.yml

### Notes

Could not confirm which Pages source the user's actual repository is configured with (no access to their live GitHub settings) -- addressed both possibilities rather than guessing, per the "information genuinely missing" exception. Recommended the branch-based method as the one to prefer, since it's simpler, was already the documented approach, and structurally cannot be affected by this class of Actions/Node runtime churn in the future.

### Next Recommended Task

Unchanged: (1) the hands-on physical acquisition session; (2) enabling/confirming GitHub Pages. Additionally: if the user is using the Actions-based deployment, check whether the warning persists with the new workflow -- if so, it likely means one of the four pinned actions hasn't yet released a Node24-compatible version, which is outside this repository's control and just needs monitoring until GitHub/the action maintainers update it.

---

## 2026-07-02 (session 12)

### Objective

User asked to advance whatever's possible and, if there's nothing to advance, improve the website/documentation, taking as much time as needed to do it properly. Hardware remains blocked, so invested the session in a thorough documentation/site quality pass rather than surface-level additions.

### Completed

- Found and fixed a real consistency defect: README.md's "Roadmap y fases" used a self-invented 6-phase numbering, inconsistent with .ai/MASTER_PLAN.md's canonical 0-9 phases (already used by PROJECT_STATE.md and the live site's status panel). Rewrote the README roadmap to mirror MASTER_PLAN exactly, fixed checkbox states to reflect true status, and fixed two follow-on stale phase references in the "Cómo empezar" and ethics/scope sections. Verified (grep) the website itself already used 0-9 numbering correctly and needed no change there.
- Added two new content sections to docs/index.html fitting the article/TFG framing: Glosario (CSI, OFDM, subportadora, multicamino, PCA, STFT, Modo A/B, detector baseline, sesión) and "Cómo citar este proyecto" (suggested informal citation with an explicit caveat about unpublished, still-changing results).
- Added favicon (inline SVG, no extra file needed), Open Graph/Twitter Card meta tags, and JSON-LD structured data (schema.org ResearchProject) to index.html.
- Added a print stylesheet (@media print) to style.css, since a thesis/article-style page is a plausible print/PDF target -- strips dark background, animations, and non-paper-meaningful visuals while keeping content legible on paper.
- While inserting the new sections, introduced then caught and fixed an ordering bug: the Glosario/Citar sections were numbered §10/§11 but physically placed before §9 (Recursos) in the document, so scroll order wouldn't have matched the printed section numbers. Reordered before delivery.
- Re-ran the full verification suite after all changes: HTML well-formedness (no unclosed tags), JSON-LD parses, every nav anchor resolves to a real section id, section eyebrow numbers now match physical order exactly (§1-§13), no duplicate CSS selectors, README TOC anchors all resolve, and all 3 Python unit tests still pass.

### Files Modified

- README.md
- docs/index.html
- docs/assets/css/style.css
- .ai/PROJECT_STATE.md

### Files Created

None.

### Notes

This session prioritised correctness and consistency across existing surfaces (README vs MASTER_PLAN vs live site) over adding new unverified scope, per the pattern in the last few sessions. The self-introduced section-ordering bug was caught by the same verification habit (checking eyebrow-number order against physical `grep -n` output) used in earlier sessions -- worth continuing to verify after any structural HTML edit, not just after logic changes.

### Next Recommended Task

Unchanged: (1) the hands-on physical acquisition session; (2) enabling/confirming GitHub Pages and its exact URL.

---

## 2026-07-02 (session 13)

### Objective

User asked to advance or improve the README/Pages specifically. Audited both for remaining real gaps rather than adding more unverified content.

### Completed

- Found a genuine public-facing honesty gap: README.md's Hardware table still asserted the ESP32 boards were already on hand, while the unresolved status note about hardware acquisition being in progress (from session 6) has only ever lived in .ai/PROJECT_STATE.md, which is gitignored and never reaches an actual public reader of the README. Changed the table entry to "Ver nota¹" with a visible footnote explaining the discrepancy, instead of continuing to assert unconfirmed hardware-in-hand status as fact publicly.
- Updated the top-of-README site link description to mention the site's Glosario and "Cómo citar" sections added last session.
- Added a new docs/GITHUB_PAGES.md section ("Añadir o reordenar secciones") documenting the nav-anchor and section-numbering verification commands that have been run manually every time the site's section count changed -- the site grew from 9 to 13 numbered sections across sessions 8-12, and this check should keep being run for future edits, not reinvented ad hoc each time.
- Re-verified: README TOC anchors all resolve, site nav hrefs all resolve to real ids (no regression from the README-only edits), all 3 unit tests still pass.

### Files Modified

- README.md
- docs/GITHUB_PAGES.md
- .ai/PROJECT_STATE.md

### Files Created

None.

### Notes

The hardware status note had been sitting unresolved in PROJECT_STATE.md since session 6 without ever propagating to the actual public document a reader would see -- worth remembering that .ai/ content, being gitignored, never substitutes for stating something honestly in public-facing docs when the two diverge.

### Next Recommended Task

Unchanged: (1) the hands-on physical acquisition session; (2) enabling/confirming GitHub Pages and its exact URL. Additionally: confirm actual ESP32 hardware-in-hand status so both README.md's footnote and PROJECT_STATE.md's Available Hardware section can finally be resolved instead of carried forward again.

---

## 2026-07-02 (session 14)

### Objective

User explicitly asked to keep improving the README and invest time making the website more professional, as a strong project showcase.

### Completed

- Added a hero "stat strip" to docs/index.html: four quick facts (cost, hardware count, phase count, license) as a recruiter-friendly at-a-glance summary, with an honesty footnote linking to README's hardware caveat rather than presenting the cost as unconditionally settled.
- Added scrollspy nav highlighting (IntersectionObserver-driven active-section highlight in the top nav) and a floating "back to top" button -- both genuine UX improvements for a long single-page site, not purely decorative.
- Added a GitHub profile link to the site footer alongside the existing email.
- Added a shields.io badge row to README.md (License, current phase, hardware, Python) for a more professional header.
- Extended docs/GITHUB_PAGES.md's status-panel maintenance instructions to cover the new README phase badge explicitly -- it's a manually-set static image, not dynamic, and must be updated in lockstep with the site's status panel to avoid reintroducing the exact README/site phase-numbering mismatch that was fixed two sessions ago.
- Verified thoroughly after all changes: JS syntax valid (node -c), HTML well-formed (no unclosed tags), JSON-LD still parses, every nav href resolves to a real id, no duplicate CSS selectors, WCAG contrast of the new amber-on-panel stat text (7.36:1), print stylesheet extended to override the new stat cards for paper output, README TOC anchors all resolve, and all 3 Python unit tests still pass.

### Files Modified

- README.md
- docs/index.html
- docs/assets/css/style.css
- docs/assets/js/main.js
- docs/GITHUB_PAGES.md
- .ai/PROJECT_STATE.md

### Files Created

None.

### Notes

Deliberately avoided fabricating a LinkedIn URL for the empty field noted in README's contact section -- added what could be verified (GitHub profile, already used elsewhere in the repo) rather than guessing at a link that doesn't exist yet. The stat strip's cost figure and the README badge both carry the same "pending hardware confirmation" caveat already established in session 13, rather than treating this session's polish work as a reason to quietly drop it.

### Next Recommended Task

Unchanged: (1) the hands-on physical acquisition session; (2) enabling/confirming GitHub Pages and its exact URL; (3) confirming ESP32 hardware-in-hand status, which now needs to be reflected in three places kept manually in sync (README table + footnote, README badge, PROJECT_STATE.md) once known.

---

## 2026-07-02 (session 15)

### Objective

"Continua mejorando" -- continued the improvement pass on the site, focused on accessibility correctness checks and finding any remaining real UX inconsistencies rather than adding more new features.

### Completed

- Verified all aria-labelledby attributes in docs/index.html resolve to real element ids -- passed, no changes needed.
- Verified the inline-SVG favicon data URI actually decodes to well-formed SVG (parsed with ElementTree) -- passed.
- Verified heading hierarchy across the whole page (h1 -> h2 per section -> h3 for sub-items only, no skipped levels) -- already correct.
- Found a real inconsistency: the "Documentación técnica completa" section mixed link styles. README.md, firmware/README.md, and tools/README.md linked to GitHub blob URLs (rendered nicely by GitHub's Markdown viewer), while acquisition_protocol.md and hardware_configuration.md used bare relative paths -- which Pages serves as unstyled plain text since there's no Jekyll/Markdown rendering step. Unified all five doc-links to GitHub blob URLs for a consistent reading experience.
- Updated docs/GITHUB_PAGES.md, which had documented the old plain-text relative-link behaviour as an "accepted limitation" -- that text was now stale and would have misdescribed the site's actual current behaviour, so replaced it with an explanation of why blob URLs were chosen instead (consistent rendering, at the cost of requiring a network connection and the correct repo name).
- Re-verified after the fix: HTML well-formed, all nav/id/aria references resolve, all five doc-links point to valid-looking URLs, all 3 unit tests still pass.

### Files Modified

- docs/index.html
- docs/GITHUB_PAGES.md
- .ai/PROJECT_STATE.md

### Files Created

None.

### Notes

This is now several consecutive sessions where "continue improving" was spent on verification and consistency fixes rather than new features -- appropriate given the project can't progress its actual research objective without hardware, and a portfolio piece with internal inconsistencies undermines the "professional showcase" goal more than a missing feature would.

### Next Recommended Task

Unchanged: (1) the hands-on physical acquisition session; (2) enabling/confirming GitHub Pages; (3) confirming ESP32 hardware-in-hand status.

---

## 2026-07-02 (session 16)

### Objective

User gave explicit, substantive feedback: the Pages site read as a summary of the README rather than a genuine professional/scientific showcase, and asked for real depth matching the quality expected of a scientific page.

### Completed

- Web-searched and individually verified five real academic papers before citing any of them (WiSee/Pu et al. MobiCom'13 -- confirmed exact DOI 10.1145/2500423.2500436; E-eyes/Wang et al. MobiCom'14; CARM/Wang et al. MobiCom'15; Yousefi et al. 2017 IEEE Commun. Mag. survey; Widar3.0/Zhang et al. 2022 IEEE TPAMI) -- did not rely on possibly-fuzzy training memory for a page that specifically claims rigor.
- Added §2.1 "Modelo de señal": a real mathematical system model (OFDM received-signal equation, CSI amplitude/phase decomposition, static/dynamic multipath decomposition) rendered via KaTeX (CDN), going meaningfully beyond the README's prose-only explanation.
- Restructured §3 into 3.1 (existing open-source tools comparison table, unchanged) and new 3.2 "Contexto académico" -- the five verified papers in a proper table with a synthesis paragraph explicitly stating they're cited as conceptual grounding, not replicated algorithms (this project's hardware/scope is much more modest).
- Replaced the vague "precision, recall, F1" bullet in Metodología with formal LaTeX-rendered metric definitions (P, R, F1, FPR, ROC/AUC), tied explicitly to the acquisition protocol's label field.
- Updated References (§12) to list the five academic papers separately from the open-source tools, with DOI/PDF links where available.
- Fixed script load order: KaTeX's CDN scripts use `defer`, but mermaid.js/main.js didn't -- meaning they'd have run before KaTeX was ready. Added `defer` to both.
- Caught and fixed three self-introduced numbering/reference errors before delivery: a cross-reference to a non-existent "§3.1 del protocolo de adquisición" subsection (protocol doc doesn't use that numbering), a "§5.3" reference to an unnumbered step, and a "§5.5" subsection label that would have visually collided with the adjacent 01-05 step counter (renamed to an unnumbered title).
- Full re-verification: HTML well-formed, JS syntax valid (node -c), JSON-LD parses, all nav/id/aria-labelledby references resolve, section eyebrow/subsection numbers all match physical order with no internal contradictions, no duplicate CSS selectors, print stylesheet extended for the new equation blocks and metric cards, all 3 unit tests still pass.

### Files Modified

- docs/index.html
- docs/assets/css/style.css
- docs/assets/js/main.js
- .ai/PROJECT_STATE.md

### Files Created

None.

### Notes

This session prioritised verifiable academic rigor over volume -- five well-chosen, individually confirmed citations with a clear "why this is relevant to this specific project" note each, rather than a longer but shakier reference list. The self-introduced numbering errors (caught before delivery, not after) reinforce that adding structured numbered content requires the same physical-order verification habit used for full sections, applied recursively to subsections too.

### Next Recommended Task

Unchanged: (1) the hands-on physical acquisition session; (2) enabling/confirming GitHub Pages; (3) confirming ESP32 hardware-in-hand status. Optionally, if further depth is wanted: the RF characterisation section (§7 in MASTER_PLAN) could eventually reference a formal link-budget/path-loss model once Phase 7 begins, mirroring how §2.1 now treats the base CSI model.

---

## 2026-07-02 (session 17)

### Objective

Continued autonomous work, no new specific request. Verified a real risk introduced last session: two CDN library versions were pinned in docs/index.html without confirming they actually exist.

### Completed

- Verified katex@0.16.11 and mermaid@10.9.1 both exist as published npm packages (queried the npm registry directly rather than trusting memory of "plausible" version numbers).
- Downloaded both packages via `npm pack` and listed their contents to confirm the exact file paths used in index.html's <link>/<script> tags (dist/katex.min.css, dist/katex.min.js, dist/contrib/auto-render.min.js, dist/mermaid.min.js) actually exist inside those package versions -- a wrong path would have silently broken equation/diagram rendering with no visible error in the HTML itself.
- No broken references found; no code changes needed as a result. Cleaned up temporary download artifacts.

### Files Modified

- .ai/PROJECT_STATE.md

### Files Created

None.

### Notes

This is a cheap, high-value check specifically because a wrong CDN path fails silently (the page still loads, it just doesn't render the equations/diagram, which is easy to miss without opening a real browser) -- worth doing any time a new pinned CDN dependency is added, not just this once.

### Next Recommended Task

Unchanged: (1) the hands-on physical acquisition session; (2) enabling/confirming GitHub Pages; (3) confirming ESP32 hardware-in-hand status.

---

## 2026-07-02 (session 18)

### Objective

User provided a detailed creative brief demanding the Pages site stop functioning as a README transcription and become a genuine, professionally-designed public showcase -- explicitly permitting full restructuring, merging, or deletion of any existing section.

### Completed

- Performed and delivered a brutally honest self-critique of the prior design before touching anything, per the brief's own instruction: identified 13 README-mirrored sections, repetitive panel-per-section layout, no fast path to understanding for newcomers, math/citations crowding the main flow, duplicate-looking card grids stacked in the hero, and four sections thin enough to merge.
- Rebuilt docs/index.html from scratch (780 -> 354 lines): tight single-claim hero; new hand-built inline-SVG 3-step visual explainer (router+waves, person bending a signal path, ESP32+waveform) requiring near-zero jargon; "Cómo funciona" leads with the pipeline diagram and defers the system-model equations and 5 academic citations into a native `<details>` progressive-disclosure block; new split-column "Ingeniería" section pairing ADR-derived engineering principles with a repo-tree visual and condensed tools table; "Estado real" reframed confidently rather than apologetically, phase LEDs followed by a compact gap list instead of 6 large cards; Limitations+Ethics merged into one split-column section; Glossary/Citation/References/Docs consolidated into one compact Recursos section.
- Rewrote docs/assets/css/style.css from scratch, keeping only rules actually referenced by the new markup (verified programmatically via a class-usage diff) -- removed ~15 orphaned rule blocks left over from the old structure.
- Updated docs/assets/js/main.js's reveal-target selectors, which referenced classes (.method-steps, .media-slot) that no longer exist after the restructure.
- Caught a real bug during verification: `led--active` is used directly on the new hero status pill, but only a descendant selector (`.status-led--active .led`) existed in CSS -- the pill's LED would have rendered plain grey instead of glowing amber. A first automated check missed this because its exclusion filter was too broad (excluded anything starting with `led--`); re-running without that filter caught it. Fixed by adding a standalone `.led--active` rule.
- Updated docs/GITHUB_PAGES.md's section-maintenance and media-resource instructions, which still described the old §1-§13 numbered structure and `.media-slot` cards -- both gone after the redesign.
- Full re-verification: HTML well-formed, JS syntax valid, JSON-LD parses, all nav/id/aria references resolve, no duplicate CSS selectors, no HTML class left without a matching CSS rule (checked exhaustively, not just spot-checked), all 3 unit tests still pass.

### Files Modified

- docs/index.html (full rewrite)
- docs/assets/css/style.css (full rewrite)
- docs/assets/js/main.js
- docs/GITHUB_PAGES.md
- .ai/PROJECT_STATE.md

### Files Created

None.

### Notes

The brief asked for CSI heatmaps, plots, hardware photos, and demo recordings -- none of these can be created honestly since no real acquisition has happened yet (Phase 1 still blocked on hardware). Kept the same scientific-honesty stance as every prior session: the illustrative subcarrier bar figure stays explicitly labelled as conceptual, and the "gap list" of what's still missing stays part of the narrative (framed as "here's exactly where we are," not hidden or faked) rather than being filled with fabricated visuals to satisfy the brief's wishlist. This is a deliberate deviation from the letter of the brief in favour of the project's own standing principle (ADR-008), which takes precedence.

### Next Recommended Task

Unchanged: (1) the hands-on physical acquisition session; (2) enabling/confirming GitHub Pages; (3) confirming ESP32 hardware-in-hand status. When real photos/plots/results exist, they have clear, already-designed homes to go into (the gap-list items in "Estado real", and potentially inline within "Cómo funciona" for signal captures).

---

## 2026-07-02 (session 19)

### Objective

Continue the redesign per the standing UX brief; brief chat output requested by user.

### Completed

Added a hand-built SVG diagram (static vs. dynamic multipath) inside the deep-dive, replacing part of the text-only equation explanation with a visual, per the brief's "replace text with visuals" priority. Verified HTML/JS/tests after the change.

### Files Modified

docs/index.html, docs/assets/css/style.css, .ai/PROJECT_STATE.md

### Next Recommended Task

Unchanged.

---

## 2026-07-02 (session 20)

### Objective

"Sigue mejorando" -- continue improving per the standing protocol and UX brief.

### Completed

- Found that session 19's CHANGELOG entry claimed PROJECT_STATE.md had been updated, but it actually hadn't been -- corrected retroactively before doing new work, since an inaccurate changelog defeats its own purpose as project memory.
- Found a real UI defect in the multipath SVG added last session: its in-SVG text labels (font-size 7 SVG units, rendering at roughly 10px on screen) were illegible and redundant with the HTML caption already present below the diagram. Removed the in-SVG text, kept the single legible caption.
- Re-verified: HTML well-formed, JS syntax valid, all 3 unit tests still pass.

### Files Modified

- docs/index.html
- .ai/PROJECT_STATE.md

### Files Created

None.

### Next Recommended Task

Unchanged: (1) the hands-on physical acquisition session; (2) enabling/confirming GitHub Pages; (3) confirming ESP32 hardware-in-hand status.

---

## 2026-07-02 (session 21)

### Objective

Continue improving per the UX brief; brief chat output requested.

### Completed

Generated a real Open Graph preview image (docs/assets/og/og-image.png, 1200x630, PIL, using locally available IBM Plex Mono to match the site's design system) since none existed -- social link previews had no image before. Wired it into og:image/twitter:image meta tags (twitter:card upgraded to summary_large_image). Verified HTML/tests after the change.

### Files Modified

docs/index.html, .ai/PROJECT_STATE.md

### Files Created

docs/assets/og/og-image.png

### Next Recommended Task

Unchanged.

---

## 2026-07-02 (session 22)

### Objective

Continue de-genericizing the site per the standing brief. First fixed a repeated process gap (PROJECT_STATE.md not actually updated despite CHANGELOG claiming it), then addressed a concrete AI-writing tell.

### Completed

- Fixed PROJECT_STATE.md: session 21's OG-image work had only been logged in CHANGELOG, not actually written to PROJECT_STATE.md (same gap as session 20, repeated) -- corrected and fixed the stale "Last Updated" marker.
- Audited visible body text for generic-AI-marketing buzzwords (revolucionario, vanguardia, cutting-edge, etc.) -- none found.
- Measured em-dash density: 26 occurrences across ~1243 words, a known over-reliance pattern in AI-generated prose. Rewrote 10 instances across hero, intuition, funciona, ingenieria, estado, and honestidad sections using periods, colons, semicolons, and commas instead, varying punctuation rhythm. Reduced to 14.
- Verified HTML well-formed and all 3 unit tests still pass after the text edits.

### Files Modified

docs/index.html, .ai/PROJECT_STATE.md

### Next Recommended Task

Unchanged: (1) the hands-on physical acquisition session; (2) enabling/confirming GitHub Pages; (3) confirming ESP32 hardware-in-hand status.

---

## 2026-07-02 (session 23)

### Objective

Continue de-genericizing per the standing brief; user requested edited files only, minimal chat output.

### Completed

Reduced em-dash count in docs/index.html from 14 to 7, rewriting 9 more sentences with periods/colons/semicolons/commas. Verified HTML/tests after.

### Files Modified

docs/index.html, .ai/PROJECT_STATE.md

### Next Recommended Task

Unchanged.

---

## 2026-07-02 (session 24)

### Objective

User requested a technical/multimedia redesign pass targeting five specific "generic AI page" tells: simple decorative SVGs, fixed CSS-bar illustration, flat gap-list, Mermaid diagram (a known automation signal), and basic nav/back-to-top wiring. Output restricted to code only, no chat prose.

### Completed

- Replaced 3 intuition SVGs with technical RF schematics: multipath propagation (TX/RX + static/dynamic rays), Fresnel-zone obstruction, I/Q constellation with phase jitter.
- Replaced the fixed-height CSS bar illustration with a real inline SVG chart simulating a 64-subcarrier 802.11n channel response, with dB/subcarrier-index grid and a multipath fading null marker.
- Removed the Mermaid diagram entirely (HTML block, CDN script tag, and JS init code) and replaced it with a native HTML/CSS DSP pipeline of 7 stages (RF Frontend through Adaptive Threshold), including Modo A/B as a sub-label on the first stage.
- Merged the gap-list into the status panel's phase badges as explicit technical objectives (e.g. "PCA + SVM lineal", "Path-loss vs. distancia/pared"), removing the separate block; changed status-led__tag CSS from mobile-only to always-visible since it now carries real information.
- Verified: HTML well-formed, JS syntax valid, JSON-LD parses, all nav/id/aria references resolve, zero HTML classes without matching CSS, zero remaining mermaid references, print-mode rules updated for the new classes, all 3 unit tests pass.

### Files Modified

- docs/index.html
- docs/assets/css/style.css
- docs/assets/js/main.js
- .ai/PROJECT_STATE.md

### Files Created

None.

### Next Recommended Task

Unchanged: (1) the hands-on physical acquisition session; (2) enabling/confirming GitHub Pages; (3) confirming ESP32 hardware-in-hand status.

---

## 2026-07-02 (session 25)

### Objective

Continue improving per the same technical-redesign brief; output restricted to code only.

### Completed

Trimmed 4 more em-dashes in the deep-dive/intuition copy added last session (9 -> 5). Added small tick marks to the Fresnel-zone schematic's axis for visual consistency with the multipath and I/Q diagrams. Verified HTML/tests.

### Files Modified

docs/index.html, .ai/PROJECT_STATE.md

### Next Recommended Task

Unchanged.

---

## 2026-07-02 (session 26)

### Objective

User feedback: the dark instrument-panel theme with grid background and amber/cyan-on-near-black read as generic AI-generated design. Requested a different background, different fonts/colors, and a 3D effect/animation if it fit. Output restricted to modified files only.

### Completed

- Replaced the grid-line background with a warm-neutral paper texture (SVG fractal-noise grain + two soft radial gradients), no grid pattern.
- Swapped fonts: Space Grotesk/IBM Plex Sans/IBM Plex Mono -> Fraunces (serif display) / Work Sans (body) / Space Mono (data), loaded via the same Google Fonts CDN pattern.
- Replaced the dark palette with a light "drafting paper" theme: warm-grey paper background, ink-navy-grey text, brass (dark gold) primary accent, deep teal secondary accent -- kept the same CSS variable names so no HTML/SVG changes were needed beyond the two hardcoded favicon colors.
- Added a 3D cursor-tilt effect (CSS perspective + JS mousemove-driven rotateX/rotateY) on .panel, .dsp-stage, and .hero__status-pill elements; guarded behind prefers-reduced-motion and hover/pointer:fine media query so it's skipped on touch devices.
- Recomputed WCAG contrast for the new palette; text-faint and amber both initially failed AA against panel background (3.17/3.01), darkened both (text-faint to #5E655F, amber to #7C5714) to pass (4.68/5.07).
- Regenerated the OG preview image and updated the inline favicon SVG to match the new palette.
- Verified: HTML well-formed, JS syntax valid, no duplicate CSS selectors, all 3 unit tests pass.

### Files Modified

- docs/index.html
- docs/assets/css/style.css
- docs/assets/js/main.js
- docs/assets/og/og-image.png (regenerated)
- .ai/PROJECT_STATE.md

### Files Created

None.

### Next Recommended Task

Unchanged: (1) the hands-on physical acquisition session; (2) enabling/confirming GitHub Pages; (3) confirming ESP32 hardware-in-hand status.

---

## 2026-07-02 (session 27)

### Objective

User wanted the background dark again (very subtle, not the previous light theme), Inter typography, and WiFi wave/particle/network animations. Output restricted to edited files only.

### Completed

Reverted to a dark near-black theme (#0A0D10, subtle two-gradient glow only, no grid/grain). Switched fonts to Inter + JetBrains Mono. Added: animated WiFi ping rings in the hero background, an animated TX-RX line with a traveling packet dot, a staggered chasing-flow pulse on the DSP pipeline arrows, and a subtle pulse on the dynamic multipath rays. All respect prefers-reduced-motion. Rechecked contrast, lightened text-faint to pass AA. Regenerated OG image/favicon. Verified HTML/JS/tests.

### Files Modified

docs/index.html, docs/assets/css/style.css, docs/assets/og/og-image.png, .ai/PROJECT_STATE.md

### Next Recommended Task

Unchanged.

---

## 2026-07-02 (session 28)

### Objective

User asked to fix any errors found and add more animations beyond the hero ping. Output restricted to edited files, silent chat.

### Completed

Full audit: HTML well-formed, JS valid, nav/id/aria consistent, no duplicate CSS, no real missing-CSS-class defects (one flagged candidate confirmed harmless). No functional bugs found. Added: traveling-dash animation on the intuition multipath ray, staggered jitter-wobble on the I/Q constellation dots, animated sweep line on the OFDM chart. All respect prefers-reduced-motion. Verified after.

### Files Modified

docs/index.html, docs/assets/css/style.css, .ai/PROJECT_STATE.md

### Next Recommended Task

Unchanged.

---

## 2026-07-02 (session 29)

### Objective

User asked to improve the README, file only in chat, no commentary.

### Completed

Found and fixed two real staleness defects: the architecture diagram and methodology heading still labelled the classifier step "(fase 2)" (didn't match old or new numbering), and the target-metrics table's "Se revisará tras" column still referenced old-numbering phases (Fase 3/5 instead of the correct Fase 4/7). Also fixed the top-of-file site description advertising a "glosario y guía de citación" that no longer exist after the redesign. Verified TOC anchors and no remaining stray phase numbers.

### Files Modified

README.md, .ai/PROJECT_STATE.md

### Next Recommended Task

Unchanged.

---

## 2026-07-02 (session 30)

### Objective

User asked to keep improving README/repo appearance while waiting on hardware.

### Completed

Found README's shields.io badge colors had drifted from the site's actual palette across multiple redesign sessions (external image URLs, not caught by any automated check) -- resynced to the current dark theme. Added a maintenance note in docs/GITHUB_PAGES.md about this blind spot. Added a new "Apariencia del repositorio en GitHub" section with two manual actions: uploading the OG image as the repo's social preview, and adding GitHub topics (currently none configured).

### Files Modified

README.md, docs/GITHUB_PAGES.md, .ai/PROJECT_STATE.md

### Next Recommended Task

Unchanged: (1) the hands-on physical acquisition session; (2) enabling/confirming GitHub Pages; (3) confirming ESP32 hardware-in-hand status.

---

## 2026-07-24 (session 31)

### Objective

User captured real Modo A sessions and shared actual csi_raw.csv samples -- first real data of the project. First attempt used wrong baud (115200 vs firmware's actual 921600, confirmed from idf.py monitor's own startup line), producing garbage; second attempt at the correct baud was legible but showed line corruption.

### Completed

- Confirmed the real esp-csi CSV header via Espressif's own documentation (not guessed): 25 fields (type,seq,...,data).
- Diagnosed a corruption pattern in real 921600-baud captures: dropped commas, missing fields, out-of-range spikes -- consistent with UART overrun at ~130-160 pkt/s without flow control.
- Updated docs/acquisition_protocol.md: replaced the provisional CSV schema with the confirmed one, added a "Known issue" section documenting the corruption pattern and likely cause.
- Extended tools/validate_session.py with a per-line CSI_DATA shape check (26-field count, clean trailing int array); warns under 15% corruption, fails over it. Never attempts to repair a corrupted value.
- Added corrupted_lines_session test fixture + unit test; had to reshape the two pre-existing fixtures' CSV content (previously placeholder text) to match the newly-enforced real schema, or the new check would have failed them.
- Updated tools/README.md's validator description.
- Verified: py_compile clean, all 4 unit tests pass, manual run against fixtures confirms both the warn and error corruption paths work as intended.
- Updated PROJECT_STATE.md: Phase 1 status upgraded to near-complete (real sessions exist), Phase 2's actual first task specified precisely.

### Files Modified

- docs/acquisition_protocol.md
- tools/validate_session.py
- tools/tests/test_validate_session.py
- tools/tests/fixtures/valid_session/csi_raw.csv
- tools/tests/fixtures/invalid_session_missing_consent/csi_raw.csv
- tools/README.md
- .ai/PROJECT_STATE.md

### Files Created

- tools/tests/fixtures/corrupted_lines_session/ (metadata.json, csi_raw.csv, notes.md)

### Notes

This session's sandbox had reset (file system resets between tasks, per environment behaviour) -- restored the working copy from the last delivered zip in /mnt/user-data/outputs/ rather than reconstructing from memory, to avoid silently diverging from what the user actually has.

### Next Recommended Task

Re-run the updated tools/validate_session.py against the user's actual three captured sessions to get a real corruption-rate number per session (not yet done -- only tested against synthetic fixtures this session). If corruption is above ~15%, investigate reducing CSI packet rate before trusting the data for Phase 2; if below, proceed to write the first analysis/ script (load, skip corrupted lines, plot amplitude vs. time).

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
