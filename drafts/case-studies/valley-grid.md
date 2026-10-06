# Valley Grid Operations — case-study activities

**Status:** Draft activity plan. Not a published case study. The live page is `valley-grid/` plus `valley-grid/CASE-STUDY.md`. This file does not replace them.

**Label to keep:** October 2026 concept. Fictional substation, people, crews, and readings.

## Problem

A control-room operator gets an equipment alarm as numbers, then has to jump between screens and calls to decide whether a crew should go. The concept puts that path on one screen: alert, evidence, a suggested cause, a confirmed action, and a resolution.

## Target user

A control-room operator on shift, responsible for several substations (the live page says nine), who has a few minutes to understand one alert and act.

This user is not a Simple Solutions client. Do not describe Valley Grid as client work.

## Role

**Concept direction.** AI-built and directed (Claude, Cursor). Cesar set the problem, the user, the flow, and the design decisions, and reviewed states. He did not write the Blender scripts (`blender/build_t2.py`, `blender/board2.py`). Do not list case-study writing as a skill.

## Activities

| Activity | State in this repo | What to do next |
| --- | --- | --- |
| Research | **Not in the repo.** No operator interviews, no source notes. | Write a short research note from public material only (how a substation alarm is handled). Mark every borrowed fact. No utility client. |
| Flows | **Partial.** The page and `valley-grid/CASE-STUDY.md` describe one path: alert → investigate → evidence → dispatch, acknowledge, or escalate → confirm → resolve or error. | Save that path as its own flow, including the film-mode branch and the States-menu branches (empty, loading, trend error, dispatch error). |
| Wireframes | **Not in the repo.** | Keep any frames that still exist outside this repo, or redraw the panel states. **OPEN** whether earlier frames exist elsewhere. |
| Usability checks | **Not done.** The live case study says it was not tested with real operators. | Script a click-through with a stand-in (not a claimed utility client). Record what confused them. Do not invent a test result. |
| Functional test of every control | **OPEN.** Handlers exist in `valley-grid/index.html`. Nobody has logged a pass/fail click-through in this repo. | Run the checklist below on demo data before any new public claim that "every control works." |

### Functional test checklist (demo data only)

- [ ] States menu: Live alert, Empty, Loading, Error · trend unavailable, Error · dispatch fails.
- [ ] Film mode plays the documented sequence and the end card; Skip intro works when it is shown.
- [ ] Orbit / drag on the model; click bushing B opens the investigation.
- [ ] Investigate, Dispatch crew, Acknowledge, Escalate.
- [ ] Crew choice, optional note, Confirm dispatch, Cancel.
- [ ] Acknowledge confirm and cancel.
- [ ] Escalate: note, Send to Marisol, cancel; Dispatch crew 4 only after the scripted reply.
- [ ] Dispatch failure: message says nothing was sent; Try again; choices kept.
- [ ] Trend retry after the data-error state.
- [ ] Back to overview from each step that offers it.
- [ ] Timeline scrub and Play / Pause.
- [ ] Resolved state returns to an empty board and does not send anything off the page.
- [ ] Keyboard: time slider and buttons can be reached and show a visible focus style.

Standing rule: do not treat this piece as ready to publish (or to re-publish with stronger claims) until every box above passes on demo data.

## Evidence still needed

- Research note and flow file. **OPEN.**
- Wireframes. **OPEN.**
- A recorded usability session. **Not done.**
- A filled functional-test log (date, browser, pass/fail per control). **OPEN.**
- The 15-second film file described in `valley-grid/CASE-STUDY.md`. Stills are in `img/`. A finished clip is **not in this repo.** **OPEN.**
- Any real operator quote or live sensor feed. **Do not add.** The concept stays fictional.

## Honest-claims checklist

- [ ] Call the role **concept direction**, not "3D modeling," "front-end build," or "Design and build."
- [ ] Say the 3D scene was built with AI tools he directed. Do not say he wrote the Blender scripts.
- [ ] Keep "not tested with real operators or live data" until a real session exists. Then describe that session only.
- [ ] Fictional names only (Sierra Gate, crews, Marisol in the demo). Not clients.
- [ ] No client results, lead counts, or testimonials.
- [ ] October 2026 concept work, not a utility product he shipped.
- [ ] Do not add "case-study writing" to a skills list because this page has a case study.
