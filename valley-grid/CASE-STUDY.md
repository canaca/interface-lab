# Valley Grid Ops: investigate an equipment alert

## Problem
Grid operators get alarms with numbers but no context. Deciding whether a reading needs a crew means jumping between monitoring screens, trend tools and phone calls.

## User
A control-room operator on shift, responsible for nine substations, who needs to understand and act on an alert in a few minutes.

## Key decisions
1. **The equipment is the interface.** The alert lives on the 3D transformer. Clicking the faulty bushing opens the investigation, and the camera moves to it.
2. **One panel, one path.** Alert, evidence, likely cause, action, confirmation and resolution all happen in the same panel, so the operator never loses context.
3. **Evidence before advice.** Readings and the 7-day trend come first. The likely cause is labeled as a suggestion, not a diagnosis.
4. **Every action confirms.** Dispatch, acknowledge and escalate each show what will happen before anything is sent. A failed dispatch says nothing was sent and keeps the operator's choices.
5. **Every state is included.** Empty, loading, data error and dispatch error each have their own screen. Use the States menu to review them.
6. **A quiet palette, one accent,** so warnings read instantly.

## Concept vs real
**Concept:** all data, people, crews and the substation are fictional.
**Real:** the concept running in the browser, the live 3D scene (AI-built with Claude and Cursor, directed by Cesar) running in Three.js, the full state flow, and graphics quality that adapts to laptop hardware. The Blender scripts that produced the 3D scene are AI-generated.
**Not built:** live sensor data, sign-in, and a real crew dispatch integration.

---

## 15-second clip shot list
Turn on **Film mode** and record one loop. It plays this exact sequence.

| Time | Beat | What happens |
| --- | --- | --- |
| 0.0–3.0 s | Fly in | Close on bushing B, the orange ring rising |
| 3.0–6.5 s | Pull back | Camera rises to the full transformer on the gold board |
| 6.0–7.4 s | Panels fade in | Unit status and alerts (no alerts yet) |
| 7.4–12.5 s | Workflow | 7.4 alert appears · 9.2 investigate, camera pushes in, detail loads · 10.6 dispatch crew · 11.2 confirm · ~12.5 resolved, ring turns teal |
| 12.9–15.0 s | End card | "Investigate an equipment alert" fades in as the camera pulls wide |

**Record:** fullscreen, 60 fps (Windows: Win+Alt+R, or OBS). Trim to one loop starting at the fly-in.
**CapCut:** soft whoosh at 3.0 s, click sounds at 9.2 s and 10.6 s, a light speed ramp on the pull-back, export MP4 at 1600×1200 for Dribbble.
