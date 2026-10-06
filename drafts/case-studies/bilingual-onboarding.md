# Bilingual client-onboarding flow — case-study activities

**Status:** Planned piece. **Not built** in this repo. Do not link it from the site until the standing rule is met.

**Label:** Concept. Fictional client. Mobile-first. English and Spanish are both first-class, not a translated afterthought.

## Problem

Getting a local service client from "yes" to ads-live is a sequence of small handoffs: offer, access, what will be filmed or collected, creative approval, and a first check-in. If the owner is more comfortable in Spanish, a flow that only works in English drops steps. The concept is a mobile flow the owner can finish in either language, with the same questions and the same confirmation at the end.

## Target user

The owner of a local service business who is being onboarded, often on a phone, in English or Spanish. A second user is the person running onboarding (the role Cesar has done), who needs to see what the owner completed.

Domain context, not a result of this piece: at SactownVideo he personally onboarded 3 clients and inherited 11, on a 3–4 week onboarding target (résumé). Do not put "3 of 14" or that target on the concept as if the prototype produced them.

## Role

**Concept direction.** AI-built and directed. Cesar sets the steps, the bilingual behavior, and the review of every state. Fluent English/Spanish on the résumé supports him directing both languages. It does not by itself prove a usability test was done. Do not list case-study writing or translation as a tested skill until a review is recorded. **OPEN:** whether a Spanish speaker besides Cesar has reviewed the copy. None exists yet because the piece is not built.

## Activities to complete before publish

| Activity | State | Next |
| --- | --- | --- |
| Research | **Not started.** | List the onboarding steps from the résumé's real sequence (offer, filming or asset prep, CRM orientation, creative approval, week-one check-in) as the *kind* of steps. Use a fictional trade (for example a heating-and-air company). No real client name, contract, or login. |
| Flows | **Not started.** | Mobile path: welcome → business → offer → access checklist → creative approval → review → done. Language toggle available on every step. Error if a required answer is missing. A "save and continue" that stays on the device or in demo state only. |
| Wireframes | **Not started.** | Phone width first. Show the same screen in both languages so overflow is visible. |
| Usability checks | **Not started.** | One pass in English and one in Spanish. Record only what was observed. Do not claim both languages were "tested" before that. |
| Functional test of every control | **Not started.** | Build, then run the checklist. |

### Controls the piece must include (all working, or do not publish)

- [ ] Language control switches **all** visible strings, including buttons, errors, and the review summary. It does not reload into a broken half-translated screen.
- [ ] Progress shows the current step. Back and Next work. Next is blocked when a required field is empty, with an error in the active language.
- [ ] Offer step: choose or type a fictional offer. No prices in the UI if this screen will be reused in Simple Solutions posts. Portfolio demo may omit prices entirely.
- [ ] Access checklist: each item can be checked, unchecked, and marked "not yet."
- [ ] Creative approval: approve or request a change, with a note. Nothing is marked approved by default.
- [ ] Review screen lists every answer. Edit jumps back to that step.
- [ ] Finish writes a demo completion state. Export or copy a summary in the active language. Nothing is emailed unless the user explicitly uses their own mail app, and the draft must say so.
- [ ] Empty (new client), loading, and a save-error state. Save error says the answers are still on the device.
- [ ] Filters, if a staff view exists: by language and by step completed. If there is no staff view, do not claim a filter.
- [ ] Pass/fail log for every control above.

Standing rule: publish only after that log passes on demo data.

## Evidence still needed

The whole piece. Also **OPEN:** a second reader for the Spanish copy. Do not call the Spanish "reviewed" until that reader is named in the notes or Cesar records that he alone reviewed it and the claim stays that narrow.

## Honest-claims checklist

- [ ] Concept direction. AI-built and directed.
- [ ] Fictional client. Not one of the 3 onboarded or 11 inherited accounts.
- [ ] Do not claim a 3–4 week launch happened inside this prototype.
- [ ] Bilingual means the UI works in both languages, not that it guarantees a business outcome.
- [ ] No testimonials, no "clients loved it," no completion-rate number.
- [ ] No prices or dollar amounts on screens that might be posted by Simple Solutions.
- [ ] Case-study writing is not a skill entry.
