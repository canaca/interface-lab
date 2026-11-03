# Kestrel Agent Console — case-study activities

**Status:** Draft activity plan. The live page is `kestrel/`. This file does not replace it.

**Label to keep:** October 2026 concept. Fictional company, customer, ticket, and amounts.

## Problem

Support teams want an agent to handle a refund, but a wrong refund costs money and trust. A chat log does not show what the agent is about to do. The concept makes the run a visible pipeline and stops for a person before money moves and again before a reply is sent.

## Target user

A support lead who reviews agent actions between tickets and owns the refund policy.

Not a Simple Solutions client. The approval pattern is the part that can later illustrate "a person approves before anything goes out." It is still a fictional support product.

## Role

**Concept direction.** AI-built and directed (Claude, Cursor). The live hub lists tools as "HTML, CSS, JavaScript" only. That line is incomplete next to the résumés. In anything new, say the prototype was AI-built under his direction. Do not claim he hand-wrote it, and do not list case-study writing as a skill.

## Activities

| Activity | State in this repo | What to do next |
| --- | --- | --- |
| Research | **Not in the repo.** | A short note on human approval before an agent moves money or sends a message. Public product patterns only. No client names. |
| Flows | **Partial.** The page's decision list is the flow: ticket → tool calls → refund approval (amount editable) → reply draft → send or keep as draft, plus error branches. | Draw that flow, including Decline, handoff, and both error states. |
| Wireframes | **Not in the repo.** | **OPEN** whether frames exist outside the repo. |
| Usability checks | **Not done.** The page says it was not tested with real users or a real billing system. | One scripted session on the demo ticket. Record only what was observed. |
| Functional test of every control | **OPEN.** Buttons exist in the page source. No pass/fail log is in the repo. | Run the checklist below. |

### Functional test checklist (demo data only)

- [ ] States: Live run, Empty · queue clear, Loading, Error · billing down, Error · send fails.
- [ ] Run agent on the demo ticket. Trace shows tool, input, and output. Sources appear.
- [ ] Run stops at the refund gate. Nothing is marked sent before approval.
- [ ] Approve refund, Change amount (reject an out-of-range amount, accept an in-range one), Decline.
- [ ] After approval, the reply stays a draft until Send reply.
- [ ] Keep as draft: toast or status says nothing was sent.
- [ ] Send-fails state: Try again; copy says it was not sent.
- [ ] Billing-down state: nothing was refunded; Retry run; Hand off to a person.
- [ ] Next ticket returns to a clear queue or the next demo state the page actually implements.
- [ ] Elapsed time and tool-call count update only from the demo run.
- [ ] Focus styles on the approval buttons.

No control may call a real billing API or send a real email. If one does, stop and treat that as a failure.

## Evidence still needed

- Research note, flow diagram, wireframes. **OPEN / not in repo.**
- Usability session. **Not done.**
- Functional-test log. **OPEN.**
- A 15–20s screen recording. **Not in this repo. OPEN.**

## Honest-claims checklist

- [ ] Role is concept direction. The design-leaning résumé already names this piece: the agent works a refund ticket, and a person approves the money and the reply.
- [ ] AI-built and directed. Do not say "prototype build" or "Design and build" (that older footer is only in commit `072bf63`).
- [ ] Demo amounts and "Acme Dental" stay fictional. Do not attach them to a real support team.
- [ ] "Not yet tested with real users or a real billing system" stays until a session exists.
- [ ] Do not claim a reduction in refunds, handle time, or error rate.
- [ ] October 2026 concept. Not a product in production.
- [ ] Case-study writing is not a skill entry.
