# "Grid Board": the transformer as a miniature on a gold circuit-board map of the valley grid.
# Energy runs along glowing traces; the faulted feeder glows orange. Shot low and macro, like a product film.
# Usage: python3 board.py --still out.png [--samples N] [--res WxH] [--cam low|top|wide] [--frame F]
import bpy, bmesh, math, sys, argparse, random
from mathutils import Vector, Matrix

ap = argparse.ArgumentParser()
ap.add_argument("--still"); ap.add_argument("--blend"); ap.add_argument("--glb", default="t2.glb")
ap.add_argument("--samples", type=int, default=64); ap.add_argument("--res", default="1600x1200")
ap.add_argument("--cam", default="low"); ap.add_argument("--export-board"); ap.add_argument("--export-paths"); ap.add_argument("--anim"); ap.add_argument("--step", type=int, default=2); ap.add_argument("--frame", type=int, default=-1); ap.add_argument("--start", type=int, default=0); ap.add_argument("--end", type=int, default=360)
A = ap.parse_args(sys.argv[1:])
bpy.ops.wm.read_factory_settings(use_empty=True)
scn = bpy.context.scene; col = scn.collection
random.seed(11)

def lin(h):
    h = h.lstrip("#"); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((x + .055) / 1.055) ** 2.4 if x > .04045 else x / 12.92 for x in c) + (1,)
def mat(name, hexc, metal=0., rough=.5, emit=None, strength=0., coat=0.):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = lin(hexc); b.inputs["Metallic"].default_value = metal; b.inputs["Roughness"].default_value = rough
    if coat: b.inputs["Coat Weight"].default_value = coat
    if emit: b.inputs["Emission Color"].default_value = lin(emit); b.inputs["Emission Strength"].default_value = strength
    return m
def ob(name, bm, m, bevel=0.):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); col.objects.link(o); me.materials.append(m)
    if bevel:
        bv = o.modifiers.new("B", "BEVEL"); bv.width = bevel; bv.segments = 2; bv.limit_method = "ANGLE"
    return o
def bbox(bm, size, loc, rz=0.):
    r = bmesh.ops.create_cube(bm, size=1)
    bmesh.ops.transform(bm, matrix=Matrix.Translation(loc) @ Matrix.Rotation(rz, 4, "Z") @ Matrix.Diagonal((*size, 1)), verts=r["verts"])
def bcyl(bm, r, h, loc, seg=20):
    res = bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r, depth=h)
    bmesh.ops.translate(bm, vec=loc, verts=res["verts"])

G = dict(
    board=mat("Board", "#16110D", .2, .55, coat=.4),
    gold=mat("Gold", "#D9A65E", 1., .22),
    goldDim=mat("GoldDim", "#B8874A", 1., .3),
    chip=mat("Chip", "#1E1813", .3, .4, coat=.6),
    teal=mat("Teal", "#6FE3D0", 0, .3, emit="#6FE3D0", strength=6),
    orange=mat("Orange", "#E07A34", 0, .3, emit="#E8823A", strength=7),
)

# board slab with bevelled edge
bm = bmesh.new(); bbox(bm, (40, 30, .6), (0, 0, -.3)); ob("Board", bm, G["board"], .12)

# traces: parallel bundles routed with 45-degree corners, like a real board
SUBS = [(-14, 8), (-15, -6), (-6, 11), (9, 10), (15, 2), (13, -9), (-3, -11), (4, -4.5)]
FAULT = 4
trace_bm = bmesh.new(); live_bm = bmesh.new(); fault_bm = bmesh.new(); pad_bm = bmesh.new(); part_bm = bmesh.new()
LIVE_PATHS = []; FAULT_PATH = None
def route(a, b):
    (x0, y0), (x1, y1) = a, b; dx, dy = x1 - x0, y1 - y0
    d = min(abs(dx), abs(dy))
    if abs(dx) >= abs(dy): m = (x0 + math.copysign(abs(dx) - d, dx), y0)
    else: m = (x0, y0 + math.copysign(abs(dy) - d, dy))
    return [a, m, b]
def seg(bmx, p, q, w=.09, h=.03, z=.02):
    v = Vector((q[0] - p[0], q[1] - p[1], 0)); L = v.length
    if L < 1e-3: return
    bbox(bmx, (L + w, w, h), ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2, z), math.atan2(v.y, v.x))
def offset_path(pts, o):
    out = []
    for i, p in enumerate(pts):
        q = pts[i + 1] if i + 1 < len(pts) else pts[i]; r = pts[i - 1] if i > 0 else pts[i]
        d = Vector((q[0] - r[0], q[1] - r[1], 0)).normalized(); n = Vector((-d.y, d.x, 0))
        out.append((p[0] + n.x * o, p[1] + n.y * o))
    return out
for i, s_ in enumerate(SUBS):
    start = (math.copysign(3.4, s_[0]) if abs(s_[0]) > abs(s_[1]) else 0, 0 if abs(s_[0]) > abs(s_[1]) else math.copysign(3.4, s_[1]))
    base = route(start, s_)
    for k in range(5):
        o = (k - 2) * .26; pts = offset_path(base, o)
        live = k == 2
        target = fault_bm if (i == FAULT and live) else live_bm if live else trace_bm
        for p, q in zip(pts, pts[1:]): seg(target, p, q, w=.12 if live else .07)
        bcyl(pad_bm, .13, .04, (pts[-1][0], pts[-1][1], .03), 16); bcyl(pad_bm, .13, .04, (pts[0][0], pts[0][1], .03), 16)
        if live and i != FAULT: LIVE_PATHS.append(pts)
        if live and i == FAULT: FAULT_PATH = pts
# decorative buses on a 0.5 grid, in parallel groups, avoiding the centre pad and the chips
def clear(x, y): return math.hypot(x, y) > 5 and all(abs(x - a) > 2.2 or abs(y - b) > 1.8 for a, b in SUBS)
for g in range(70):
    x = round(random.uniform(-18, 18) * 2) / 2; y = round(random.uniform(-13, 13) * 2) / 2
    horiz = random.random() < .5; L = random.choice((2, 3, 4, 5, 6)); n = random.randint(2, 6); bend = random.choice((-1, 1))
    for k in range(n):
        o = k * .22
        p0 = (x, y + o) if horiz else (x + o, y)
        p1 = (x + L, y + o) if horiz else (x + o, y + L)
        p2 = (p1[0] + 1.2, p1[1] + bend * 1.2) if horiz else (p1[0] + bend * 1.2, p1[1] + 1.2)
        if not (clear(*p0) and clear(*p1) and clear(*p2)): continue
        seg(trace_bm, p0, p1, w=.05, h=.02); seg(trace_bm, p1, p2, w=.05, h=.02)
        bcyl(pad_bm, .07, .03, (p2[0], p2[1], .02), 10)
for n in range(160):
    x = round(random.uniform(-19, 19) * 4) / 4; y = round(random.uniform(-14, 14) * 4) / 4
    if not clear(x, y): continue
    if random.random() < .6: bbox(part_bm, (.3, .15, .1), (x, y, .06), random.choice((0, math.pi / 2)))
    else: bcyl(pad_bm, .06, .03, (x, y, .02), 10)
ob("Traces", trace_bm, G["goldDim"]); ob("LiveTraces", live_bm, G["teal"]); ob("FaultTrace", fault_bm, G["orange"]); ob("Pads", pad_bm, G["gold"]); ob("Parts", part_bm, G["chip"])

# substation chips with gold pins
for i, (x, y) in enumerate(SUBS):
    w, d = random.uniform(1.6, 2.6), random.uniform(1.2, 1.8)
    bm = bmesh.new(); bbox(bm, (w, d, .35), (x, y, .2)); ob(f"Sub{i}", bm, G["chip"], .05)
    bm = bmesh.new()
    for k in range(int(w / .3)):
        for sgn in (-1, 1): bbox(bm, (.1, .25, .06), (x - w / 2 + .2 + k * .3, y + sgn * (d / 2 + .1), .04))
    ob(f"Sub{i}Pins", bm, G["gold"])
    bm = bmesh.new(); bcyl(bm, .12, .02, (x + w / 2 - .3, y + d / 2 - .3, .39), 16); ob(f"Sub{i}Led", bm, G["orange"] if i == FAULT else G["teal"])

# centre pad + the T2 model as a miniature
bm = bmesh.new(); bcyl(bm, 3.6, .08, (0, 0, .04), 96); ob("CentrePad", bm, G["gold"])
bm = bmesh.new(); bcyl(bm, 3.3, .1, (0, 0, .06), 96); ob("CentreInset", bm, G["board"])
PRE_IMPORT = set(o.name for o in bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=A.glb)
roots = [o for o in bpy.context.selected_objects if o.parent is None]
for o in roots:
    o.scale = (o.scale[0] * .42, o.scale[1] * .42, o.scale[2] * .42); o.location = (o.location[0] * .42, o.location[1] * .42, o.location[2] * .42 + .1)
# hide the model's own gantry to keep the miniature clean
for o in bpy.data.objects:
    if o.name.startswith(("Gantry", "StringInsulator", "Busbar")): o.hide_render = True



if A.export_paths:
    import json
    json.dump({"scale": .42, "live": LIVE_PATHS, "fault": FAULT_PATH, "subs": SUBS, "fault_sub": FAULT}, open(A.export_paths, "w"))
if A.export_board:
    for o in bpy.data.objects: o.select_set(o.name in PRE_IMPORT and o.type == "MESH")
    bpy.context.view_layer.objects.active = next(o for o in bpy.data.objects if o.select_get())
    bpy.ops.export_scene.gltf(filepath=A.export_board, export_format="GLB", use_selection=True, export_apply=True, export_yup=True, export_animations=False)
    print("DONE export"); sys.exit(0)

# ---------------- animation: pulses, fault blink, camera move (24 fps, 15 s) ----------------
scn.render.fps = 24; scn.frame_start = 0; scn.frame_end = 360
pulse_m = mat("Pulse", "#BFFFF4", 0, .2, emit="#9FF5E6", strength=14)
for pi, pts in enumerate(LIVE_PATHS):
    L = [Vector((p[0], p[1], .12)) for p in pts]; seglen = [(L[i+1] - L[i]).length for i in range(len(L) - 1)]; tot = sum(seglen)
    def at(t):
        d = t * tot
        for i, sl in enumerate(seglen):
            if d <= sl: return L[i].lerp(L[i+1], d / sl if sl else 0)
            d -= sl
        return L[-1]
    for j in range(2):
        bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=12, v_segments=8, radius=.065); o = ob(f"Pulse{pi}_{j}", bm, pulse_m)
        period = 72 + pi * 6; ph = j * .5 + pi * .13
        for f in range(0, 361, 3):
            t = ((f / period) + ph) % 1
            o.location = at(t); o.keyframe_insert("location", frame=f)
        for fc in o.animation_data.action.fcurves if hasattr(o.animation_data.action, "fcurves") else []:
            for kp in fc.keyframe_points: kp.interpolation = "LINEAR"
em = G["orange"].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
for f in range(0, 361, 6):
    em.default_value = 9 if (f // 6) % 4 < 2 else 1.5; em.keyframe_insert("default_value", frame=f)

# lights and camera
def area(name, loc, target, energy, color, size):
    L = bpy.data.lights.new(name, "AREA"); L.energy = energy; L.color = lin(color)[:3]; L.size = size
    o = bpy.data.objects.new(name, L); col.objects.link(o); o.location = loc
    o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
area("Key", (-14, -16, 18), (0, 0, 0), 9000, "#FFD8B0", 10)
area("Rim", (16, 18, 8), (0, 0, 1), 3500, "#6FE3D0", 8)
area("Spot", (2, -4, 10), (0, 0, 1), 1500, "#FFE6CC", 3)
w = bpy.data.worlds.new("W"); w.use_nodes = True; scn.world = w
w.node_tree.nodes["Background"].inputs["Color"].default_value = lin("#0E0A08"); w.node_tree.nodes["Background"].inputs["Strength"].default_value = .4

CAMS = {"low": ((9.5, -12.5, 3.2), (0, 0, 1.4), 70, 1.8, (0, -1, 1.2)),
        "top": ((0, -6, 30), (0, 0, 0), 40, 6.0, (0, 0, 0)),
        "wide": ((18, -24, 13), (0, 0, 0), 45, 4.0, (0, 0, .8))}
pos, look, lens, fs, foc = CAMS[A.cam]
cd = bpy.data.cameras.new("Cam"); cd.lens = lens
c = bpy.data.objects.new("Cam", cd); col.objects.link(c); c.location = pos
c.rotation_euler = (Vector(look) - Vector(pos)).to_track_quat("-Z", "Y").to_euler()
f = bpy.data.objects.new("F", None); col.objects.link(f); f.location = foc
cd.dof.use_dof = True; cd.dof.focus_object = f; cd.dof.aperture_fstop = fs; scn.camera = c
if A.anim or A.frame >= 0:
    tc = c.constraints.new("TRACK_TO"); tc.target = f; tc.track_axis = "TRACK_NEGATIVE_Z"; tc.up_axis = "UP_Y"
    cd.dof.aperture_fstop = 3.2; cd.lens = 42
    KEYS = [(0, (6.5, -10.5, 1.5), (0, -1.6, .9)), (96, (8.5, -6.0, 3.0), (0, 0, 1.2)),
            (216, (9.5, 8.5, 5.5), (0, 0, .9)), (360, (17, -21, 15), (0, 0, 0))]
    for fr, pos_, look_ in KEYS:
        c.location = pos_; c.keyframe_insert("location", frame=fr); f.location = look_; f.keyframe_insert("location", frame=fr)

scn.render.engine = "CYCLES"; scn.cycles.device = "CPU"; scn.cycles.samples = A.samples; scn.cycles.use_denoising = True
W, H = map(int, A.res.split("x")); scn.render.resolution_x = W; scn.render.resolution_y = H
try: scn.view_settings.view_transform = "AgX"; scn.view_settings.look = "AgX - Medium High Contrast"; scn.view_settings.exposure = .3
except Exception: pass
if A.blend: bpy.ops.wm.save_as_mainfile(filepath=A.blend)
scn.render.use_persistent_data = True; scn.cycles.max_bounces = 4
if A.frame >= 0:
    scn.frame_set(A.frame); scn.render.filepath = A.still; bpy.ops.render.render(write_still=True)
elif A.anim:
    import os, time
    for fr in range(A.start, A.end + 1, A.step):
        out = os.path.join(A.anim, f"f{fr:04d}.png")
        if os.path.exists(out): continue
        scn.frame_set(fr); scn.render.filepath = out; t0 = time.time(); bpy.ops.render.render(write_still=True); print("FRAME", fr, round(time.time() - t0, 1), flush=True)
elif A.still: scn.render.filepath = A.still; bpy.ops.render.render(write_still=True)
print("DONE board", A.cam)
