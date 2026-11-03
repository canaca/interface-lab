# Meta ads cost-per-lead copilot — case-study activities

**Status:** Planned piece. **Not built** in this repo. Do not link it from the site until the standing rule is met.

**Label:** Concept. Fictional ad account. The copilot explains and proposes. A person approves before any recommendation is marked applied. Nothing here changes a real Meta account.

## Problem

Someone running Meta ads can see a cost-per-lead figure and still not know what to do next, or can let a tool change spend without a check. The concept is a review screen: pick a demo campaign, see which leads the demo data ties to that campaign, read a proposed next step, and approve or dismiss it. The point of the interface is the review, not a promise that cost per lead will fall.

## Target user

The owner of a local service business that is already running Meta ads, or the person who reviews those ads with them. They are not a full-time media buyer. They need plain language and a gate before anything is "applied."

Domain context from the résumés, **not results of this prototype:** Cesar has run Meta ads since 2017, reviewed hook rate, CTR, and lead quality with clients, and personally managed one med-aesthetics account. Do not put that client's performance, budget, or CTR on this piece. Those figures are not demo data and are not to be invented into a testimonial.

## Role

**Concept direction.** AI-built and directed. Cesar sets the review flow and the rule that the copilot cannot apply a change alone. Do not claim he wrote an ads-API integration. Do not list case-study writing as a skill.

## Activities to complete before publish

| Activity | State | Next |
| --- | --- | --- |
| Research | **Not started.** | Define the on-screen fields from public Meta terms (campaign, ad set, objective, lead, cost per lead as a label). **OPEN:** the exact checklist of "first things to check" is not locked. The week-1 social draft lists that checklist as a Cesar decision (item C12). Do not invent the six checks. |
| Flows | **Not started.** | Choose a demo account → filter → open one campaign → see the demo breakdown → read one proposal → approve or dismiss → export a review note. Error if the demo "account" fails to load. Empty if the filter matches nothing. |
| Wireframes | **Not started.** | One review layout. Proposals look different from applied changes. |
| Usability checks | **Not started.** | One session: can a stand-in tell that nothing was sent to Meta? |
| Functional test of every control | **Not started.** | Build, then run the checklist. |

### Controls the piece must include (all working, or do not publish)

- [ ] A fictional account with several campaigns. No Meta login, no token, no live pull.
- [ ] Filters that actually change the list: objective, a demo date range, and on/off or "needs review."
- [ ] Campaign detail: the demo's lead count and cost per lead, clearly marked **sample data**.
- [ ] A proposal (for example "pause this demo ad set" or "duplicate this demo concept") that stays a proposal until Approve.
- [ ] Approve and Dismiss. Approve updates only the demo state. Dismiss leaves it unchanged.
- [ ] Undo the last approval inside the demo.
- [ ] Export or copy a review summary that includes the sample-data label and does not include a real account id.
- [ ] Empty, loading, and error states. Error says the demo account did not load and that no change was made.
- [ ] Pass/fail log for every control.

If a control cannot work without a real ad account, cut the control. Do not publish a dead button.

## Evidence still needed

The whole piece. Also **OPEN:** which review checks Cesar wants on the screen (do not invent them). Also **OPEN:** whether any real account screenshot will ever be used. Default is no.

## Honest-claims checklist

- [ ] Concept direction. AI-built and directed. October 2026 or later concept, same honesty bar as the other pieces.
- [ ] Every cost, lead count, and rate on screen is fictional sample data.
- [ ] Do not use the med-aesthetics CTR, cost per result, view counts, or budget as if this copilot produced them.
- [ ] Do not promise a lower cost per lead, a better CTR, or a return.
- [ ] The copilot does not send, spend, or edit a live account. The UI has to show that, not only the case study.
- [ ] No testimonials.
- [ ] Social posts about this piece must not quote the sample dollar figures. See `drafts/simple-solutions/pillar-to-portfolio-map.md`.
- [ ] Case-study writing is not a skill entry.
