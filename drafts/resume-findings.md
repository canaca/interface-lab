# Résumé audit — Interface Lab repo

**Date of search:** 2026-10-06  
**Repo:** `canaca/interface-lab`  
**Live site (unchanged by this draft):** https://canaca.github.io/interface-lab/  
**This file is a report only.** No published page, résumé line, or existing case study was edited.

## Source of truth

When the repo and the résumés disagree, the attached résumés win.

| Source | File |
| --- | --- |
| Customer-success résumé | `Cesar_Navarro_Resume_DRAFT_i_CSM_Onboarding_with_Interface_Lab_v2` |
| Design-leaning résumé | `Cesar_Navarro_Resume_DRAFT_ii_Design_Leaning_v2` |

Locked facts used for every conflict below:

- SactownVideo book: **14 clients** (he onboarded **3**, inherited **11**).
- **100% A2P** approval across the **8** companies that needed it is a **team** result, not a solo result.
- Simple Solutions started in **2020**, about **10–12** clients served since then.
- He personally managed one med-aesthetics client's Meta ads on about a **$60K** annual budget.
- Client budgets ranged about **$1,000/month to $5–7K/month**.
- GoHighLevel: **6+ years**.
- Interface Lab pieces are **October 2026 concept work**, built with AI tools Cesar **directed**.
- Do not claim he wrote the Blender scripts.
- Do not list case-study writing as a skill.

## Where this was searched

| Place | Result |
| --- | --- |
| Working tree on `main` at `be829b8` (2026-10-04 23:37 PT), "Accuracy credits + Decision OS contrast + Harbor label" | Searched. Findings below. |
| Parent commit `072bf63` (2026-10-04 21:38 PT), "Interface Lab portfolio" | Searched with `git grep` and `git show`. Older wording is quoted where it still conflicts. That wording is **superseded on `main`** but remains in git history. |
| `git branch -a`, `git ls-remote --heads origin`, GitHub API `repos/canaca/interface-lab/branches` | **Only `main`.** |
| `gh repo list canaca` | **Only `canaca/interface-lab`.** |
| `functional-v5` | **Not found.** No local branch, no remote head, no pull request. Recorded as **OPEN** only in the sense that this audit cannot see a branch that is not on this remote. Nothing in this repo was skipped because of that name. |
| Pull requests | None existed at search time. |

Text search covered `*.html`, `*.md`, `*.py`, and the readable headers of the Blender scripts. `valley-grid/t2.json` and `valley-grid/board.json` are base64 glTF payloads (Khronos glTF generator string only). They contain no biography. `img/` and `og-image.png` were not OCR'd. **OPEN:** whether the preview image contains résumé text that is not also in the HTML `alt` attributes quoted below.

## Summary

The repo does **not** state the SactownVideo book, the A2P team result, Simple Solutions' start year or client count, the med-aesthetics budget, the monthly budget range, or 6+ years of GoHighLevel. Those locked facts are **absent**, so the site does not contradict them.

The conflicts that do exist are about **Interface Lab authorship and labeling**:

1. **Current `main` still says Cesar "designs" the interfaces** in the hub hero and social previews, while the locked role is **concept direction** of work built with AI tools he directed.
2. **Decision OS is labeled a "working build" and "a real product in development,"** with the role "Product owner, design direction." Both résumés describe **four** October 2026 **concepts** (AI support agent, CRM deal cleanup, utility operations, SaaS revenue analytics). Decision OS is a fifth piece and is not described that way on either résumé.
3. **Kestrel, Harbor, and Tidewell list tools as HTML, CSS, and JavaScript** (Tidewell: HTML, SVG charts, JavaScript) and do not say the build was AI-assisted. That can be read as hands-on coding. The locked fact is AI-built and directed.
4. **Commit `072bf63` (still in history, no longer the live text) claimed 3D modeling, a front-end build, Blender as his tool, and "Design and build: Cesar Navarro."** That conflicts with "concept direction" and with "never claim he wrote the Blender scripts." Current `main` replaced most of that credit. The Blender script files themselves do not name him as author.

Case-study **pages exist**. Case-study writing is **not** listed as a skill anywhere in the repo. That part matches the lock. Who wrote the case-study sentences is **OPEN**.

## Absent locked facts (no conflict, because they are not claimed)

Searched the working tree and both commits for: Sactown, SactownVideo, GoHighLevel, GHL, A2P, 10DLC, Simple Solutions, Talisman, med-aesthetics, med spa, client counts, CTR, budget figures, and "6+ years" / "6 years."

**No matches** in résumé or biography prose. The only "14" that appears in product UI is Harbor's fictional "14 open deals" (`harbor-copilot/index.html` crumbs and table count). That is demo data for a concept, not the SactownVideo book. Do not reuse it as a client-count claim.

## Findings — current `main` (`be829b8`)

### `README.md`

| Lines | What it claims | Vs résumés |
| --- | --- | --- |
| 3 | "Live, working interface concepts for AI and data products, **directed by** Cesar Navarro." | **ALIGNED** with concept direction. |
| 23–25 | Concepts directed by Cesar; he set the problem, user, flow, and design decisions, and reviewed every state. "The code and 3D assets were generated with those tools" (Claude, Cursor). | **ALIGNED.** |
| 27 | "`blender/` holds the **AI-generated** Python scripts" (`build_t2.py`, `board2.py`, `heroes.py`). | **ALIGNED** with "do not claim he wrote the Blender scripts," as long as this sentence stays. The scripts are still in the repo; see below. |
| 49 | Contact `cnavarro.business@gmail.com`. | **ALIGNED** with both résumés. |

### `index.html` — hub (about, role, offers)

| Lines | What it claims | Vs résumés |
| --- | --- | --- |
| 6–7, 12–13, 20–21 | Title and descriptions: "Cesar Navarro **designs** interfaces for AI and data products." | **CONFLICT.** Locked role is concept direction of AI-built work. "Designs" is the stronger, hands-on verb. The design-leaning résumé headline is "Product Design (Concept Work)" and the body says he is "directing" the concepts, not that he personally coded them. |
| 16, 23 | Preview alt text: "Cesar Navarro: **I design interfaces that actually run, with five working prototypes**." | **CONFLICT** on two points. (1) "I design" vs concept direction. (2) **Five** prototypes. Both résumés say **four** concepts: AI support agent, CRM deal cleanup, utility operations, SaaS revenue analytics. The fifth item on the site is Decision OS. |
| 227 | Nav: "Cesar Navarro" and "Open for projects." | No experience claim. **ALIGNED** as a contact state, not a job history. |
| 231–233 | Eyebrow "Product design for AI and data products." Hero: "I design interfaces that actually run." Body: every project is a working prototype, "labeled honestly as a concept or a working build." | **CONFLICT** on "I design," same as the meta description. The "working build" label is the Decision OS problem in the next row. |
| 238 | Section note: "Concept: fictional data, real working interface. **Working build: a real product in development.**" | **CONFLICT** with "Interface Lab pieces are October 2026 concept work." Neither résumé describes a separate product in development. |
| 245, 250 | Valley Grid role "**Concept direction**." Tools: "AI-assisted build (Claude, Cursor)." Outcome: live 3D scene "built with AI-assisted tooling (Claude, Cursor)." "Not tested with real operators or live data." | **ALIGNED** with concept direction and with not claiming he wrote the Blender scripts. "Not tested" matches the evidence gap in the case-study drafts. |
| 259 | Kestrel role "Concept direction." Tools: "**HTML, CSS, JavaScript**." | Role **ALIGNED**. Tools line is a **CONFLICT** if read as "he built this by hand." Résumés: built with AI tools (Claude, Cursor) under his direction. |
| 263–265 | Decision OS tag "**Working build**." Role: "**Product owner, design direction**." Status: "ChatGPT import works. **The Chart approved.** Not in production. Demo uses fictional data." | **CONFLICT.** Résumés do not list Decision OS, do not give him "product owner," and do not say a chart was approved at a production phase. Count of concepts on the résumés is four, not five. Fictional demo data is fine. "Not in production" does not make the "working build / real product" label match the résumés. |
| 271 | Harbor role "Concept direction." Tools: "HTML, CSS, JavaScript." | Same as Kestrel. Role **ALIGNED**. Tools line **CONFLICT** if read as hand-built. |
| 277 | Tidewell role "Concept direction." Tools: "HTML, SVG charts, JavaScript." | Same pattern. Role **ALIGNED**. Tools line **CONFLICT** if read as hand-built. |
| 283–288 | "How I work": a **two-week sprint** (map the job, first live build, every state, handoff with "clean code" and a walkthrough video). | **Not on either résumé.** It is a service promise, not a past job. **OPEN** whether he offers this. It should not be copied onto a résumé as experience. It also sits next to "clean code," which pulls toward a hands-on build claim. |
| 292–298 | Offers: "AI UX Audit," "Live Prototype Sprint," "Fractional Design Partner" (weekly sprints, a design system, "in your Slack and standups"). Prices are "Scoped after a short discovery call" (no dollar amounts). | **Not on either résumé.** No product-design client engagements are listed there. **OPEN** as a forward offer. Do not write it up as completed client work. |
| 317–320 | Contact form paths: product design role, freelance product design, website, Meta ads. | Services, not a biography. Meta ads and websites are consistent with Simple Solutions on the résumés. No client counts or results here. |
| 396 | Footer: "Cesar Navarro · **Upper Sacramento area · English and Spanish**." | **ALIGNED** with bilingual English/Spanish (fluent) and with Cameron Park / Sacramento-area location. "Upper Sacramento area" is not a different city claim. |

### Piece pages — case studies and credits

These are concept write-ups, not a résumé file. They matter because they state his role.

| File and lines | What it claims | Vs résumés |
| --- | --- | --- |
| `kestrel/index.html` 210–224 | Problem, user, decisions, outcome for a refund-approval concept. "Not yet tested with real users or a real billing system." Fictional company and data. | **ALIGNED** as concept work. The design-leaning résumé names this piece (Kestrel: a person approves the money and the reply). |
| `kestrel/index.html` 227 | Footer: "**Concept direction:** Cesar Navarro." | **ALIGNED.** |
| `harbor-copilot/index.html` 193–207 | CRM bulk-cleanup concept. Undo, conflicts, fictional deals. "Not yet tested with real users or a real CRM." | **ALIGNED** with the résumé's "CRM deal cleanup" concept and "undo for bulk changes." |
| `harbor-copilot/index.html` 210 | Footer: "Concept direction: Cesar Navarro." | **ALIGNED.** |
| `tidewell/index.html` 154–168 | Revenue-explanation concept. Fictional accounts and numbers. "Not yet tested with real users or real billing data." | **ALIGNED** with the résumé's "SaaS revenue analytics" concept. The numbers inside the prototype are demo UI, not client results. Do not move them onto a résumé. |
| `tidewell/index.html` 171 | Footer: "Concept direction: Cesar Navarro." | **ALIGNED.** |
| `decision-os/index.html` 7, 13, 21 | Meta description: "**Working build**, shown with fictional demo data." | **CONFLICT** with October 2026 concept-work labeling. See hub notes above. |
| `decision-os/index.html` 186–200 | Case study calls it a working build. Outcome: "The working build imports ChatGPT history. Its visual system, The Chart, **was approved at Phase 9**. It is not deployed to production." Label: "This page is a separate demo with fictional data, **not the product**." | **CONFLICT.** "Phase 9" approval and a product separate from this demo are **not** on either résumé. **OPEN:** whether any product by that name exists outside this repo. This repo only contains the demo page. |
| `decision-os/index.html` 203 | Footer: "**Product owner and design direction:** Cesar Navarro." | **CONFLICT** with concept direction as the role for Interface Lab pieces. |
| `valley-grid/index.html` 245 | End card: "Valley Grid Ops · **concept by Cesar Navarro**." | **ALIGNED** enough (concept, not "built by" or "Blender by"). Weaker than the old "CONCEPT BUILD · DESIGN" line. |
| `valley-grid/index.html` 247 | Credit: "**CONCEPT DIRECTION: CESAR NAVARRO**." | **ALIGNED.** |
| `valley-grid/CASE-STUDY.md` 1–21 | Problem, user, six decisions, concept vs real. Line 19: the live 3D scene was "built with AI-assisted tooling: Claude, Cursor" in Three.js. "Not built: live sensor data, sign-in, and a real crew dispatch integration." | **ALIGNED.** Does not say he wrote `build_t2.py`. |
| `valley-grid/CASE-STUDY.md` 24–36 | Shot list for a 15-second film mode, including a CapCut note. | Process note for a clip, not a skill list. The design-leaning résumé does not claim a finished promo video. **OPEN** whether a recorded clip exists. It is not in this repo (`img/` has stills only). |

### `blender/build_t2.py`, `blender/board2.py`, `blender/heroes.py`

Headers describe what the scripts build and how to run them. They do **not** say "written by Cesar Navarro."

- **Current README** calls them AI-generated. **ALIGNED** with the lock, via the README, not via the script files.
- **Do not** add these scripts to a skills list, and do not say he wrote them.
- `valley-grid/index.html` comments (current) say "Detailed exported model" and "gold circuit board scene" without naming Blender in those two comments. That is **ALIGNED**.

### Case-study writing as a skill

Case studies are **published as page sections** (`index.html` details, each piece's `<section class="cs">`, and `valley-grid/CASE-STUDY.md`). No skills list in this repo says "case-study writing." **ALIGNED** with "do not list case-study writing as a skill."

**OPEN:** whether Cesar wrote that prose himself or directed AI drafts. The current README says he set problem, user, flow, and design decisions and that code and 3D assets were generated with AI tools. It does not say who wrote the case-study paragraphs.

## Findings — superseded text still in git history

Live Pages is built from `main`, which is `be829b8`. The lines below are **not** what the live site shows now. They are still in commit `072bf63` and conflict with the résumés. If an old link, fork, or cached preview quoted them, the résumés still win.

| Where in `072bf63` | Claim | Conflict |
| --- | --- | --- |
| `README.md` line 3 | "concepts … **by** Cesar Navarro" (not "directed by") | Sounds like sole authorship. |
| `README.md` lines 23–31, heading "Blender" | "The 3D models are built by Python scripts in `blender/`" with no "AI-generated" and no direction credit. | Can be read as his scripts. Conflicts with "never claim he wrote the Blender scripts." |
| `index.html` Valley Grid role | "Product design, **3D modeling, front-end build**." Tools: "**Blender**, Three.js, JavaScript." | **CONFLICT.** Claims he modeled in Blender and built the front end. |
| `index.html` Valley Grid outcome | "3D models **built in Blender** running live in the browser." | **CONFLICT** with AI-directed concept credit. |
| `index.html` Kestrel, Harbor, Tidewell roles | "Product design, **prototype build**." | Stronger than concept direction. |
| `kestrel/index.html`, `harbor-copilot/index.html`, `tidewell/index.html` footers | "**Design and build:** Cesar Navarro." | **CONFLICT.** Current footers say "Concept direction." |
| `valley-grid/index.html` credit | "**CONCEPT BUILD · DESIGN:** CESAR NAVARRO." | **CONFLICT.** Current credit says "CONCEPT DIRECTION." |
| `valley-grid/CASE-STUDY.md` | "the 3D models **built in Blender**." | **CONFLICT.** Current line says AI-assisted tooling (Claude, Cursor). |
| `valley-grid/index.html` comments | "Detailed **Blender** model" and "gold circuit board **from Blender**." | Names the tool. Does not by itself say he wrote the scripts. Still easier to misread next to the old role line. |

`decision-os/index.html` footer was already "Product owner and design direction: Cesar Navarro" in `072bf63`. That conflict is **still on `main`** (see above).

## What this audit did not find

- No résumé PDF, LinkedIn export, about-me essay, or experience section for SactownVideo, Simple Solutions, or Talisman.
- No claim that he personally hit 100% A2P, and no claim that contradicts the team result, because A2P is not mentioned.
- No dollar amounts for client budgets.
- No testimonial.
- No `functional-v5` branch to compare.

## Do not do from this report

Do not "fix" the live pages inside this drafts task. Label and credit changes belong in a later, separate change if Cesar asks for them. Until then, public copy on `main` is what shipped in `be829b8`, and the résumés remain the source of truth for applications and for anything new drafted here.
