# Weekly review · 23 November 2026

This branch continues draft PR #12 (16 November, unmerged). It is a new draft that supersedes #12 if you would rather merge one pull request. It includes the 19 October, 26 October, 2 November, 9 November, and 16 November work, plus this week. It does not replace pull request #10. Nothing here is merged. `main` is unchanged. Cesar publishes.

The deeper Relay pass below is the work that supersedes draft pull request #13. Same rule: one draft if you would rather merge one pull request. Pull request #10 was not edited.

## Relay, for a hiring manager

Relay is the piece to open for customer success, onboarding, implementation, or account management. A person can pick one of four fictional follow-ups, or write a sentence. Each draft sets the timing, the channel, and the branch.

- Med spa lead. Text within a minute, offer two times, tell the owner if there is no reply in 15 minutes. Solace Skin Studio and Daniela R. are fictional.
- After-hours remodel. Hold the first text until 8:00 AM, then email the owner if they book a walkthrough. Northline Remodel and Marcus T. are fictional.
- Consult no-show. Text within 10 minutes with two new times, then one follow-up the next morning. Elena V. is fictional.
- Fence quote. Text the next morning, follow up in 2 days if there is no reply, and book a site visit if they say yes. Cedar Line Fencing and Priya S. are fictional.

The branches in the dry run are booked, replied (answered, not booked), no reply, and opt out. The timeline shows the clock time and the channel. Nothing is texted or emailed.

Guardrails stay on the page. Steps the sentence never mentioned stay flagged until a person marks them checked. Publish stays blocked until those steps are checked and a dry run finishes. Version history shows what changed between versions. Rollback puts the previous version back.

The short case study at the top names the problem (slow speed-to-lead), the approach, what a person still decides, and a before and after. That before and after is labeled illustrative. It is not a measured result. The sample month on Results uses the same label. Concept direction. AI-assisted build (Claude, Cursor).

## Checks on this pass

Playwright on local Chrome, reduced motion on, at 1280×800 and 360×740. A control passed if the page changed, a file downloaded, a same-site link returned a successful status, a mailto link was a real address, or the control was already selected. States menus ran after the other controls. Each control was counted once.

**776 passed, 126 flagged, 0 broken requests.** 15 pages × 2 viewports. One page error, on Keel, both widths: confirming a note before the note field was on screen. Relay had no page errors and no console errors. The flags were checked against the pages. None of them was a Relay control that does nothing.

| Page | Desktop passed | Mobile passed | Flagged |
|---|---:|---:|---:|
| Hub | 31 | 31 | 12 on each width |
| Valley Grid | 2 | 2 | 4 desktop, 0 mobile |
| Kestrel | 45 | 45 | 2 on each width |
| Keel | 12 | 13 | 8 desktop, 7 mobile |
| Berth | 31 | 31 | 4 on each width |
| Linden | 45 | 45 | 6 on each width |
| Decision OS | 30 | 30 | 1 on each width |
| Harbor | 24 | 24 | 15 on each width |
| Tidewell | 5 | 5 | 0 |
| Relay | 34 | 34 | 3 on each width |
| AgentProof | 8 | 8 | 0 |
| Estate intake | 24 | 25 | 4 desktop, 3 mobile |
| Signed → Live | 23 | 23 | 2 on each width |
| Lab UI | 59 | 59 | 4 on each width |
| Flare | 14 | 14 | 1 on each width |
| **Total** | **387** | **389** | **126** |

Direct checks on the Relay flags: Zoom in moved the canvas from 77% to 87%, Zoom out moved it back to 77%, and an empty sentence shows "Write what the follow-up should do. Nothing was drafted." Draft the flow, the four examples, Mark checked, the dry run, Check before publish, Mark this version live, Show changes, and Roll back were also run on their own. Rollback restored Cedar Line Fencing as the live version in the demo. Nothing was sent.

The other flags are the same kind as the earlier pass. Hub company type and size leave the screen once the form moves on. Valley Grid's Play, Investigate, and Film mode settle after the crawler's short wait. The phone layout does not show Film mode. Harbor's column sorts and the already-selected filters do not change the page when chosen again. Skip links sit off screen until Tab.

axe-core 4.14 (WCAG 2 A and AA, including WCAG 2.2 AA): **0 violations** on all 15 pages, desktop and mobile. Relay's remodel draft, the blocked publish sheet, the dry run, and the empty version list were checked the same way: 0 violations.

360px: no page scrolls sideways, including Relay after a remodel draft and on the dry run. Relay controls on those screens are at least 44px on both sides. Primary buttons stay at least 44px.

Lighthouse 13.6. Accessibility, best practices, and SEO were **100 on every page, both widths**. Performance, for the record: Relay desktop 100, Relay mobile 98. Harbor desktop was 82, with layout shift about 0.38, on two runs. Harbor mobile was 100. I did not change Harbor. Kestrel is 96 on both widths. The hub, Decision OS, Lab UI, and Flare are 99 on the phone. That is the web font, same as the earlier note.

Screenshots for this pass, desktop 1280×800 and mobile 360×740, are in `weekly-reports/2026-11-23/shots/` with the prefix `relay-case`, `relay-examples`, `relay-spa-flow`, `relay-remodel-flags`, `relay-remodel-flow`, `relay-noshow-flow`, `relay-fence-flow`, `relay-publish-blocked`, `relay-dry-booked`, `relay-dry-replied`, `relay-dry-noreply`, and `relay-version-diff`.

The résumé line is in `weekly-reports/2026-11-23/resume-notes.md`.

The ranked pieces from the October strategy are already on the hub: Relay is the speed-to-lead builder, Signed → Live is the phone onboarding flow, Lab UI is the system, and Flare is the ad-account copilot. The bilingual inbox that was on hold is already a message handoff inside Kestrel. I did not add another piece. Reviewers stop after a few case studies, and a fifth product would sit under work that already covers the ranked gaps.

I improved Relay. It was the highest-ranked piece in the strategy, and it opened on a finished template. The brief asks for a sentence that becomes a flow, low-confidence steps a person can check, a test lead, and a person who publishes, with a version to roll back. The empty state also told you to add steps one by one, and the only button was the template. The hub still led with Valley Grid. That piece is the 3D differentiator. It is not the work the strategy says to put first for automation or onboarding roles. Relay is now the first piece. Signed → Live is next.

AgentProof was not edited.

## Click-through

Playwright on local Chrome, reduced motion on, at 1280×800 and 360×740. A control passed if the page changed, a file downloaded, the clipboard changed, or a link returned a successful status. A control that was already selected and stayed selected also passed. Skip links were checked by keyboard. The States menus ran after the live controls.

Final run, after the changes below: **1,364 passed, 836 flagged, 0 console errors, 0 broken requests.** 15 pages × 2 viewports. The flags were checked by hand. None of them was a control that does nothing. The pass count is lower than 16 November because this crawler counts each control once, and it does not count a control that has already left the screen.

| Page | Desktop passed | Mobile passed | Flagged |
|---|---:|---:|---:|
| Hub | 35 | 35 | 4 on each width |
| Valley Grid | 12 | 12 | 16 desktop, 12 mobile |
| Kestrel | 67 | 67 | 32 on each width |
| Keel | 30 | 30 | 30 on each width |
| Berth | 75 | 75 | 37 on each width |
| Linden | 83 | 83 | 49 on each width |
| Decision OS | 35 | 35 | 31 on each width |
| Harbor | 19 | 19 | 36 on each width |
| Tidewell | 18 | 18 | 4 on each width |
| Relay | 42 | 42 | 55 on each width |
| AgentProof | 8 | 8 | 0 |
| Estate intake | 23 | 23 | 20 on each width |
| Signed → Live | 20 | 20 | 58 on each width |
| Lab UI | 184 | 184 | 9 on each width |
| Flare | 31 | 31 | 39 on each width |
| **Total** | **682** | **682** | **836** |

## Flags checked by hand

- **Hub inquiry options.** Freelance, Website, Meta ads, and Next were flagged because the form moves on as soon as you pick a need, and the crawler was still holding the other choices. A direct run used each need, including Freelance, Website, and Meta ads. Company type and size stay put until Next. An empty Next says to pick a type and a size. The form rejected a one-letter name and a bad email, then opened a mailto to cnavarro.business@gmail.com. Back returned to the previous step. Both widths.
- **Valley Grid.** Film mode, Play, and Investigate were flagged because the crawler lost them while the 3D model was loading or after film mode hid the tools. A direct run toggled Play, opened Investigate (the panel spends about a second on the loading state, then shows the trend and the crew actions), and started film mode. The phone layout does not load the model. Play and All work are on the page. Both widths.
- **Kestrel.** Close step detail, Run to this step, Approve refund, Change amount, and Decline were flagged because the step card leaves the screen when another choice moves the page. A direct run opened the Read ticket step, ran to that step, and closed the card. Both widths.
- **Keel, Berth, and Linden.** The flagged rows are filters and sorts that are already selected, or rows that leave the screen once the list changes. Choosing the current sort again does not change the page.
- **Harbor "Show changed deals only."** The box is hidden until a cleanup is proposed, so the crawler lost it. A direct check, after Clean up stalled deals, cut the table from 14 rows to 6 and left the box checked.
- **Decision OS.** Select none, Select all, and the source rows are on the import screen, not the first screen. Select none clears the selection and says so.
- **Tidewell "See the 4 accounts."** That button is on the June explanation, not the first screen. It opens the four fictional accounts.
- **Relay zoom, Fit, and Reset.** Those were flagged while a draft or a test had moved the canvas. A direct click on a fresh page changed the zoom, fit the canvas, and reset the flow. Draft the flow, the sample sentence, Check before publish, Mark checked, and Roll back were exercised on their own. An empty sentence shows an error and drafts nothing. The sample sentence marks two steps. Publish stays blocked until those steps are checked and a test lead finishes. Rollback restored the previous version. Undo puts the current draft back.
- **Skip links.** Estate intake, Lab UI, and Flare keep the skip link off-screen until it is focused. Tab then Enter lands on the content. Lab UI's target now takes the focus, which it did not do before this week. The mouse timeout is the hidden skip link, not a dead control.
- **Flare "Water heater replacement" and "Diagnosis."** Those are the campaign and the tab that are already selected. Choosing them again does not change the page.
- **Signed → Live.** Reiniciar muestra and the step list were flagged because the page is already in one language and on one step. Switching language changes the labels. The steps that are not current leave the screen when you move on.

## Accuracy

Checked on the hub, every piece, Lab UI, Estate intake, the agent cards, `llms.txt`, and the README.

- Role line is **Concept direction**. Tools line is **AI-assisted build (Claude, Cursor)**. On Relay those two lines stay in English. The new draft bar does not translate them.
- No Blender claim. No claim that Cesar modeled or built the 3D scene by hand. No `/blender` files, and no page links to a `.py` build script.
- No prices on the offers. They still say "Scoped after a short discovery call." Kestrel's `$249` refund, Tidewell's fictional monthly revenue, and Flare's cost-per-lead figures are the demo subject and are labeled as demo.
- No real client names. Relay still uses Solace Skin Studio and Daniela R., both fictional. The new sentence is a sample instruction, not a client.
- Demo data is labeled fictional or sample. The draft says nothing is texted. The sample month on Results is still labeled fictional. It is not a measured outcome.
- The only contact email is **cnavarro.business@gmail.com**. Kestrel's `dana@acmedental.example` is still fictional mail inside the ticket.

## Lighthouse, axe, and 360px

Local Chrome. Lighthouse 13.6. One sequential run. Desktop used the desktop config (form factor desktop, no CPU slowdown). Mobile used the default mobile run (slowdown 4, screen 412). The local preview server does not gzip. GitHub Pages does.

Accessibility, best practices, and SEO were **100 on every page, both widths**. Performance:

| Page | Desktop | Mobile |
|---|---:|---:|
| Hub | 100 | 99 |
| Valley Grid | 100 | 100 |
| Kestrel | 100 | 96 |
| Keel | 100 | 100 |
| Berth | 100 | 100 |
| Linden | 100 | 100 |
| Decision OS | 100 | 100 |
| Harbor | 100 | 100 |
| Tidewell | 100 | 100 |
| Relay | 100 | 98 |
| AgentProof | 100 | 100 |
| Estate intake | 100 | 100 |
| Signed → Live | 100 | 100 |
| Lab UI | 100 | 99 |
| Flare | 100 | 99 |

A first desktop pass of Harbor scored 82 because the layout shift was 0.382. Three quiet runs after that scored 100, and the shift was about 0. The table above uses the quiet run. I did not find a shift I could reproduce by hand.

Kestrel's phone score is 96. Layout shift is about 0. The largest paint is still about 2.7 seconds, which is the brand font on a longer page. Dropping the font would change the design. I did not. Desktop Kestrel is 100 on this run.

axe-core 4.14 (WCAG 2 A and AA, including WCAG 2.2 AA) on the default screen of all 15 pages, desktop and mobile: **0 violations.** Relay's draft, with two steps marked to check, and the blocked publish sheet were checked the same way: 0 violations.

360px: no page scrolls sideways. Every control measured on the first screen is at least 24px on the short side, and every primary button is at least 44px. Relay's checkboxes, which sit on the AI step, are 24px. The new draft, sample, publish, and version buttons are at least 44px.

## What changed, and why

Relay now starts from a sentence. The sample sentence is the one in the October brief: text a new Facebook lead within a minute, offer two times, and tell the owner if there is no reply in 15 minutes. Draft the flow turns that into the existing ten-step flow. It sets the first text to within 60 seconds and the wait to 15 minutes, which the wait list can now hold. Steps the sentence never mentions stay marked. On that sample, those are the opt-out line and quiet hours. The draft kept both. Mark checked clears one step, and undo puts the mark back.

Check before publish lists what is still open. It stays blocked until the marked steps are checked and a test lead has finished. Nothing is texted. Mark this version live saves the version in this browser. Versions can roll back. Reset flow clears the live mark and can be undone.

The empty state no longer says you can add steps one by one. That button was not there. It now says to describe the follow-up, or to use the template.

The case study names what was rejected: a chat box that hides the flow, and marking the draft live as soon as it appears. It also says this was not tested with shop owners.

The hub leads with Relay, then Signed → Live, then Lab UI, Kestrel, and Valley Grid. The README table follows that order. Lab UI's approval note now includes Relay's publish check.

Primary buttons that measured 40px tall now have a 44px minimum. That was Kestrel's Run agent, Decision OS's Import sample export, Harbor's Clean up stalled deals, and Tidewell's Explain June. The same minimum is on the other pieces so a primary button that is not on the first screen still meets it. Relay's three checkboxes went from 16px to 24px. Lab UI's skip link now moves focus to the content.

## Left unfixed, and why

- **Kestrel's phone performance at 96, Relay's phone at 98, and the hub, Lab UI, and Flare at 99.** The web font and the photos. Layout shift is about 0. Dropping the brand font would change the design.
- **Harbor's one noisy desktop run at 82.** It did not repeat. Three later runs were 100.
- **No sessions with real users, including no shop owners and no Spanish-first speakers.** The pages say so. The new draft makes no claim about a real texting campaign or a measured booked rate.
- **The live GitHub Pages site.** This is a draft. `main` is unchanged.

## For the résumé and LinkedIn

The short version is in `weekly-reports/2026-11-23/resume-notes.md`.

## Screenshots

Desktop is 1280px wide. Mobile is 360px wide.

- `weekly-reports/2026-11-23/shots/hub-desktop.png`
- `weekly-reports/2026-11-23/shots/hub-mobile.png`
- `weekly-reports/2026-11-23/shots/relay-desktop.png`
- `weekly-reports/2026-11-23/shots/relay-mobile.png`
- `weekly-reports/2026-11-23/shots/relay-publish-desktop.png`
- `weekly-reports/2026-11-23/shots/relay-publish-mobile.png`
