# PROJECT_STATE.md

# WiFi CSI Presence Sensing
## Current Project State

---

Last Updated

2026-07-24 (session 31)

---

# Current Phase

Phase 1 — CSI Acquisition

Status:

🟢 Near-complete — three labelled sessions (ausente, presente_estatico, presente_movimiento) captured via Modo A and validated by the user. Remaining before Phase 1 closes: confirm the corruption rate on the actual captured sessions using the updated `tools/validate_session.py` (not yet re-run against them), and decide whether to recapture at a reduced packet rate if corruption is high, per `docs/acquisition_protocol.md`'s "Known issue" section.

Next Phase:

Phase 2 — Signal Characterisation (first script: load a validated session's csi_raw.csv, skip corrupted lines, plot amplitude vs. time — not started).

---

# Current Objective

Validate reliable CSI acquisition using Espressif's official esp-csi firmware on ESP32 hardware.

The objective of the next work session is NOT to process the data.

Only to demonstrate stable acquisition and create the first reproducible raw dataset.

---

# Current Status

Repository structure completed.

README completed — merge conflicts from prior branches resolved (README.md and LICENSE had unresolved Git conflict markers; both now clean).

Project architecture defined.

Research methodology defined.

Hardware available.

Firmware flashing guide written (`firmware/README.md`) — describes cloning `esp-csi`, the Modo A / Modo B setup steps, and Phase 1 exit criteria. No custom firmware code exists yet; none is expected until `esp-csi` proves insufficient.

Raw session format and acquisition protocol formally defined (`docs/acquisition_protocol.md`) — session naming convention, required `metadata.json` fields, raw CSV format, labelling discipline, immutability rule.

Hardware configuration template and pre-flight checklist written (`docs/hardware_configuration.md`) — board/router fields left as explicit `TBD` pending the physical session (not guessed, per ADR-008); checklist sequences the flash → associate → verify-CSI-stream → test-capture steps before any labelled session is recorded.

Capture automation script written (`tools/capture_session.py`, documented in `tools/README.md`) — streams live serial output directly into a correctly formatted `data/raw/` session folder with auto-generated `metadata.json`. Does not parse or interpret the CSI payload (stays within ADR-005 immutability boundary); the exact `csi_raw.csv` column layout remains provisional until real firmware output confirms it (flagged explicitly in both the script and its README, not assumed).

Project scope clarified per ADR-010: person-level CSI sensing (identification/re-identification) is documented as an in-scope future research direction — not excluded from documentation for privacy optics — governed by concrete per-session informed consent and anonymisation requirements. README gained an "Ética y consentimiento" section; `docs/acquisition_protocol.md`'s metadata schema and `tools/capture_session.py` now both enforce mandatory consent recording for any session with participants.

Session validator written (`tools/validate_session.py`) and unit-tested against synthetic fixtures (`tools/tests/`, clearly marked as non-real test data) — checks any captured session folder against the acquisition protocol schema and ADR-010 consent rules before it's trusted. All 3 tests pass. `requirements.txt` added for the `pyserial` capture dependency.

Full repository consistency audit performed: Python syntax check (py_compile), JSON fixture validity, unit test run (3/3 pass), grep for leftover Git conflict markers (none found), and cross-reference check of every file path mentioned in README/docs/firmware/tools markdown against the actual filesystem (only prospective future paths from CHANGELOG.md's own archival instructions were "missing", as expected — not a real gap). A stray malformed directory from an earlier session's shell command was found and removed. Missing scaffolding files not yet recreated in this working copy (`.gitignore`, `.gitkeep` placeholders, `.ai/CLAUDE.md`, `.ai/MASTER_PLAN.md`) were restored from the original project design. Full repository packaged as a zip and delivered to the user (40 files).

GitHub Pages site built (`docs/index.html` + `docs/assets/{css,js}`) — an in-depth, article/TFG-style public page: abstract, motivation, technical foundation with an illustrative (explicitly labelled non-real) subcarrier figure, related-work comparison table, the Modo A/B architecture diagram (rendered live via Mermaid CDN), full methodology, an ethics/consent section restating ADR-010's substance in the page's own words (since `.ai/` is gitignored and not publicly reachable), honest limitations, and a signature "instrument panel" status widget with one LED per MASTER_PLAN phase reflecting the real state in `PROJECT_STATE.md` at time of publication. A "multimedia resources" section deliberately shows empty, labelled slots (photos, plots, confusion matrices) rather than fabricating placeholder results — nothing here overstates progress beyond what's true. HTML verified well-formed (no unclosed tags) and all relative asset/doc paths verified to resolve. `docs/GITHUB_PAGES.md` documents how to enable Pages (a manual GitHub Settings action the user must perform), why `.nojekyll` exists, and how to keep the status panel and media slots honest over time as the project progresses. README.md now links to the site (URL explicitly flagged as an assumption pending confirmation, not asserted as fact, per ADR-008).

Accessibility audit of the site's colour palette (WCAG contrast ratios computed programmatically): `--text-faint` originally failed AA-normal-text contrast (3.69:1 on background, 3.28:1 on panel, both below the 4.5:1 threshold) despite passing the large-text/UI threshold — it's used for genuinely small captions/labels throughout, so the stricter threshold applies. Replaced `#6B7280` with `#8B929E` (5.7:1 on background, 5.07:1 on panel), preserving the intended visual hierarchy (still visibly dimmer than `--text-dim`) while meeting AA. All other colour pairs in the palette already passed. Also checked the stylesheet for exact-duplicate CSS selectors that could silently override each other (a specificity pitfall the design guidance calls out explicitly) — none found.

Cross-checked `tools/capture_session.py`'s actual CLI flags against `tools/README.md` and found two real defects, both fixed: (1) `--baud`, `--ap-placement`, `--sta-placement`, and `--notes` existed in the script but weren't mentioned anywhere in the README — added an "Other optional flags" section pointing to `--help` as the authoritative source. (2) The `pyserial` availability check ran at module import time, before argparse had a chance to handle `-h`/`--help` — meaning `--help` itself failed with a misleading "pyserial not installed" error instead of showing usage. Fixed by deferring the check to inside `main()`, after `parse_args()` — verified `--help` now works without `pyserial` installed, and that real execution without it still fails with the same clear message at the point it's actually needed. All 3 existing unit tests still pass.

Investigated a user-reported "Node.js 20 is deprecated" warning on the GitHub Pages site. Confirmed via web search (current as of 2026-07) this is a GitHub Actions *runner*-level deprecation notice (Node 20 -> Node 24 transition; Node 24 became default 2026-06-02, Node 20 fully removed from runners 2026-09-16) — not a defect in this site's own HTML/CSS/JS, which has no build step or Node dependency of its own. It only appears if the repository's Pages source is set to "GitHub Actions" rather than "Deploy from a branch" (the latter never invokes Actions at all, and was already the method documented in `docs/GITHUB_PAGES.md`). Addressed both possibilities: added `docs/GITHUB_PAGES.md` guidance recommending "Deploy from a branch" as the root-cause fix (avoids the whole warning category, since a build-step-free static site doesn't need Actions), and — in case Actions-based deployment is required or preferred — added `.github/workflows/pages.yml` using current major-version tags of the official Pages actions (`checkout@v4`, `configure-pages@v5`, `upload-pages-artifact@v3`, `deploy-pages@v4`), which is GitHub's own recommended mitigation (major tags receive Node 24 support automatically as each action updates, without workflow changes). YAML syntax verified valid.

Documentation consistency audit found and fixed a real gap: README.md's "Roadmap y fases" used a simplified, self-invented 6-phase numbering that didn't match `.ai/MASTER_PLAN.md`'s canonical 0-9 phase structure (already used by `PROJECT_STATE.md` and the live site's status panel) — same underlying plan, three different numbering schemes across three surfaces a reader could compare side by side. Rewrote README's roadmap to mirror MASTER_PLAN's phases 0-9 exactly, with checkbox state reflecting true current status (only Phase 0 checked), and fixed two follow-on stale references: the "Cómo empezar" step referring to old "Fase 3/Fase 4" (now correctly Fase 4/Fase 6), and the ethics section's "Fases 1-6" scope boundary (now "Fases 0-9, ver MASTER_PLAN.md"). Verified the website's own phase references were already 0-9-aligned and needed no change. Verified all README TOC anchors still resolve after the edit.

Enriched the GitHub Pages site with two new sections fitting the "artículo/TFG" framing: a Glosario (§10 — CSI, OFDM, subportadora, multicamino, PCA, STFT, Modo A/B, detector baseline, sesión) and a "Cómo citar este proyecto" section (§11 — a suggested informal citation, with an explicit caveat that unpublished-work results should be cited by commit/date since they'll change as real data arrives). Also added: favicon (inline SVG, no extra file), Open Graph/Twitter Card meta tags, and JSON-LD structured data (schema.org ResearchProject) for better link previews and discoverability; a print stylesheet (`@media print`) since an article/thesis-style page is a plausible print/PDF-export target — strips the dark background, decorative animations, and non-paper-meaningful visuals (Mermaid diagram, CSS-only subcarrier illustration) while keeping content legible in black-on-white. Re-verified after all changes: HTML well-formed, JSON-LD parses, every nav anchor resolves to a real section id, section eyebrow numbers (§1-§13) now match physical scroll order exactly (an ordering bug introduced while inserting the new sections was caught and fixed before delivery), no duplicate CSS selectors, all 3 unit tests still pass.

Found and fixed a real public-facing honesty gap: README.md's "Hardware" table still asserted the ESP32 boards were already on hand ("Ya disponible: Sí"), while the unresolved status note about hardware acquisition being in progress (raised by the user in session 6) has lived only in `.ai/PROJECT_STATE.md` — which is gitignored and never reaches a public reader. Changed the table to "Ver nota¹" with a visible footnote explaining the discrepancy and that it's pending confirmation, rather than continuing to assert unconfirmed hardware-in-hand status as fact to anyone reading the public README (per ADR-008). Also updated the top-of-README site link description to mention the new Glosario/Citar sections, and added a new `docs/GITHUB_PAGES.md` section ("Añadir o reordenar secciones") documenting the nav-anchor and section-numbering verification commands used repeatedly this session, since the site has now grown from 9 to 13 numbered sections across several sessions and future edits will need the same checks. Re-verified README TOC anchors and site nav/id consistency after these edits — all resolve correctly; all 3 unit tests still pass.

Invested a full session in professional-polish UX work on the site and README, per explicit request: (1) added a hero "stat strip" with four verifiable quick facts (cost, hardware count, phase count, license) for at-a-glance credibility, with an honesty footnote linking back to the README's hardware caveat rather than presenting the cost figure as unconditionally settled; (2) added scrollspy nav highlighting (active section highlighted in the top nav as the reader scrolls, via IntersectionObserver) and a "back to top" floating button, both genuine UX improvements for a long single-page article-style site; (3) added a GitHub profile link to the site footer alongside the existing email contact; (4) added a shields.io badge row to README.md (License, current phase, hardware, Python) for a more professional at-a-glance header — explicitly documented in `docs/GITHUB_PAGES.md` that the phase badge is a manually-set static image, not dynamic, and must be updated in lockstep with the site's own status panel to avoid reintroducing the README/site numbering mismatch fixed last session. Verified after all changes: JS syntax valid (node -c), HTML well-formed, JSON-LD parses, all nav/id anchors resolve, no duplicate CSS selectors, WCAG contrast of the new amber stat-card text (7.36:1, well above AA), print stylesheet extended to handle the new stat cards, and all 3 unit tests still pass.

Continued the polish pass: verified all `aria-labelledby` attributes resolve to real ids (accessibility correctness check) and that the inline-SVG favicon data URI decodes to well-formed SVG — both passed with no changes needed. Verified heading hierarchy across the whole page (h1 -> h2 per section -> h3 for sub-items, no skipped levels) — already correct. Found and fixed a real UX inconsistency: the "Documentación técnica completa" section mixed link styles — most doc-links pointed to GitHub blob URLs (rendered nicely by GitHub's own Markdown viewer) while `acquisition_protocol.md` and `hardware_configuration.md` used bare relative paths, which Pages serves as unstyled plain text (no Jekyll, no Markdown rendering). Unified all five doc-links to use GitHub blob URLs for a consistent, well-rendered reading experience, and updated the now-stale explanation in `docs/GITHUB_PAGES.md` that had documented the old plain-text behaviour as an "accepted limitation" — it's no longer applicable since the links changed, so keeping that text would have been misleading about the site's actual current behaviour.

Major content depth upgrade, per explicit user feedback that the site read as a README summary rather than a genuine scientific showcase: added a rigorous mathematical system model (§2.1) with real OFDM/CSI equations (received-signal model, static/dynamic multipath decomposition) rendered via KaTeX (CDN); restructured §3 into 3.1 (existing open-source tools table) and a new 3.2 "Contexto académico" citing five real, individually web-search-verified papers (WiSee/Pu et al. MobiCom'13, E-eyes/Wang et al. MobiCom'14, CARM/Wang et al. MobiCom'15, the Yousefi et al. 2017 IEEE Commun. Mag. survey, Widar3.0/Zhang et al. 2022 IEEE TPAMI) with a synthesis paragraph explaining why they're cited as conceptual grounding rather than replicated algorithms; replaced the vague "precisión, recall, F1" bullet in Metodología with formal LaTeX-rendered definitions (precision, recall, F1, FPR, ROC/AUC) tied explicitly to the metadata label field; updated References (§12) to list the five academic papers separately from the open-source tools, with DOI/PDF links where available. Caught and fixed three self-introduced consistency errors before delivery: a spurious cross-reference to a non-existent "§3.1 del protocolo de adquisición" subsection, a "§5.3" reference to a step that isn't numbered that way, and a "§5.5" subsection numbering that would have visually clashed with the adjacent 01-05 step counter (renamed to an unnumbered subsection title instead). Fixed script execution order: KaTeX's own scripts use `defer`, but mermaid.js and main.js did not, meaning they would have executed before KaTeX finished loading — added `defer` to both so all four scripts run in guaranteed document order. Verified thoroughly: HTML well-formed, JS syntax valid, JSON-LD parses, all nav/id/aria references resolve, section eyebrow and subsection numbers all match their physical position and don't collide with each other, no duplicate CSS selectors, print stylesheet extended for the new equation blocks, all 3 unit tests still pass.

Full site redesign (2026-07), per explicit user brief demanding the page stop reading as a README transcription and become a genuine showcase. Self-critique performed first (documented in-conversation): 13 sections mirroring README's own order, near-identical panel-per-section layout, no path to understanding the project in under a minute, math/citations mixed into the main flow instead of offered as optional depth, status panel and stat strip stacked as near-duplicate card grids in the hero, four thin sections (Glosario/Citar/Referencias/Documentación) that could be one. Rebuilt from scratch: tight hero (single claim + one sentence, no stat grid); a new 3-step visual explainer with hand-built inline SVG icons (router+waves, person bending a wave path, ESP32+waveform) requiring near-zero jargon, addressing the "understand in under a minute" audience; "Cómo funciona" leads with the pipeline diagram and pushes the system-model equations/citations into a native `<details>` progressive-disclosure block so casual readers can skip it and researchers can expand it; new split-column "Ingeniería" section (ADR-derived engineering principles list + repo tree + condensed tools-comparison table) aimed at the engineer-browsing-GitHub audience; "Estado real" reframed as a confident reality-check ("esto no es una demo terminada") rather than an apologetic status dump, with the phase LEDs followed by a compact one-line-per-item gap list instead of six large cards; Limitations and Ethics merged into one split-column section instead of two; Glossary/Citation/References/Docs consolidated into a single compact "Recursos" section. Cut from 780 to 354 lines of HTML. Rewrote the stylesheet from scratch afterward, keeping only CSS actually referenced by the new markup (verified programmatically) — removed roughly 15 orphaned rule blocks (old stat-card grid, media-slot cards, method-steps counters, glossary/citation-specific styles, etc.). Caught and fixed a real bug during verification: `led--active` was used directly on the hero status pill but only existed as a descendant selector (`.status-led--active .led`), so the pill's LED would have rendered as plain grey instead of the intended glowing amber — found by re-running the missing-class check without an overly broad exclusion filter that had hidden it the first pass. Updated `docs/GITHUB_PAGES.md`'s section-maintenance and media-slot instructions, which described the old §1-§13 numbered structure and `.media-slot` cards, neither of which exist anymore. Re-verified everything after all changes: HTML well-formed, JS syntax valid, JSON-LD parses, all nav/id/aria references resolve, no duplicate CSS selectors, no HTML class left without a matching CSS rule, all 3 unit tests still pass.

No firmware modifications have been made yet.

**Phase 1 has real data.** User confirmed all three labelled sessions (ausente, presente_estatico, presente_movimiento) were captured with Modo A (single ESP32, `csi_recv_router` example) and validated. First real `csi_raw.csv` sample revealed two things: (1) the initial capture attempt used the wrong baud (115200) producing binary garbage — the firmware's actual console baud is 921600, confirmed by reading `idf.py monitor`'s own startup line, not assumed; (2) even at the correct 921600 baud, real captures show occasional line corruption (dropped commas producing concatenated numbers, missing fields, out-of-range spikes) consistent with UART overrun at the observed ~130-160 packet/s rate without hardware flow control. The real esp-csi CSV header (25 fields: type,seq,mac,rssi,rate,sig_mode,mcs,bandwidth,smoothing,not_sounding,aggregation,stbc,fec_coding,sgi,noise_floor,ampdu_cnt,channel,secondary_channel,local_timestamp,ant,sig_len,rx_state,len,first_word,data) was confirmed via Espressif's own `csi_recv_router` example documentation, not guessed. Updated `docs/acquisition_protocol.md`'s provisional CSV schema to this confirmed one, with a documented "Known issue" section on the corruption pattern. Extended `tools/validate_session.py` with a per-line CSI_DATA shape check (field count + clean trailing array) — warns below 15% corruption rate, fails above it — and added a `corrupted_lines_session` test fixture plus a new unit test; also had to reshape the two existing fixtures' CSV content to match the now-enforced real schema (they previously used placeholder text that would have failed the new check). All 4 unit tests pass.

Continued improving repo polish while hardware is pending: found the README's shields.io badge colors had drifted out of sync with the site's actual palette across several redesign sessions (badges are external image URLs, invisible to any of this repo's automated checks) — resynced them to the current dark theme (amber #E0A857, cyan #4FC3E8, near-black #0A0D10) and added an explicit maintenance note in `docs/GITHUB_PAGES.md` warning that badge colors need manual resync on future palette changes, since nothing catches this automatically. Added a new "Apariencia del repositorio en GitHub" section to `docs/GITHUB_PAGES.md` with two manual, actionable improvements the user can make in repo Settings: uploading the existing OG image as the repo's social preview image, and adding GitHub topics for discoverability (repo currently has none configured).

Audited README.md and found two real staleness defects left over from the earlier phase-renumbering fix (session 15): the architecture diagram and methodology section still labelled the classifier step "(fase 2)" — a reference that didn't even match the old 6-phase scheme, let alone the current 0-9 one — and the "Métricas objetivo" table's "Se revisará tras" column still used old-numbering phase references (Fase 3/Fase 5) instead of the correct new ones (Fase 4 for classical-detector metrics, Fase 7 for the wall-penetration recall question). Fixed both, and fixed the top-of-file site description which still advertised a "glosario y guía de citación" that no longer exist as standalone sections after the site redesign. Re-verified TOC anchors resolve and no stray old phase numbers remain.

Audited the page for real defects after the dark-theme/animation session: HTML well-formed, JS valid, nav/id/aria consistent, no duplicate CSS, no missing CSS classes (one flagged candidate, `.wifi-ping`, confirmed harmless — it's a bare SVG grouping hook with no styling need, differentiated via the existing `.wifi-ping--alt .ping-ring` descendant rule). No functional bugs found. Added three more animations per request: a traveling-dash animation on the intuition multipath schematic's dynamic ray, a subtle staggered jitter-wobble on the I/Q constellation's phase-jitter dots, and an animated horizontal sweep line across the OFDM chart. All new animations respect prefers-reduced-motion. Verified HTML/CSS/tests after.

Reverted to a dark theme per user feedback (near-black #0A0D10, very subtle radial glow, no grid/grain texture), switched fonts to Inter (display+body) + JetBrains Mono (data), and added network/signal animations: an animated WiFi ping (concentric expanding rings) in the hero background, an animated TX-RX connecting line with a traveling packet dot (SVG animateMotion), a staggered chasing-flow pulse on the DSP pipeline arrows, and a subtle pulse on the dynamic multipath rays in the deep-dive diagram. All animations respect prefers-reduced-motion. Rechecked WCAG contrast for the new dark palette and lightened text-faint (#6B747D -> #7C8892) to pass AA. Regenerated OG image to match. Verified HTML/JS/tests.

Full visual identity overhaul (session 26): replaced the dark instrument-panel theme (grid background, amber/cyan on near-black, Space Grotesk/IBM Plex) with a light "drafting paper" theme — warm-neutral paper background with SVG grain texture and radial vignette (no grid), Fraunces (serif display) + Work Sans (body) + Space Mono (data), and a brass/deep-teal accent pair. Added a 3D cursor-tilt effect (perspective + rotateX/rotateY on mousemove) on panels, pipeline stages, and the hero status pill, disabled on touch devices and under prefers-reduced-motion. Re-verified WCAG contrast for the new palette and darkened text-faint/amber slightly to pass AA against both backgrounds. Regenerated the OG image and favicon to match. Verified HTML/JS/tests after all changes.

Continued the technical redesign: trimmed 4 more em-dashes in the new deep-dive/intuition copy for punctuation variety (9 -> 5), and added small tick marks to the Fresnel-zone schematic's axis for visual consistency with the other two technical intuition diagrams. Verified HTML/tests.

Replaced the three intuition icons with technical RF schematics (multipath propagation, Fresnel-zone obstruction, I/Q constellation with phase jitter); replaced the CSS-bar subcarrier illustration with an inline SVG simulating a real 64-subcarrier 802.11n channel response (dB grid, subcarrier-index axis, multipath fading null); removed the Mermaid diagram (and its CDN script + init code) in favour of a native HTML/CSS DSP pipeline (RF Frontend -> Frame Capture -> H_k Extraction -> Noise Filtering -> Windowing/STFT -> Feature Extraction -> Adaptive Threshold); merged the separate gap-list into the phase status panel as explicit technical objective badges per pending phase, removing the redundant block. Verified: HTML well-formed, JS valid, no orphaned CSS classes, mermaid fully removed, all 3 tests pass.

Reduced em-dash density in docs/index.html from 26 to 7 occurrences (across sessions 22-23), rewriting sentences with periods/colons/semicolons/commas for punctuation variety — a concrete fix against the "generic AI writing" tell, per the standing UX brief.

Added a hand-built inline SVG diagram (static vs. dynamic multipath paths) inside the "Cómo funciona" deep-dive, next to the multipath equation — replaces part of the text-only explanation with a visual, per the standing UX brief's "replace text with visuals" priority. Verified HTML/JS/tests after the change.

Found and fixed a documentation-process gap: the prior session's CHANGELOG entry claimed PROJECT_STATE.md had been updated, but it hadn't actually been edited — corrected retroactively. Also found and fixed a real UI defect in the new multipath SVG: in-SVG text labels at font-size 7 (SVG units) would render at roughly 10px on screen, illegible, and were redundant with the HTML caption paragraph already present below the diagram — removed the in-SVG text, kept the caption as the single source of that explanation.

Generated a real Open Graph preview image (`docs/assets/og/og-image.png`, 1200x630, via PIL, using locally available IBM Plex Mono to match the site's own design system) since none existed — social link previews had no image before. Wired into `og:image`/`twitter:image` meta tags (twitter:card upgraded to `summary_large_image`). Note: this same session repeated the earlier documentation-process gap once — CHANGELOG recorded this work before PROJECT_STATE.md did — corrected here.

No datasets have been collected yet — this requires physical hardware in hand, which is outside what an AI session can perform. The documentation is now ready for that session.

No Python analysis scripts exist yet — intentionally deferred (see ADR-003, ADR-005; nothing to analyse before raw data exists).

No experiments have been executed.

---

# Next Task

Physical, hands-on task (requires the user at the bench with the ESP32 boards):

1. Clone `espressif/esp-csi`, flash Modo B (two dedicated ESP32s: AP + STA/sniffer) following `firmware/README.md`.
2. `pip install pyserial` on the host machine.
3. Confirm CSI frames appear over serial with `idf.py monitor`, no corruption, roughly stable packet rate.
4. Capture at least one raw session per label class (`ausente`, `presente_estatico`, `presente_movimiento`) at Modo B using `tools/capture_session.py` (see `tools/README.md`), following the format in `docs/acquisition_protocol.md`.
5. Run `tools/validate_session.py` on each captured folder immediately; fix any structural error before moving to the next label. Note in `docs/acquisition_protocol.md` if the real firmware line format differs from what was assumed.
6. Optionally repeat for Modo A (existing router) once Modo B is confirmed stable.

---

# Immediate Priorities

Priority 1

Reliable CSI acquisition (hardware-dependent, next physical session).

Priority 2

Raw dataset generation.

Priority 3

Initial signal visualisation (first `analysis/` script — just load + plot, no detection logic yet).

Nothing else should be implemented before these tasks are complete.

---

# Known Decisions

Current architecture uses:

• Espressif esp-csi as acquisition framework.

• Two ESP32 devices (Modo B) as the primary experimental configuration; Modo A (existing router) as secondary/optional.

• Python for all offline signal processing.

• Person-level CSI sensing (identification) is an in-scope future research direction, governed by per-session informed consent and anonymisation (ADR-010) — not excluded from the project.

Refer to DECISIONS.md before modifying any architectural choice.

---

# Known Risks

Possible router incompatibilities (Modo A specifically — untested, flagged as an open question in `firmware/README.md`).

ESP32 firmware limitations.

Packet loss.

Unstable packet timing.

Dataset quality depends heavily on experimental methodology.

These risks should be evaluated experimentally, not assumed.

---

# Available Hardware

2 × ESP32-WROOM

1 × WiFi Router (2.4 GHz)

USB cables

Development PC

No additional hardware required.

**Status note (2026-07-02, session 6):** earlier documentation (README "Hardware" section) assumed the ESP32 boards were already on hand ("Ya disponible: Sí"). The user has indicated hardware acquisition is currently in progress. This section is left as originally specified rather than guessed at, per ADR-008 (scientific honesty) — confirm actual hardware-in-hand status before starting the physical session, and update this section and README's Hardware table once confirmed.

---

# Pending Deliverables

☑ Firmware flashing guide (documentation only — code pending physical session)

☑ Raw dataset format specification

☑ Hardware configuration template + pre-flight checklist

☑ Capture automation tooling (tools/capture_session.py)

☑ Session validator + unit tests (tools/validate_session.py, tools/tests/)

☑ GitHub Pages public project site (docs/index.html + assets/) — pending manual activation in GitHub Settings

☑ GitHub Actions workflow for Pages deployment (.github/workflows/pages.yml) — optional alternative to branch-based deploy

□ Raw CSI acquisition (actual capture — requires hardware session)

□ Initial signal plots

---

# Blockers

Raw CSI acquisition itself requires physical access to the ESP32 hardware and cannot be completed in a documentation-only session. All Phase 1 documentation deliverables (flashing guide, session format spec, hardware config template, pre-flight checklist) are now complete — there is no further engineering work that can be done without physical hardware in hand. The next session must be a hands-on capture session.

Separately (not a Phase 1 blocker, but a pending user action): the GitHub Pages site is built but not live — enabling it requires a manual step in the repository's GitHub Settings (Settings → Pages → source = `main` branch, `/docs` folder), which an AI session cannot perform. See `docs/GITHUB_PAGES.md`. The README's link to the site assumes a specific repo owner/name and should be confirmed once Pages is actually enabled.

---

# Session Resume

When continuing work:

1. Complete the current phase before starting the next.

2. Do not begin feature extraction until raw acquisition is fully validated.

3. Do not implement Machine Learning before a classical baseline exists.

4. Update PROJECT_STATE.md after every completed work session.

5. Record important architectural decisions in DECISIONS.md.

6. Record completed work in CHANGELOG.md.
