# Tidewell Revenue Pulse — case-study activities

**Status:** Draft activity plan. The live page is `tidewell/`. This file does not replace it.

**Label to keep:** October 2026 concept. Fictional company, accounts, and figures.

## Problem

A dashboard can show that monthly revenue fell and still not show why. Teams export and rebuild the story by hand, so the follow-up starts late. The concept breaks one month into a bridge, then into the accounts behind the biggest cause, then into a win-back task.

## Target user

A head of customer success at a SaaS company, preparing a monthly revenue review.

Not a local service business and not a Simple Solutions client. This is the résumé's "SaaS revenue analytics" concept.

## Role

**Concept direction.** AI-built and directed (Claude, Cursor). The hub tools line ("HTML, SVG charts, JavaScript") should not be read as a hand-coded build. Do not list case-study writing as a skill.

## Activities

| Activity | State in this repo | What to do next |
| --- | --- | --- |
| Research | **Not in the repo.** | A short note on a revenue bridge (new, expansion, contraction, churn) from public definitions. No client billing extract. |
| Flows | **Partial.** Overview → explain a down month → bridge → four accounts → one account's signals → confirm a win-back task. States: empty, loading, incomplete data, task error. | Draw it. Note that account-level detail in the current demo is for one month only. |
| Wireframes | **Not in the repo.** | **OPEN.** |
| Usability checks | **Not done.** The page says it was not tested with real users or real billing data. | One scripted session. |
| Functional test of every control | **OPEN.** | Run the checklist. Every figure on screen is demo data. |

### Functional test checklist (demo data only)

- [ ] States: Live, Empty · nothing unusual, Loading, Warning · data incomplete, Error · task fails.
- [ ] Chart: click a month. June (the demo drop) offers Explain. Other months show a net figure and say account detail is for June only, if that is still the copy.
- [ ] Explain June → bridge. The biggest-cause step is clickable.
- [ ] See the 4 accounts. Each account opens signals. Back links return to the previous step.
- [ ] Create win-back task: confirm, cancel, and the task-fails state (Try again; nothing created).
- [ ] Success state names the demo owner and does not create a task in any external tool.
- [ ] Incomplete-data warning is visible before a task can be created, and the warning text says the data is incomplete.
- [ ] No export control exists today. Do not claim one. If added, it exports the demo explanation only.
- [ ] Focus styles on month hit targets and account buttons.

## Evidence still needed

- Research note, flow, wireframes. **OPEN.**
- Usability session. **Not done.**
- Functional-test log. **OPEN.**
- Screen recording. **OPEN.**

## Honest-claims checklist

- [ ] Concept direction. AI-built and directed.
- [ ] Every account name and figure is fictional. Do not move demo revenue numbers into a résumé, a post, or a client story.
- [ ] Do not claim Tidewell found churn, saved revenue, or ran a real win-back program.
- [ ] "Not yet tested with real users or real billing data" stays until a session exists.
- [ ] October 2026 concept. One of the four résumé concepts (SaaS revenue analytics).
- [ ] Case-study writing is not a skill entry.
