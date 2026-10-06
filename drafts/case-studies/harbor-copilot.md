# Harbor CRM Copilot — case-study activities

**Status:** Draft activity plan. The live page is `harbor-copilot/`. This file does not replace it.

**Label to keep:** October 2026 concept. Fictional company, people, and deals.

## Problem

Pipelines go stale: deals go quiet, owners leave, close dates slip. Cleaning that up by hand is tedious, and letting an AI edit the CRM in bulk is risky. The concept proposes a change set, shows each change in the table, and lets a person apply, skip, or undo.

## Target user

A sales manager cleaning the team pipeline before a forecast call.

This is not a GoHighLevel screenshot and not a Simple Solutions client account. It is the résumé's "CRM deal cleanup" concept, with undo for bulk changes.

## Role

**Concept direction.** AI-built and directed (Claude, Cursor). The hub tools line ("HTML, CSS, JavaScript") should not be read as a hand-coded build. Do not list case-study writing as a skill.

## Activities

| Activity | State in this repo | What to do next |
| --- | --- | --- |
| Research | **Not in the repo.** | A short note on bulk CRM edits and why conflicts need a person. No client pipeline. |
| Flows | **Partial.** Scan → review diffs → select safe vs risky → conflict choice → apply → partial failure → per-row undo and undo all. Empty and loading states exist in the States menu. | Draw it, including Discard set and the "show changed deals only" filter. |
| Wireframes | **Not in the repo.** | **OPEN.** |
| Usability checks | **Not done.** The page says it was not tested with real users or a real CRM. | One scripted session. Do not invent a finding. |
| Functional test of every control | **OPEN.** | Run the checklist on the fictional 14-deal board. That "14" is demo deals, not the SactownVideo client book. |

### Functional test checklist (demo data only)

- [ ] States: Live, Empty · nothing stalled, Loading · scanning, Error · 2 changes fail.
- [ ] Clean up stalled deals starts a scan and does not write to any external CRM.
- [ ] Empty state: no change set, Done returns cleanly.
- [ ] Review: diffs show old and new. Risky close (Summit Fitness in the current copy) is not pre-selected. Conflict (Lakeside Health in the current copy) is held.
- [ ] Checkboxes, Clear, Select safe, Apply (disabled at zero), Discard set.
- [ ] Show changed deals only filters the table and can be turned off.
- [ ] Conflict buttons: Apply copilot's on top, and Skip deal.
- [ ] Apply writes only the selected demo rows. Change log lists them.
- [ ] Partial-failure state names the rows that failed and says the others applied. Retry those rows.
- [ ] Undo on one log row restores that deal. Undo all restores the set. Toast Undo all matches.
- [ ] Done / restart returns to idle.
- [ ] No export control exists today. Do not claim an export until one is built and tested. If an export is added, it must download the demo change set only.

## Evidence still needed

- Research note, flow, wireframes. **OPEN.**
- Usability session. **Not done.**
- Functional-test log. **OPEN.**
- Screen recording. **OPEN.**
- Confirmation that no button calls a live CRM. **OPEN until the click-through.**

## Honest-claims checklist

- [ ] Concept direction. Not "Design and build" (older footer in `072bf63` only).
- [ ] AI-built and directed. Matches the résumé line on undo for bulk changes.
- [ ] Fictional deals only. Do not attach Harbor's board to SactownVideo or Simple Solutions clients.
- [ ] Do not say the copilot improved win rate, forecast accuracy, or revenue.
- [ ] "Not yet tested with real users or a real CRM" stays until a session exists.
- [ ] October 2026 concept.
- [ ] Case-study writing is not a skill entry.
