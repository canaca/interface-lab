# Weekly review · 26 October 2026

This branch continues draft PR #7 (19 October, unmerged). It adds **Lab UI**, the shared system behind the pieces, and it fixes the gaps the accessibility pass found. Valley Grid's 3D model still exists. It now loads when you ask, so the alert panel is ready first.

Nothing here is merged. `main` is unchanged. Cesar publishes.

## Click-through

Playwright on local Chrome, reduced motion on, at 1280×800 and 360×740. Every visible control was used: buttons, tabs, radios, filters, search, selects, exports, file fields, and the multi-step flows. A control passed only if the page changed (text, state, toast, download, or the field value). A control that was already selected and stayed selected also passed. Links to other pages were requested and had to return a successful status. The States menu ran after the live controls, so empty, loading, and error screens were included.

A control is counted once for its name, its place on the page, and its row. The same action is not counted again.

Final run: **1,447 passed, 0 failed, 0 console errors, 0 broken requests.** 14 pages × 2 viewports.

| Page | Desktop passed | Mobile passed | Failed |
|---|---:|---:|---:|
| Hub | 31 | 31 | 0 |
| Valley Grid | 13 | 16 | 0 |
| Kestrel | 55 | 55 | 0 |
| Keel | 74 | 74 | 0 |
| Berth | 57 | 57 | 0 |
| Linden | 75 | 75 | 0 |
| Decision OS | 78 | 78 | 0 |
| Harbor | 76 | 76 | 0 |
| Tidewell | 25 | 25 | 0 |
| Relay | 23 | 23 | 0 |
| AgentProof | 8 | 8 | 0 |
| Estate intake | 7 | 7 | 0 |
| Signed → Live | 55 | 55 | 0 |
| Lab UI | 145 | 145 | 0 |
| **Total** | **722** | **725** | **0** |

Counts are lower than the 19 October report on some pages because this crawler does not count the same control twice. Relay's 23 is the canvas steps, the zoom controls, and the inspector that is open on the first step. Choosing another step replaces that inspector. Decision OS's 78 includes the sample import, the duplicate choice, the lenses, and the chart.

## Failures found, and what fixed them

These were real, and the retest is in the table above.

- **Valley Grid crashed after the 3D model loaded.** The camera position was a plain stand-in until Three.js arrived, and the new frame called `.copy` on it. The console error was `camPos.copy is not a function`. The play control also said "Pause" while reduced motion had already stopped the clock, so a click did not change the label. The model load now builds real camera vectors, and the play label is set from whether time is actually moving. Retest: 13 passed on desktop, 16 on mobile, no console errors. The alert panel works before the model loads. Load 3D model and Film mode both bring the model in. The toast says the model loaded.
- **Relay showed a fake phone number**, `(555) 010-4477`, on the demo handset. The line now says "demo line · not a real number". No digits.
- **Small dim text failed contrast.** `#7F6B5B` on the page background was 3.80:1. It is now `#A38B78` (5.96:1 on the page, 4.90:1 on a panel), including the Valley Grid and Tidewell chart labels that were hard-coded. Decision OS's unrecognized lane was `#6B7383` at 4.11:1 on its ink background. It is now `#8E97A6` (6.65:1 on the page, 6.32:1 on a row).
- **Focus and reduced motion did not match.** Several pages used a 1px focus ring, and a few fields removed the outline. The ring is 2px, including those fields. Linden and Berth only stopped the skeleton, the spinner, and the toast when the system asks for less motion. They now stop animation and transitions the same way the other pieces do.

Two crawler reports were not product bugs. Decision OS's "Keep only the second" radio re-renders the list, so the first script lost the input and called it a no-effect. Clicking it directly selects it and the button becomes "Add 11 items to state". The retest, which looks the radio up again by name, is 78 passed and 0 failed on both widths. Valley Grid's time slider was reported with no box while the page was busy loading the model. The slider has a 52px hit area at rest, and the retest passed.

## Accuracy

Checked on the hub, every piece, Lab UI, the README, and the case-study files.

- Role line is **Concept direction**. Tools line is **AI-assisted build (Claude, Cursor)**.
- No Blender claim. No claim that Cesar modeled or built the 3D scene by hand. The README still says he did not model it by hand.
- No prices on the offers. They still say "Scoped after a short discovery call." Kestrel's `$249` refund and Tidewell's fictional monthly revenue are the demo subject, as the 12 October notes kept. Lab UI's `$249` is labeled demo and is the same fictional refund.
- No real client names. Shops in the demos are fictional (Acme Dental, Northwind Heating, Blue Finch Roofing, and the others). Linden still names Cesar's own GIA credentials and his time at Talisman Collection Fine Jewelers. That is his background, and the page says it is not a client engagement. "Diamond Grader" does not appear.
- Demo data is labeled fictional or sample on the pieces. Lab UI's banner says the shops, people, and amounts are fictional.
- The only contact email is **cnavarro.business@gmail.com**. Kestrel's `dana@acmedental.example` is fictional mail inside the ticket.
- No phone numbers.

## Lighthouse, axe, and 360px

Local Chrome, Lighthouse 12.8, desktop preset and the default mobile run. Performance / accessibility / best practices / SEO. The local preview server does not gzip. GitHub Pages does. Accessibility, best practices, and SEO were **100 on every page, both widths, before and after**. Lab UI is new, so it has no before score.

| Page | Viewport | Perf before | Perf after |
|---|---|---:|---:|
| Hub | desktop | 84 | 84 |
| Hub | mobile | 84 | 84 |
| Valley Grid | desktop | 100 | 99 |
| Valley Grid | mobile | 100 | 99 |
| Kestrel | desktop | 92 | 92 |
| Kestrel | mobile | 92 | 92 |
| Keel | desktop | 93 | 93 |
| Keel | mobile | 93 | 93 |
| Berth | desktop | 93 | 93 |
| Berth | mobile | 93 | 93 |
| Linden | desktop | 93 | 93 |
| Linden | mobile | 93 | 93 |
| Decision OS | desktop | 90 | 90 |
| Decision OS | mobile | 90 | 90 |
| Harbor | desktop | 93 | 93 |
| Harbor | mobile | 93 | 93 |
| Tidewell | desktop | 93 | 93 |
| Tidewell | mobile | 93 | 93 |
| Relay | desktop | 90 | 90 |
| Relay | mobile | 90 | 90 |
| AgentProof | desktop | 100 | 100 |
| AgentProof | mobile | 100 | 100 |
| Estate intake | desktop | 100 | 100 |
| Estate intake | mobile | 100 | 100 |
| Signed → Live | desktop | 100 | 100 |
| Signed → Live | mobile | 100 | 100 |
| Lab UI | desktop | — | 92 |
| Lab UI | mobile | — | 92 |

These scores are not the same scale as the 19 October report. That run scored the hub at 99 desktop and Valley Grid desktop at 59, with best practices at 0, because Three.js and the model blocked the main thread inside the trace. This week's before trace for Valley Grid finished without that work in the metric window (performance 100, total blocking time 0). A separate timed load of the old page still downloaded **5.6 MB** before any click: Three.js plus `t2.json` (2.5 MB) and `board.json` (1.5 MB). The new page's first load is **0.28 MB**. Three.js, `t2.glb`, and `board.glb` start only after Load 3D model, the poster, or Film mode. The model is still the interface once it loads. Phones still skip it. The GLB files replace the base64 JSON, so the repo is not carrying both.

Tidewell desktop and Relay desktop each had one noisy run (74 and 62) from the web font and a slow largest paint. Repeat runs on the same files scored 93 and 90, matching the before scores. Those are the numbers in the table. Linden and Kestrel stay where the font leaves them. Switching the brand font off would be a design change.

axe-core 4.10 (WCAG 2 A/AA) after the fixes: **0 violations on all 14 pages, desktop and mobile.**

360px: no page scrolls sideways. Every control on the page, not only the first screen, is at least 24px on the short side. The pieces already aim for 44px. Relay's flow canvas still scrolls inside its own region on a phone. The page itself does not.

## Lab UI

New piece at `lab-ui/`. It is on the hub and in the README. Role: Concept direction. Tools: AI-assisted build (Claude, Cursor). No 3D. A Figma mirror is described as planned and not built. There is no claim of a Figma library.

Case study line: concepts were built fast with AI and didn't match. One system was extracted, the accessibility gaps were fixed, and the pieces were aligned on it.

Tokens: color with the contrast ratio next to each one, a type scale from 12 to 40, spacing from 4 to 48, radius 8 / 12 / 18 / pill, and motion at 120 / 200 / 360ms. When the system asks for less motion, those durations are 0.

Fourteen components, each with when to use it, when not to, the pieces that already use it, the keyboard behavior, and a live demo. Every demo control is in the click-through above (Lab UI 145 / 0 on each width). States covered: default, hover, focus, disabled, loading, error, empty.

1. Status chip
2. Approval card
3. Change preview, before and after
4. Undo toast
5. Sortable data table, with search, empty state, and a sample CSV
6. Step tracker
7. AI confidence badge, in words, not a percent
8. Error banner with a plain-language fix. The first retry fails on purpose. The second clears it.
9. English / Spanish toggle. The role and tools lines stay in English.
10. Loading skeleton
11. Field with a plain error
12. Segmented control
13. Conflict flag
14. Reminder that stays on the page and is not sent

The page also publishes the accessibility audit: contrast, focus, reduced motion, and keyboard, with the before and after values above.

## Left unfixed, and why

- **Hub performance 84, Lab UI 92, and a few pieces in the low 90s.** Render-blocking fonts and full-size photos. Last week's note still holds for Linden and Kestrel: reserving height did not remove the font shift, and dropping the brand font would change the design.
- **Valley Grid's model is one click away on a wide screen.** That is the point of the change. Lighthouse scores the first load, which no longer downloads the model. The piece is still there.
- **This was not tested with real operators, shop owners, or Spanish-first speakers.** The pages say so.
- **The live GitHub Pages site.** This is a draft. `main` is unchanged.

## For the résumé and LinkedIn

Plain version, only what this branch actually adds:

- Directed Lab UI, the shared system behind Interface Lab: checked color contrast, type, spacing, and 14 components taken from the live prototypes, each with working empty, loading, and error states.
- The concepts had been built fast with AI and didn't match. I extracted one system, fixed the contrast, focus, and reduced-motion gaps, and aligned the pieces on it. Concept direction. AI-assisted build (Claude, Cursor). A Figma library is planned, not built.
- Valley Grid's 3D transformer now loads when you ask, so the alert workflow is on screen first. The model is still the interface after that click.
- The only contact is cnavarro.business@gmail.com. Offers have no prices. The shops and numbers in the prototypes are fictional.
- It is concept direction, not a shipped design system, and it was not tested with a team.

## Screenshots

Desktop is 1280px wide. Mobile is 360px wide.

- `weekly-reports/2026-10-26/shots/hub-desktop.png`
- `weekly-reports/2026-10-26/shots/hub-mobile.png`
- `weekly-reports/2026-10-26/shots/valley-grid-desktop.png`
- `weekly-reports/2026-10-26/shots/valley-grid-mobile.png`
- `weekly-reports/2026-10-26/shots/kestrel-desktop.png`
- `weekly-reports/2026-10-26/shots/kestrel-mobile.png`
- `weekly-reports/2026-10-26/shots/keel-desktop.png`
- `weekly-reports/2026-10-26/shots/keel-mobile.png`
- `weekly-reports/2026-10-26/shots/berth-desktop.png`
- `weekly-reports/2026-10-26/shots/berth-mobile.png`
- `weekly-reports/2026-10-26/shots/linden-desktop.png`
- `weekly-reports/2026-10-26/shots/linden-mobile.png`
- `weekly-reports/2026-10-26/shots/decision-os-desktop.png`
- `weekly-reports/2026-10-26/shots/decision-os-mobile.png`
- `weekly-reports/2026-10-26/shots/harbor-desktop.png`
- `weekly-reports/2026-10-26/shots/harbor-mobile.png`
- `weekly-reports/2026-10-26/shots/tidewell-desktop.png`
- `weekly-reports/2026-10-26/shots/tidewell-mobile.png`
- `weekly-reports/2026-10-26/shots/relay-desktop.png`
- `weekly-reports/2026-10-26/shots/relay-mobile.png`
- `weekly-reports/2026-10-26/shots/agentproof-desktop.png`
- `weekly-reports/2026-10-26/shots/agentproof-mobile.png`
- `weekly-reports/2026-10-26/shots/estate-intake-desktop.png`
- `weekly-reports/2026-10-26/shots/estate-intake-mobile.png`
- `weekly-reports/2026-10-26/shots/signed-desktop.png`
- `weekly-reports/2026-10-26/shots/signed-mobile.png`
- `weekly-reports/2026-10-26/shots/lab-ui-desktop.png`
- `weekly-reports/2026-10-26/shots/lab-ui-mobile.png`
