# Weekly review · 2 November 2026

This branch continues draft PR #8 (26 October, unmerged). It adds **Flare**, an ad-account copilot, and takes Tidewell off the hub. Tidewell is still at `tidewell/`. Nothing here is merged. `main` is unchanged. Cesar publishes.

## Click-through

Playwright on local Chrome, reduced motion on, at 1280×800 and 360×740. Every control the crawler could see was used: buttons, tabs, radios, filters, search, selects, exports, and the multi-step flows. A control passed if the page changed (text, state, toast, or a field), a file downloaded, or the clipboard changed. A control that was already selected and stayed selected also passed. Links to other pages had to return a successful status. The States menu ran after the live controls.

A control is counted once for its name and its place on the page. The same action is not counted again. Some rows below are lower than the 26 October report because this crawler does not count a control twice, and it does not count a control that had already left the screen.

Final automated run: **1,366 passed, 5 flagged, 0 console errors, 0 broken requests.** 15 pages × 2 viewports. After the fixes and the rechecks below, there is no open product failure.

| Page | Desktop passed | Mobile passed | Flagged |
|---|---:|---:|---:|
| Hub | 58 | 58 | 0 |
| Valley Grid | 15 | 13 | 0 |
| Kestrel | 48 | 48 | 0 |
| Keel | 65 | 65 | 0 |
| Berth | 61 | 61 | 0 |
| Linden | 61 | 61 | 0 |
| Decision OS | 45 | 45 | 0 |
| Harbor | 26 | 26 | 0 |
| Tidewell | 46 | 46 | 1 |
| Relay | 36 | 36 | 1 |
| AgentProof | 9 | 9 | 0 |
| Estate intake | 8 | 8 | 0 |
| Signed → Live | 40 | 40 | 0 |
| Lab UI | 138 | 139 | 1 on desktop |
| Flare | 29 | 26 | 0 |
| **Total** | **685** | **681** | **5** |

Valley Grid's desktop count includes Load 3D model and Film mode. The phone layout does not show Load 3D model. Relay's 36 is the canvas, the zoom controls, and the inspector that is open on the first step.

## Failures found, and what fixed them

These were real, and they are in the table above as already fixed (Keel, Berth) or rechecked (the five flags).

- **Keel "Open" did nothing if that account was already open.** The button now says the account is already open. Final crawl: 65 passed, 0 failed, both widths.
- **Berth "Start" on a later step only used a toast.** A second Start could look idle if that toast was still up. The reason is now written on that step: the earlier step is still open. Final crawl: 61 passed, 0 failed, both widths.
- **Lab UI "Save sample name" did nothing useful when the name was empty.** The field was marked required, so the browser blocked the submit and the message under the field never appeared. The form now lets the script run, and an empty save says to enter at least 2 characters. Nothing is saved. A direct click after the fix shows that message, then a real name saves on the page. The mobile crawl ran after the fix: 139 passed, 0 failed. The desktop flag in the table is from the crawl that ran before the fix.
- **Tidewell's June bar was flagged because the chart had just been redrawn** and the crawler was holding the old node. A direct click on June opens the churn explanation, including the four accounts. It is not a dead control. Both widths.
- **Relay's "Flow" tab was already selected.** Choosing it again does not change the page. A retest that treats an already selected tab as a pass is 37 passed, 0 failed, both widths.

Flare's crawler count is the controls it reached before it switched to a quiet campaign. The approval path was walked on purpose at both widths after that: pause and confirm, change the daily move, ask Mateo and confirm, file the creative request and confirm, copy the note (five lines), export the note, mark it ready, undo, the owner's approve and the owner's "Don't move it", Spanish, the empty state, the file error (first retry fails, second loads), and the approve error (first confirm fails, second saves). All of those changed the page. 0 console errors. No sideways scroll at 360px.

## Accuracy

Checked on the hub, every piece including Flare and Tidewell, Lab UI, and the README.

- Role line is **Concept direction**. Tools line is **AI-assisted build (Claude, Cursor)**. On Flare those two lines stay in English when the note to the owner is in Spanish.
- No Blender claim. No claim that Cesar modeled or built the 3D scene by hand.
- No prices on the offers. They still say "Scoped after a short discovery call." Kestrel's `$249` refund, Tidewell's fictional monthly revenue, and Flare's cost-per-lead figures are the demo subject. Flare says the numbers are made up.
- No real client names. Flare uses Mesa Local, the same fictional agency as Signed → Live, and Solano Plumbing, a fictional shop. Mateo Solano and Camila R. are fictional. Linden still names Cesar's own GIA credentials and his time at Talisman Collection Fine Jewelers. "Diamond Grader" does not appear.
- Demo data is labeled fictional or sample. Flare's banner says the agency, the shop, the people, and the numbers are made up, and that nothing changes a real ad account.
- The only contact email is **cnavarro.business@gmail.com**. Kestrel's `dana@acmedental.example` is fictional mail inside the ticket.
- No phone numbers. Flare's form fields are name, city, and what is going on. It does not show a number.

## Lighthouse, axe, and 360px

Local Chrome. Lighthouse 13.6 (last week's report was 12.8, so the scores are not on the same scale). Desktop preset and the default mobile run. Performance / accessibility / best practices / SEO. The local preview server does not gzip. GitHub Pages does.

Accessibility, best practices, and SEO were **100 on every page, both widths**. A clean performance run, with no other browser work in the way:

| Page | Desktop | Mobile |
|---|---:|---:|
| Hub | 99 | 99 |
| Valley Grid | 100 | 100 |
| Kestrel | 95 | 95 |
| Keel | 100 | 100 |
| Berth | 100 | 100 |
| Linden | 100 | 100 |
| Decision OS | 100 | 100 |
| Harbor | 100 | 100 |
| Tidewell | 100 | 100 |
| Relay | 98 | 98 |
| AgentProof | 100 | 100 |
| Estate intake | 100 | 100 |
| Signed → Live | 100 | 100 |
| Lab UI | 99 | 99 |
| Flare | 99 | 99 |

The hub's clean runs are 99 and 99. Last week's write-up had 84. A batch run of every page, while another browser was still busy, scored the hub desktop at 88 and then the clean runs returned to 99. The hero photo is preloaded. The brand font is still there. Kestrel stays at 95 because the largest paint is the photo plus that font (about 2.8s in this trace). Dropping the font would change the design.

axe-core 4.14 (WCAG 2 A and AA) on the default screen of all 15 pages, desktop and mobile: **0 violations.** Flare's changes screen, the pause confirm, the owner screen, and the Spanish note were checked the same way: 0 violations.

360px: no page scrolls sideways. Every control measured on the page, not only the first screen, is at least 24px on the short side. The pieces aim for 44px.

## Flare

New piece at `flare/`. It is on the hub, in the place Tidewell had, and in the README. Tidewell is not on the hub. The page is still at `tidewell/`. Role: Concept direction. Tools: AI-assisted build (Claude, Cursor). No 3D. The chart is flat.

Case study line: when lead costs spike, owners panic and agencies guess. The copilot shows its evidence, separates diagnosis from action, and never moves budget without approval.

It is one fictional alert, on one campaign, for Camila at Mesa Local and Mateo at Solano Plumbing. Made-up numbers. Cost per lead goes from $22 to $61. Spend stays $671. Leads fall from 31 to 11.

- The other two campaigns are quiet, so a normal week is not treated as an emergency.
- Diagnosis ranks four checks: creative fatigue (high), lead quality in the CRM (medium), audience overlap (medium), and the landing page and form (low, ruled down). Each one shows the demo rows it used. Confidence is a word, not a percent. A list says what the file did not contain.
- Three proposed changes, each previewed, each confirmed by a person, each undoable. Pause the tired photo and keep the other one running. Move budget only inside the cap Mateo set. File a request for new photos on the page. The budget does not move until Mateo approves it. He can also say no.
- The note to Mateo is five lines, in English or Spanish. Camila can edit it. If she has edited it, switching language asks before it replaces her text. Copy and export work. Mark ready stays on the page. Nothing is emailed.

Empty, loading, a delivery-file error, and an approve error are in the States menu. The file error fails once on purpose, then loads. The approve error fails once, then saves. Reset demo clears the browser save.

## Left unfixed, and why

- **Kestrel at 95, Relay at 98, and the hub, Lab UI, and Flare at 99.** The web font and the photos. Last week's note still holds: dropping the brand font would change the design. The hub's hero image is preloaded. That did not move a clean run off 99.
- **This was not tested with account managers, shop owners, or Spanish-first speakers.** The pages say so. Flare makes no claim about a real ad account.
- **The live GitHub Pages site.** This is a draft. `main` is unchanged. Tidewell is still on the live site until Cesar publishes.

## For the résumé and LinkedIn

Plain version, only what this branch actually adds:

- Directed Flare, a concept copilot for when a fictional shop's cost per lead spikes. The account manager sees the checks ranked, each one tied to the demo rows, with confidence in words and a list of what the file did not contain. Pausing an ad, asking for new photos, and moving budget are separate. Budget cannot pass a cap the owner set, and it does not move until the owner approves. The note to the owner is five lines, in English or Spanish, and copy and export work. Concept direction. AI-assisted build (Claude, Cursor). Not a client result, and not tested with a real account team.
- Tidewell remains in the portfolio repo and is no longer on the front page.
- It is concept work. The shops and the numbers are made up. The only contact is cnavarro.business@gmail.com.

## Screenshots

Desktop is 1280px wide. Mobile is 360px wide.

- `weekly-reports/2026-11-02/shots/hub-desktop.png`
- `weekly-reports/2026-11-02/shots/hub-mobile.png`
- `weekly-reports/2026-11-02/shots/valley-grid-desktop.png`
- `weekly-reports/2026-11-02/shots/valley-grid-mobile.png`
- `weekly-reports/2026-11-02/shots/kestrel-desktop.png`
- `weekly-reports/2026-11-02/shots/kestrel-mobile.png`
- `weekly-reports/2026-11-02/shots/keel-desktop.png`
- `weekly-reports/2026-11-02/shots/keel-mobile.png`
- `weekly-reports/2026-11-02/shots/berth-desktop.png`
- `weekly-reports/2026-11-02/shots/berth-mobile.png`
- `weekly-reports/2026-11-02/shots/linden-desktop.png`
- `weekly-reports/2026-11-02/shots/linden-mobile.png`
- `weekly-reports/2026-11-02/shots/decision-os-desktop.png`
- `weekly-reports/2026-11-02/shots/decision-os-mobile.png`
- `weekly-reports/2026-11-02/shots/harbor-desktop.png`
- `weekly-reports/2026-11-02/shots/harbor-mobile.png`
- `weekly-reports/2026-11-02/shots/tidewell-desktop.png`
- `weekly-reports/2026-11-02/shots/tidewell-mobile.png`
- `weekly-reports/2026-11-02/shots/relay-desktop.png`
- `weekly-reports/2026-11-02/shots/relay-mobile.png`
- `weekly-reports/2026-11-02/shots/agentproof-desktop.png`
- `weekly-reports/2026-11-02/shots/agentproof-mobile.png`
- `weekly-reports/2026-11-02/shots/estate-intake-desktop.png`
- `weekly-reports/2026-11-02/shots/estate-intake-mobile.png`
- `weekly-reports/2026-11-02/shots/signed-desktop.png`
- `weekly-reports/2026-11-02/shots/signed-mobile.png`
- `weekly-reports/2026-11-02/shots/lab-ui-desktop.png`
- `weekly-reports/2026-11-02/shots/lab-ui-mobile.png`
- `weekly-reports/2026-11-02/shots/flare-desktop.png`
- `weekly-reports/2026-11-02/shots/flare-mobile.png`
- `weekly-reports/2026-11-02/shots/flare-changes-desktop.png`
- `weekly-reports/2026-11-02/shots/flare-changes-mobile.png`
- `weekly-reports/2026-11-02/shots/flare-confirm-desktop.png`
- `weekly-reports/2026-11-02/shots/flare-owner-desktop.png`
- `weekly-reports/2026-11-02/shots/flare-owner-mobile.png`
- `weekly-reports/2026-11-02/shots/flare-spanish-desktop.png`
- `weekly-reports/2026-11-02/shots/flare-spanish-mobile.png`
- `weekly-reports/2026-11-02/shots/flare-empty-desktop.png`
- `weekly-reports/2026-11-02/shots/flare-error-desktop.png`
