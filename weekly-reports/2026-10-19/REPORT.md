# Interface Lab weekly review — 19 October 2026

Draft only. This branch is not published. GitHub Pages still serves `main` until Cesar says to merge.

## What changed

The interactive pieces already on the hub were solid once three loading-state filters told the truth. The one addition is **Signed → Live**, the next piece from the October strategy that was not built yet. Speed-to-lead is already Relay. Signed → Live is not Berth: Berth is a desktop checklist for the fictional software company Fieldnote. Signed → Live is the shop owner's phone, for the fictional agency Mesa Local, in English and Spanish, plus an agency desk.

## Click-through

Playwright (desktop Chrome), 1280×800 and 360×740, reduced motion on. Every visible button, link, tab, select, field, slider, and file input was exercised. A control passed only when the page changed (text, toast, field, download, or an already-selected control that stays selected). Final run: **1,385 controls, 0 failures, 0 console errors, 0 broken requests**, 13 pages × 2 viewports.

| Page | Desktop pass | Mobile pass |
|---|---:|---:|
| Hub | 38 | 38 |
| Valley Grid | 17 | 12 |
| Kestrel | 59 | 59 |
| Keel | 102 | 102 |
| Berth | 68 | 68 |
| Linden | 157 | 157 |
| Decision OS | 55 | 55 |
| Harbor | 38 | 38 |
| Tidewell | 33 | 33 |
| Relay | 61 | 61 |
| AgentProof | 8 | 8 |
| Estate intake | 7 | 7 |
| Signed → Live | 52 | 52 |

### Failures found, and the fix

Real product failures:

- **Keel, Berth, and Linden.** In the loading state, the count buttons did nothing. The handler returned before any toast. After a first toast was added, the other chips still looked dead because every chip used the same sentence. Each toast now names that filter ("Need a touch is a filter. This is the loading screen…"). Same pattern for Berth's status chips and Linden's queue chips.
- **Signed → Live, while it was being built.** The "I'm stuck" label was overwritten by the status word "Stuck", so the button did not say what it did. A search that matched nothing still answered with the current step. The guide search and the desk search rebuilt the field on every keystroke. "Preview the approved screen" ignored the save-error state. Those are fixed: the button says "I'm stuck" / "No puedo seguir", an unknown question says the demo only answers the five steps, typing updates the answer or the list without replacing the field, and the next save in the error state fails once and keeps the note.
- **AgentProof waitlist** was addressed to `agentproof@mail.grokbot.com` on the page, in `llms.txt`, and in `openapi.json`. It is now `cnavarro.business@gmail.com`.
- **Hub Tidewell title** said "Explaining why a month of revenue moved". The piece already said "Explaining why monthly revenue changed". The hub matches the piece.
- **Relay at 360px** scrolled sideways because the States menu was wider than the screen. The menu now stays inside the width.
- **Tap targets under 24px** on the hub summary and email, the States menus, Keel's home link and "Open only" checkbox, Decision OS lane buttons, Harbor sort headers, Tidewell's month bars at 360px, and the AgentProof and estate-intake links. Those hit areas are at least 44px tall. A second layout pass found no horizontal scroll and no control under 24×24px on any page, at 1280 and at 360.
- **Landmarks.** Signed had no `main`. The back link on AgentProof and estate intake sat outside `main`. axe reported those as moderate. They are inside `main` now. Final axe-core: **0 violations** on every page, both viewports, including serious and critical.

Not product bugs (the first audit script flagged them; the pages already worked):

- Tidewell's month bars are SVG groups. This Chrome has no `.click()` on them. The script now sends a real mouse event. Final count 33/0.
- Relay zoom only changes the percent, and the first script ignored digits. Some tabs and steps were already selected. Final count 61/0.
- Kestrel's reply box was filled with the same sentence twice, so the second type changed nothing. The script uses a second sentence. Final count 59/0.
- Valley Grid's States menu is on top of the model and stable, but Playwright's native menu call timed out on one run. Choosing "Empty · no alerts" does clear the panel. The script sets the value and fires `change` if the native call stalls. Final count 17/0 desktop, 12/0 mobile (the phone layout has no 3D film mode).

## Accuracy

Checked the pages, README, and meta descriptions.

- Role is **Concept direction**. Tools are **AI-assisted build (Claude, Cursor)**. Both are on the hub cards, the piece case studies, AgentProof, estate intake, and Signed → Live. On Signed → Live they stay in those exact words when the rest of the page is in Spanish.
- Linden credentials are unchanged: **GIA Applied Jewelry Professional Diploma (2023)** and **GIA Diamond Grading Certificate (in-person at AGS Laboratories, 2022)**. "Diamond Grader" does not appear.
- The only contact email is **cnavarro.business@gmail.com**. Kestrel's demo customer is `dana@acmedental.example`. That is fictional demo mail inside the ticket, not a contact address.
- No Blender claim. Valley Grid still says the 3D scene runs in the browser, and the README still says Cesar did not model it by hand.
- No prices on Cesar's offers. Kestrel's `$249` refund and Tidewell's fictional monthly recurring revenue are the demo subject, which the 12 October change list kept. Signed → Live shows no price.
- Demo shops and people on Signed → Live are named as fictional: Mesa Local, Rio Tile (Elena V.), Blue Finch Roofing, Cactus & Clay, Kiln Electric, Northwind Heating. Nothing is texted, emailed, or published.
- Three "by hand" sentences were left as they are. They are not a claim that Cesar built the site by hand: Linden's "Draft the advisor sends by hand", Tidewell's "rebuild the story by hand", and the README line that he did not model the scene by hand.

## Lighthouse and axe

Local Chrome, performance / accessibility / best practices / SEO. "Before" is this branch after the filter toasts and before the tap-target and spacing pass. "After" is the final tree. Accessibility was 100 before and after on every page. SEO was 100 before and after. Best practices was 100 except Valley Grid on desktop.

| Page | Viewport | Perf before | Perf after | Best practices before | Best practices after |
|---|---|---:|---:|---:|---:|
| Hub | desktop | 99 | 99 | 100 | 100 |
| Hub | mobile | 81 | 79 | 100 | 100 |
| Valley Grid | desktop | 59 | 59 | 0 | 0 |
| Valley Grid | mobile | 100 | 100 | 100 | 100 |
| Kestrel | desktop | 99 | 99 | 100 | 100 |
| Kestrel | mobile | 76 | 76 | 100 | 100 |
| Keel | desktop | 99 | 99 | 100 | 100 |
| Keel | mobile | 93 | 93 | 100 | 100 |
| Berth | desktop | 100 | 99 | 100 | 100 |
| Berth | mobile | 93 | 93 | 100 | 100 |
| Linden | desktop | 76 | 76 | 100 | 100 |
| Linden | mobile | 83 | 83 | 100 | 100 |
| Decision OS | desktop | 99 | 99 | 100 | 100 |
| Decision OS | mobile | 90 | 90 | 100 | 100 |
| Harbor | desktop | 99 | 99 | 100 | 100 |
| Harbor | mobile | 93 | 93 | 100 | 100 |
| Tidewell | desktop | 99 | 99 | 100 | 100 |
| Tidewell | mobile | 93 | 93 | 100 | 100 |
| Relay | desktop | 76 | 99 | 100 | 100 |
| Relay | mobile | 90 | 90 | 100 | 100 |
| AgentProof | desktop | 100 | 100 | 100 | 100 |
| AgentProof | mobile | 100 | 100 | 100 | 100 |
| Estate intake | desktop | 100 | 100 | 100 | 100 |
| Estate intake | mobile | 100 | 100 | 100 | 100 |
| Signed → Live | desktop | 100 | 100 | 100 | 100 |
| Signed → Live | mobile | 100 | 100 | 100 | 100 |

Relay's desktop score moved from 76 to 99 because the compliance bar and the inspector now reserve their height, so the case study does not jump when they fill in.

Scores still under 90, and why they were left:

- **Valley Grid desktop, performance 59, best practices 0.** The 3D model loads Three.js (about 4.3 MB) and blocks the main thread for tens of seconds. The phone layout does not download the model and scores 100 / 100 / 100 / 100. Taking the model off the desktop page would raise the score and would remove the piece. Accessibility on that run is still 100.
- **Linden desktop 76 and mobile 83, Kestrel mobile 76.** Lighthouse attributes a large layout shift to the book (Linden, CLS about 0.72) and to the run pipeline (Kestrel, CLS about 0.32) after the web font arrives. Reserving the list height did not move Linden's score. A taller reservation made the shift worse, so that try was reverted. Switching the brand font off would be a design change, not a small fix.
- **Hub mobile 81, then 79.** Render-blocking fonts, full-size photos, and the new Signed → Live card. The two-point drop is the new image.

The local preview server does not gzip. Lighthouse flags that as "uses text compression" on every page. GitHub Pages compresses responses. That flag is not a defect in the files.

axe-core after the landmark fix: 0 violations on all 13 pages, desktop and mobile.

360px: no page scrolls sideways. Every measured control is at least 24px on the short side. Signed → Live was also walked on a phone-width viewport: access, calendar, texting wait, one real file plus five sample photos, send-back (note required), undo, approve, Spanish for the whole page with the role and tools lines unchanged, an English reminder for Blue Finch and a Spanish reminder for Kiln Electric, CSV download, empty, loading, and save-error.

## For the résumé and LinkedIn

Plain version, only what this branch actually adds:

- New concept, Signed → Live: a phone flow in English and Spanish that takes a fictional agency client from a signed contract to approving a first ad, and an agency view of who is stuck. A reminder stays on the page. Nothing is texted or emailed.
- It is concept direction. The build line stays "AI-assisted build (Claude, Cursor)".
- It is not a shipped product, it was not tested with real clients, and it shows no prices.
- The Tidewell card title now matches the piece: "Explaining why monthly revenue changed".
- The AgentProof waitlist address is cnavarro.business@gmail.com, the same as the rest of the site.

## What was not verified

- The live GitHub Pages site. This is a draft pull request. `main` is unchanged.
- A test with real shop owners or Spanish-first speakers. The strategy asks for that. It was not invented here.
- Valley Grid best practices on a fast machine without the 3D trace stalling Lighthouse. Two local runs both scored 0 while accessibility and SEO scored 100.

## Screenshots

Desktop is 1280px wide. Mobile is 360px wide.

- `weekly-reports/2026-10-19/shots/hub-desktop.png`
- `weekly-reports/2026-10-19/shots/hub-mobile.png`
- `weekly-reports/2026-10-19/shots/signed-desktop.png`
- `weekly-reports/2026-10-19/shots/signed-mobile.png`
- `weekly-reports/2026-10-19/shots/keel-desktop.png`
- `weekly-reports/2026-10-19/shots/keel-mobile.png`
- `weekly-reports/2026-10-19/shots/berth-desktop.png`
- `weekly-reports/2026-10-19/shots/berth-mobile.png`
- `weekly-reports/2026-10-19/shots/linden-desktop.png`
- `weekly-reports/2026-10-19/shots/linden-mobile.png`
- `weekly-reports/2026-10-19/shots/valley-grid-desktop.png`
- `weekly-reports/2026-10-19/shots/valley-grid-mobile.png`
- `weekly-reports/2026-10-19/shots/kestrel-desktop.png`
- `weekly-reports/2026-10-19/shots/kestrel-mobile.png`
- `weekly-reports/2026-10-19/shots/relay-desktop.png`
- `weekly-reports/2026-10-19/shots/relay-mobile.png`
- `weekly-reports/2026-10-19/shots/tidewell-desktop.png`
- `weekly-reports/2026-10-19/shots/tidewell-mobile.png`
- `weekly-reports/2026-10-19/shots/decision-os-desktop.png`
- `weekly-reports/2026-10-19/shots/decision-os-mobile.png`
- `weekly-reports/2026-10-19/shots/harbor-desktop.png`
- `weekly-reports/2026-10-19/shots/harbor-mobile.png`
- `weekly-reports/2026-10-19/shots/agentproof-desktop.png`
- `weekly-reports/2026-10-19/shots/agentproof-mobile.png`
- `weekly-reports/2026-10-19/shots/estate-intake-desktop.png`
- `weekly-reports/2026-10-19/shots/estate-intake-mobile.png`

The hub card image is `img/signed.jpg`.
