# Weekly review · 16 November 2026

This branch continues draft PR #11 (9 November, unmerged). It is a new draft that includes the 19 October, 26 October, 2 November, and 9 November work, plus this week. It does not replace pull request #10. Nothing here is merged. `main` is unchanged. Cesar publishes.

The ranked pieces already on the hub still pass the checklist from the last reviews. The bilingual inbox that was on hold as its own piece is now a message handoff inside Kestrel. AgentProof was not edited.

## Click-through

Playwright on local Chrome, reduced motion on, at 1280×800 and 360×740. A control passed if the page changed, a file downloaded, the clipboard changed, or a link returned a successful status. A control that was already selected and stayed selected also passed. Skip links were checked by keyboard. The States menus ran after the live controls.

Final run, after the Kestrel fix below: **2,530 passed, 1,097 flagged, 0 console errors, 0 broken requests.** 15 pages × 2 viewports. The flags were checked by hand. One of them was a real miss, and it is fixed. The rest are not dead controls.

| Page | Desktop passed | Mobile passed | Flagged |
|---|---:|---:|---:|
| Hub | 44 | 44 | 14 on each width |
| Valley Grid | 20 | 10 | 21 desktop, 5 mobile |
| Kestrel | 144 | 147 | 48 desktop, 45 mobile |
| Keel | 147 | 132 | 8 desktop, 15 mobile |
| Berth | 101 | 90 | 64 desktop, 63 mobile |
| Linden | 135 | 133 | 72 desktop, 74 mobile |
| Decision OS | 77 | 76 | 31 desktop, 35 mobile |
| Harbor | 84 | 86 | 81 desktop, 79 mobile |
| Tidewell | 47 | 47 | 42 on each width |
| Relay | 79 | 32 | 37 desktop, 62 mobile |
| AgentProof | 9 | 9 | 0 |
| Estate intake | 88 | 88 | 26 on each width |
| Signed → Live | 51 | 46 | 62 desktop, 67 mobile |
| Lab UI | 207 | 207 | 7 on each width |
| Flare | 75 | 75 | 25 on each width |
| **Total** | **1,308** | **1,222** | **1,097** |

The flag count is higher than 9 November because this crawler records a control that leaves the screen when another choice moves the page. Those are listed below. They are not extra failures.

## Flags checked by hand

- **Hub inquiry options.** Freelance, Website, Meta ads, This month, Just exploring, Not sure yet, and the role types were flagged because the form moves on as soon as you pick one, and the crawler was still holding the other choices. A direct run used each of those choices. Company type and size stay put until Next. The form reached the contact step, rejected an empty name and a bad email, and then opened a mailto to cnavarro.business@gmail.com. Back returned to the previous step. Both widths.
- **Valley Grid desktop.** Film mode, Play, and the States menu were flagged because the crawler lost the controls while the 3D model was loading. A direct run changed the crew from Crew 4 to Crew 2. Acknowledge and Escalate each opened their confirm. Empty cleared the alerts. Play switched its label. Film mode showed its toast. The phone layout does not load the model. Its one flag was the same crew radio, and a direct click selected Crew 2.
- **Kestrel Keep as draft, before the fix.** During the five-second send countdown the step card still showed Keep as draft, and that click did nothing. The step card now shows the countdown, and a Keep click during the countdown undoes the send. The re-run passed Keep as draft. Both widths. The other Kestrel flags are the refund choices and the inbox threads that leave the screen once you pick one. Approve and send, Confirm, Don't send, Cancel, Export, the language buttons, and the filters all passed on the re-run.
- **Keel "Needs a touch" on the save-error screen.** The select was flagged because the list did not change in the trace the crawler held. A direct change set the filter to Needs a touch.
- **Harbor "Show changed deals only."** A direct check, after the cleanup ran, cut the table from 14 rows to 6 and left the box checked.
- **Relay "Never replies."** A direct click on the Test run tab selected that scenario.
- **Decision OS lanes on the file-error screen.** The crawler clicked while the import was still moving. After it settled, the page said the file did not open and nothing was imported. A lane click still showed only that lane.
- **Estate intake checkbox.** Checking "I reviewed this draft" sticks. The skip link is off-screen until it is focused. Tab then Enter on Lab UI lands on the content. The same pattern is the Flare skip link. Those timeouts are the hidden skip link, not a dead control.
- **Flare "Water heater replacement" and "Diagnosis" on the approve-error screen.** Those are the campaign and the tab that are already selected. Choosing them again does not change the page.

## Accuracy

Checked on the hub, every piece, Lab UI, Estate intake, the agent cards, and the README.

- Role line is **Concept direction**. Tools line is **AI-assisted build (Claude, Cursor)**. On Kestrel those two lines stay in English when a draft is in Spanish.
- No Blender claim. No claim that Cesar modeled or built the 3D scene by hand. No `/blender` files, and no page links to a `.py` build script.
- No prices on the offers. They still say "Scoped after a short discovery call." Kestrel's `$249` refund, Tidewell's fictional monthly revenue, and Flare's cost-per-lead figures are the demo subject and are labeled as demo.
- No real client names. The new Kestrel threads use Marisol Vega at Acme Dental, Jonah Hale at Bright Smile Studio, Elena Ruiz at Acme Dental, and Noah Patel as the fictional teammate. Ledgerly is the same fictional company as the refund ticket.
- Demo data is labeled fictional or sample. The message handoff says the people and the messages are made up, and that nothing leaves the browser.
- The only contact email is **cnavarro.business@gmail.com**. Kestrel's `dana@acmedental.example` is still fictional mail inside the ticket.
- Estate intake's public agent card and OpenAPI summary said "pre-appraisal." The page and `llms.txt` already said this is not an appraisal. Those two files now say "intake sheet," and they still say this is not an appraisal.

## Lighthouse, axe, and 360px

Local Chrome. Lighthouse 13.6. One sequential run, desktop preset and the default mobile run. The local preview server does not gzip. GitHub Pages does.

Accessibility, best practices, and SEO were **100 on every page, both widths**. Performance:

| Page | Desktop | Mobile |
|---|---:|---:|
| Hub | 99 | 99 |
| Valley Grid | 100 | 100 |
| Kestrel | 95 | 96 |
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

Berth's desktop score last week was 77 because the brand font reflowed the book. The font is still Hanken Grotesk. It is preloaded, `font-display` is `optional`, and the fallback is width-matched, so a late font does not move the book. This run is 100 and 100, and the layout shift is 0.

A quiet rerun of Kestrel alone was 95 and 95. Layout shift is about 0. The largest paint is still about 2.7 seconds, which is the brand font on a longer page. Dropping the font would change the design. I did not.

axe-core 4.14 (WCAG 2 A and AA) on the default screen of all 15 pages, desktop and mobile: **0 violations.** Kestrel's confirm sheet, the empty inbox, and the English draft were checked the same way: 0 violations.

360px: no page scrolls sideways. Every control measured on the page is at least 24px on the short side. The new handoff buttons are at least 44px.

## What changed, and why

Kestrel's "Hand off to a person" was a toast that cleared the queue. That was the weakest moment I could change. The refund run is still there. Under it, a message handoff holds three fictional threads, two on WhatsApp and one on Messenger. The customer's words stay in the language they used. The draft can be read in English or Spanish. The rest of the console, including Concept direction and AI-assisted build (Claude, Cursor), stays in English.

Nothing is marked sent until a person confirms. Confirm says it is only marked sent in the demo, and Undo puts the thread back. Don't send, and Hand to Noah, work the same way and can be undone. Copy and export stay on the page. The export says the file is fictional. The first send can be set to fail once, and the draft remains. Empty and loading are in the Inbox menu. If the refund run stops because billing does not answer, Hand off to a person opens Marisol's thread and does not send anything.

The case study says what was rejected: sending the chat reply from the model, hiding the other language, and a separate inbox product.

## Left unfixed, and why

- **Kestrel performance at 95.** The brand font on the longer page. Layout shift is about 0. The phone batch was 96 and the quiet rerun was 95.
- **Relay at 98, and the hub, Lab UI, and Flare at 99.** The web font and the photos. Same call as the last report.
- **No sessions with real users, including no Spanish-first speakers.** The pages say so. The new threads make no claim about a real support team or a real chat channel.
- **The live GitHub Pages site.** This is a draft. `main` is unchanged.

## For the résumé and LinkedIn

Plain version, only what this branch adds on the site:

- Directed a message handoff inside the Kestrel concept. Three fictional threads, on WhatsApp and Messenger, keep the customer's language. A draft can be shown in English or Spanish. A person confirms before the demo marks it sent, and undo puts it back. Concept direction. AI-assisted build (Claude, Cursor). Not a client result, and not a live chat channel.
- The refund run is still on the same page. A stopped billing check opens the message instead of clearing the queue. Nothing is emailed.
- It is concept work. The customers and the messages are made up. The only contact is cnavarro.business@gmail.com.

## Screenshots

Desktop is 1280px wide. Mobile is 360px wide.

- `weekly-reports/2026-11-16/shots/hub-desktop.png`
- `weekly-reports/2026-11-16/shots/hub-mobile.png`
- `weekly-reports/2026-11-16/shots/kestrel-desktop.png`
- `weekly-reports/2026-11-16/shots/kestrel-mobile.png`
- `weekly-reports/2026-11-16/shots/kestrel-approve-desktop.png`
- `weekly-reports/2026-11-16/shots/kestrel-approve-mobile.png`
- `weekly-reports/2026-11-16/shots/berth-desktop.png`
- `weekly-reports/2026-11-16/shots/berth-mobile.png`
