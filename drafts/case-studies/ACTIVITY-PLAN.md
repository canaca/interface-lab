# Portfolio activity plan

**Status:** Draft checklist. Nothing here is published. The live Interface Lab pages stay as they are until a later change.

**Standing rule:** a piece is not ready to publish until it is fully functional: every button, filter, export, and workflow works on demo data. A control that is only drawn, or that calls a service the demo does not have, is not done.

**Role on every piece:** concept direction. AI-built and directed. October 2026 concept work for the pieces that already exist. Do not claim Cesar wrote the Blender scripts. Do not list case-study writing as a skill.

**Honesty rule:** do not invent client results, numbers, or testimonials. Mark gaps **OPEN**.

## Priority

1. Prove the five live pieces with a real click-through, and stop any claim the résumés do not support.
2. Fill the evidence gaps on those five (research note, flow, wireframes, usability) without rewriting the live site in this task.
3. Build the three planned pieces in the order below. Each one ships only after its own functional test passes.
4. Only then connect a piece to a Simple Solutions post (`drafts/simple-solutions/pillar-to-portfolio-map.md`).

Label fixes on the live site (Decision OS "working build," hub "I design," tools lines that omit AI) are **next work for a later edit**, documented in `drafts/resume-findings.md`. They are not done here, because this task must not change published pages.

## What is done

"Done" here means "present in the repo on `main`," not "tested" and not "ready to claim on a résumé."

| Piece | In the repo | Case study on the live page | Separate research, wireframes, usability log | Functional-test log |
| --- | --- | --- | --- | --- |
| Valley Grid Operations | Yes. `valley-grid/`, 3D scene, States menu, film mode. | Yes. `valley-grid/CASE-STUDY.md` and the hub details. | No. | **OPEN.** |
| Kestrel Agent Console | Yes. `kestrel/`. | Yes, bottom of the page. | No. | **OPEN.** |
| Harbor CRM Copilot | Yes. `harbor-copilot/`. | Yes, bottom of the page. | No. | **OPEN.** |
| Tidewell Revenue Pulse | Yes. `tidewell/`. | Yes, bottom of the page. | No. | **OPEN.** |
| Decision OS | Yes. `decision-os/`. | Yes, but the public label conflicts with the résumés. | No. | **OPEN.** |
| Speed-to-lead automation builder | No. | Draft only: `speed-to-lead.md`. | No. | Not started. |
| Bilingual mobile onboarding | No. | Draft only: `bilingual-onboarding.md`. | No. | Not started. |
| Meta ads cost-per-lead copilot | No. | Draft only: `meta-ads-cpl-copilot.md`. | No. | Not started. |

Résumé coverage today: the attached résumés name **four** concepts (support agent, CRM cleanup, utility operations, SaaS revenue analytics). Those match Kestrel, Harbor, Valley Grid, and Tidewell. Decision OS is extra and is labeled more strongly than the résumés allow.

## What's next — ordered checklist

### A. Live pieces, before any stronger public claim

- [ ] **A1. Valley Grid functional test.** Run `valley-grid.md` checklist in a browser. Write pass/fail. **OPEN.**
- [ ] **A2. Kestrel functional test.** Same for `kestrel.md`. **OPEN.**
- [ ] **A3. Harbor functional test.** Same for `harbor-copilot.md`, including the "changed deals only" filter and both undo levels. **OPEN.**
- [ ] **A4. Tidewell functional test.** Same for `tidewell.md`. **OPEN.**
- [ ] **A5. Decision OS functional test.** Same for `decision-os.md`, including lenses, duplicate choice, and copy handoff. **OPEN.**
- [ ] **A6. Fix fail items** from A1–A5 on demo data only. No new claimed metrics.
- [ ] **A7. One-page flow** for each live piece, taken from the page that already exists. Research notes and wireframes stay **OPEN** until files exist. Usability sessions are **not done**; the live copy already says users were not tested.
- [ ] **A8. Later site edit (not this PR):** align credits with the résumés. Concept direction. AI-built and directed. Decision OS not described as a shipped product or as Phase 9 approval unless a source shows up. Tools lines should not read as "he hand-coded this" or "he wrote the Blender scripts."

### B. New pieces, in build order

Order follows the work Cesar can direct from real process knowledge, without inventing results. Speed-to-lead is the core Simple Solutions follow-up story. Onboarding is the next step a client feels. The ads copilot is last because its on-screen checks are still **OPEN** (do not invent the review list).

- [ ] **B1. Speed-to-lead builder** — research, flow, wireframes, then a functional build, then usability, then the full control test in `speed-to-lead.md`. Publish only after the test passes.
- [ ] **B2. Bilingual onboarding** — same sequence (`bilingual-onboarding.md`). Spanish review is **OPEN** until someone records it.
- [ ] **B3. Meta ads copilot** — block the build of the "what we check" list on Cesar's own list. **OPEN** (week-1 draft calls this decision C12). Then the same research → flow → wireframes → functional build → usability → control test sequence (`meta-ads-cpl-copilot.md`).

### C. After a piece actually passes

- [ ] Add it to the hub only in a separate change, with fictional-data labeling and concept-direction credit.
- [ ] Draft social posts from `drafts/simple-solutions/pillar-to-portfolio-map.md`. Posts still need Cesar's approval. This plan does not schedule or publish them.
- [ ] Keep client budgets, A2P, and the med-aesthetics performance figures off the portfolio UI and off social posts.

## Not in scope for "done"

- Rewriting `index.html`, navigation, or GitHub Pages.
- Merging this drafts branch.
- Claiming a piece is tested because the source code contains a click handler.
