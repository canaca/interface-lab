# Interface Lab

Live, working interface concepts directed by Cesar Navarro. The pieces are October 2026 concept work. He set the problem, the user, and the flow. The builds were made with AI tools under that direction. Websites and landing pages, through Simple Solutions, since 2020.

Every piece here runs in the browser. Click, drag, approve, undo, and see what happens.

![Valley Grid Operations](img/grid.jpg)

| Piece | Label | What it shows |
| --- | --- | --- |
| [Keel Account Health](keel/) | Concept · October 2026 | A customer-success book: health from five visible signals, filters, a confirmed next step, tasks, undo, and a sample CSV |
| [Linden Client Book](linden/) | Concept · October 2026 | A boutique morning book: who is due, what they prefer, and a draft that never sends. Fictional clients. No prices |
| [Berth Onboarding](berth/) | Concept · October 2026 | A new-account checklist: blocked steps, who owes the next one, and a nudge that stays a task. Nothing is emailed |
| [Relay Speed to Lead](relay/) | Concept · October 2026 | Instant reply, missed-call text, and a pipeline, previewed on fictional leads. Nothing sends |
| [Valley Grid Operations](valley-grid/) | Concept · October 2026 | Investigate an equipment alert, from alert to crew sent ([case study](valley-grid/CASE-STUDY.md)). The 3D scene was generated with AI tools under direction |
| [Kestrel Agent Console](kestrel/) | Concept · October 2026 | An AI agent handles a refund ticket. A person approves the money and the reply |
| [Harbor CRM Copilot](harbor-copilot/) | Concept · October 2026 | Bulk deal cleanup shown as diffs in the table, with conflicts and undo |
| [Decision OS](decision-os/) | Concept · October 2026 | Import a sample ChatGPT export and see where everything stands. Fictional data. Not a shipped product |
| [Tidewell Revenue Pulse](tidewell/) | Concept · October 2026 | Why a fictional month of revenue moved, down to four accounts and a win-back task. Not a finance claim |

Each page has its own case study at the bottom, and a States menu to see empty, loading, and error states.

## Built with

Plain HTML, CSS, and JavaScript. Three.js for 3D, used only on Valley Grid, where the 3D model is the interface. No build step. Each piece is one file.

## How these were made

These are concepts directed by Cesar Navarro and built with AI tools (Claude, Cursor) under his direction: he set the problem, user, flow and design decisions, and reviewed every state. The code and 3D assets were generated with those tools.

The `blender/` folder holds the AI-generated Python scripts used to produce Valley Grid's 3D scene (`build_t2.py` for Transformer T2, `board2.py` for the circuit-board scene, `heroes.py` for hero objects). They run with Blender's Python package (`pip install bpy`, then `python3 blender/build_t2.py --still out.png`).

## Site address

Link previews (Open Graph and Twitter) use the full web address of the site, `https://canaca.github.io/interface-lab/`. If the repo or GitHub username changes, update `canaca` and `/interface-lab/` in the meta tags of each page. The preview image is `og-image.png` (1200×630) and the icon is `favicon.svg`.

## Contact form setup

The hub has a step-by-step contact form. It works on GitHub Pages with no server.

1. Make a free form at formspree.io (or any service that accepts JSON posts).
2. In `index.html`, find the config block near the bottom and paste the form URL into `FORM_ENDPOINT`.
3. Optional: paste a booking link (like Calendly) into `BOOKING_URL`. Strong-fit leads see a "Book a call" button.

If `FORM_ENDPOINT` is empty or the post fails, the form opens the visitor's email app with their answers filled in, addressed to cnavarro.business@gmail.com.

## Run it

Open `index.html`, or turn on GitHub Pages (Settings > Pages > Deploy from branch > main).

All data in these demos is fictional.

Contact: cnavarro.business@gmail.com
