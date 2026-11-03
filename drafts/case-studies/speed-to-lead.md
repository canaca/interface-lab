# Speed-to-lead automation builder — case-study activities

**Status:** Planned piece. **Not built** in this repo. Do not link it from the site until the standing rule is met.

**Label:** October 2026 (or later) concept. Fictional business and fictional leads. GoHighLevel-style means the interaction pattern (trigger, wait, message, pipeline stage). It is not a GoHighLevel screenshot, not a partner integration, and not a claim that this builder is inside a client's account.

## Problem

A local service business can buy ads and still lose the lead. The form sits there, the call hits voicemail, and nobody has a next step. The concept is a builder where the owner assembles a follow-up path: instant reply, missed-call text-back, and a pipeline stage, then runs it on demo leads before anything is turned on.

## Target user

The owner or office manager of a local service business that is already running ads. They are not a CRM administrator. They need to see what will be sent, to whom, and what happens if they turn a step off.

Domain context for Cesar, not a result of this piece: he has used GoHighLevel for 6+ years (résumé). Do not write "6+ years" on the concept UI. Do not imply this prototype served the 10–12 Simple Solutions clients or the SactownVideo book.

## Role

**Concept direction.** AI-built and directed (Claude, Cursor, or the same class of tools). Cesar sets the problem, user, flow, and design decisions and reviews every state. He does not have to hand-write the script. Do not list case-study writing as a skill.

## Activities to complete before publish

| Activity | State | Next |
| --- | --- | --- |
| Research | **Not started.** | Map a generic new-lead path from public descriptions of instant reply, missed-call text-back, and a simple pipeline. No client account, no real phone numbers, no screenshots of a live CRM. |
| Flows | **Not started.** | One primary flow: demo lead arrives → instant reply (preview) → missed call → text-back (preview) → pipeline stage updates → owner task. Branches: step off, send error, empty pipeline, duplicate lead. |
| Wireframes | **Not started.** | Mobile and desktop. Builder on one side, a demo inbox and pipeline on the other. |
| Usability checks | **Not started.** | At least one session with a stand-in owner. Script only. No result until the session happens. |
| Functional test of every control | **Not started.** The piece does not exist yet. | Build it, then run the checklist on demo data. |

### Controls the piece must include (all working, or do not publish)

- [ ] A demo business with a fixed set of leads. No live inbox and no real SMS.
- [ ] Trigger list: form submitted, call missed, lead stage changed. Each can be turned on or off.
- [ ] Instant-reply step: message preview, on/off, save. Preview never sends.
- [ ] Missed-call text-back step: message preview, on/off, save. Preview never sends.
- [ ] Pipeline: named stages, drag or explicit move of a demo lead, undo move.
- [ ] Test run: pick one demo lead, step through the path, show what would send. A failure state says nothing was sent.
- [ ] Filters: by stage, by trigger, and a "would have texted" vs "still open" filter on the demo list.
- [ ] Export: download or copy a plain-language summary of the automation and the demo run. Export contains demo data only.
- [ ] Empty, loading, and error states, reachable without breaking the other controls.
- [ ] Every button, filter, and export in the checklist has a pass/fail line in a log.

Standing rule: the piece is publishable only when that log is complete and every control works on demo data.

## Evidence still needed

All of the above. Nothing for this piece is in the repo. Client results that might someday illustrate the problem (views, CTR, budgets) stay off this case study. They are not evidence that a prototype worked.

## Honest-claims checklist

- [ ] Concept direction. AI-built and directed.
- [ ] "GoHighLevel-style" describes the pattern, not a certification, a partnership, or access to a client's sub-account.
- [ ] No real leads, no real sends, no A2P claim. The 100% A2P figure is a team result at SactownVideo and does not belong on this concept.
- [ ] No prices, no client counts, no testimonials.
- [ ] Do not say the builder shortened response time by any amount. No measured time exists for this piece.
- [ ] Fictional business name only.
- [ ] Case-study writing is not a skill entry.
