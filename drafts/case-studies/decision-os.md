# Decision OS — case-study activities

**Status:** Draft activity plan. The live page is `decision-os/`. This file does not replace it.

**Label the résumés support:** October 2026 concept work on fictional data, directed by Cesar, built with AI tools.

**Label the live page uses today:** "Working build," "a real product in development," role "Product owner, design direction," and "The Chart was approved at Phase 9." That labeling **conflicts** with both attached résumés. See `drafts/resume-findings.md`. Do not repeat the product-owner or Phase 9 claims in new writing until Cesar has a source outside this repo. **OPEN:** no such source is in this repo.

## Problem

People run work through long AI chats. Decisions and promises get buried, so "where do things stand?" takes a long time to answer. The demo turns a sample ChatGPT export into four kinds of state: in hand, waiting on, decided, and not recorded.

## Target user

The live page says a founder who already plans inside ChatGPT and is juggling a few projects. Keep that user if the piece stays a concept. Do not upgrade the user into "Cesar's customers" or a shipped product.

## Role

**Concept direction** in new drafts. AI-built and directed (Claude, Cursor). The live footer still says "Product owner and design direction." That is a conflict to fix later on the site, not in this drafts task. Do not claim he wrote the implementation by hand. Do not list case-study writing as a skill.

## Activities

| Activity | State in this repo | What to do next |
| --- | --- | --- |
| Research | **Not in the repo.** | Note how a chat export is structured, using a fake sample only. The page already says the demo never reads a file from the computer. Keep that true. |
| Flows | **Partial.** Empty → import sample → progress → review (checkboxes, duplicate choice) → add to The Chart → lenses → copy handoff. States cover loading, partial read, and file-won't-open. | Draw the flow. Include Cancel and Start over. |
| Wireframes | **Not in the repo.** | **OPEN.** |
| Usability checks | **Not done.** | One session on the sample export. Do not claim Phase 9 approval as a usability result. |
| Functional test of every control | **OPEN.** | Run the checklist. Also decide, in a later site edit, whether the public label stays "working build" or moves to "concept." This draft does not change the page. |

### Functional test checklist (demo data only)

- [ ] States: New workspace, Loading · import running, Error · some unreadable, Error · file won't open.
- [ ] Import sample export shows progress and does not open a real file picker that reads the disk. The note on the page says it never reads files from the computer. Confirm that.
- [ ] Review list: uncheck an item, Add is disabled at zero, Cancel import clears state.
- [ ] Duplicate suggestion: keep both, keep only the first, keep only the second. The Chart matches the choice.
- [ ] Add to state. Counts on the four lanes match the items added.
- [ ] Lenses: Attention, CEO, Execution, Network. Each changes which lanes are emphasized. Items are not deleted by a lens.
- [ ] Copy handoff for AI copies text or shows a clear blocked-copy message. It does not send the text anywhere.
- [ ] Partial error: "3 of 42 chats" message and Retry those 3.
- [ ] File-won't-open: nothing imported; Try another file.
- [ ] Start over returns to an empty workspace.
- [ ] Source quotes open for an item. Quotes are from the fictional sample only.

## Evidence still needed

- A source, if any, for "Phase 9" and for a product separate from this demo. **OPEN. Not in this repo.** Until that exists, new claims should not use those words.
- Research, wireframes, usability log, functional-test log. **Not in repo.**
- Screen recording. **OPEN.**

## Honest-claims checklist

- [ ] Do not count Decision OS as one of the résumé's four named concepts unless the résumés are updated on purpose. Those four are the support agent, CRM cleanup, utility operations, and SaaS revenue analytics.
- [ ] Do not call Cesar the product owner of a shipped product.
- [ ] Do not say The Chart was approved at Phase 9 without a source. **OPEN.**
- [ ] Fictional sample only. "42 chats" is demo copy, not a client metric.
- [ ] AI-built and directed. October 2026 concept unless a later résumé says otherwise.
- [ ] No testimonials and no claim that this saved a founder an hour. The live problem statement uses "an hour" as the pain. That figure is **not** a measured result. Mark it **OPEN** and do not repeat it as evidence.
- [ ] Case-study writing is not a skill entry.
