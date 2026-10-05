# Hero objects for the portfolio pieces, rendered as studio product shots.
# Usage: python3 heroes.py --scene kestrel|harbor|tidewell|dos --still out.png [--samples N] [--res WxH]
import bpy, bmesh, math, sys, argparse, random
from mathutils import Vector, Matrix

ap = argparse.ArgumentParser()
ap.add_argument("--scene", required=True); ap.add_argument("--still"); ap.add_argument("--blend")
ap.add_argument("--samples", type=int, default=64); ap.add_argument("--res", default="1600x1200")
A = ap.parse_args(sys.argv[1:])
bpy.ops.wm.read_factory_settings(use_empty=True)
scn = bpy.context.scene; col = scn.collection
random.seed(7)

def lin(h):
    h = h.lstrip("#"); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((x + .055) / 1.055) ** 2.4 if x > .04045 else x / 12.92 for x in c) + (1,)

def mat(name, hexc, metal=0., rough=.5, coat=0., emit=None, strength=0., trans=0., ior=1.45):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = lin(hexc); b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = rough
    if coat: b.inputs["Coat Weight"].default_value = coat
    if trans: b.inputs["Transmission Weight"].default_value = trans; b.inputs["IOR"].default_value = ior
    if emit: b.inputs["Emission Color"].default_value = lin(emit); b.inputs["Emission Strength"].default_value = strength
    return m

def ob(name, bm, m, smooth=True, bevel=0., segs=3):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    if smooth:
        for p in me.polygons: p.use_smooth = True
    o = bpy.data.objects.new(name, me); col.objects.link(o); me.materials.append(m)
    if bevel:
        bv = o.modifiers.new("Bevel", "BEVEL"); bv.width = bevel; bv.segments = segs; bv.limit_method = "ANGLE"
    return o

def rbox(name, size, loc, m, bevel=.08, rot=(0, 0, 0)):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1)
    bmesh.ops.scale(bm, vec=size, verts=bm.verts)
    o = ob(name, bm, m, smooth=False, bevel=bevel, segs=4); o.location = loc; o.rotation_euler = rot; return o

def sphere(name, r, loc, m, sub=4, ico=False):
    bm = bmesh.new()
    if ico: bmesh.ops.create_icosphere(bm, subdivisions=sub, radius=r)
    else: bmesh.ops.create_uvsphere(bm, u_segments=48, v_segments=24, radius=r)
    o = ob(name, bm, m, smooth=not ico); o.location = loc; return o

def torus(name, R, r, loc, m, rot=(0, 0, 0), seg=96, sides=16):
    bm = bmesh.new(); rings = []
    for i in range(seg):
        a = i / seg * 2 * math.pi; ring = []
        for j in range(sides):
            b = j / sides * 2 * math.pi
            ring.append(bm.verts.new(((R + r * math.cos(b)) * math.cos(a), (R + r * math.cos(b)) * math.sin(a), r * math.sin(b))))
        rings.append(ring)
    for i in range(seg):
        for j in range(sides):
            bm.faces.new((rings[i][j], rings[(i+1) % seg][j], rings[(i+1) % seg][(j+1) % sides], rings[i][(j+1) % sides]))
    o = ob(name, bm, m); o.location = loc; o.rotation_euler = rot; return o

def cyclorama(hexc, rough=.6, radius=5, depth=40, width=60):
    """Seamless studio backdrop: floor curving up into a back wall."""
    m = mat("Backdrop", hexc, 0, rough)
    bm = bmesh.new(); prof = [(-depth, 0)]
    for k in range(17):
        a = k / 16 * math.pi / 2
        prof.append(((8 - radius) + radius * math.sin(a), radius - radius * math.cos(a)))
    prof.append((8, 30))
    L = [bm.verts.new((-width / 2, y, z)) for y, z in prof]; R = [bm.verts.new((width / 2, y, z)) for y, z in prof]
    for i in range(len(prof) - 1): bm.faces.new((L[i], R[i], R[i+1], L[i+1]))
    return ob("Backdrop", bm, m)

def area(name, loc, target, energy, color, size):
    L = bpy.data.lights.new(name, "AREA"); L.energy = energy; L.color = lin(color)[:3]; L.size = size
    o = bpy.data.objects.new(name, L); col.objects.link(o); o.location = loc
    o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler(); return o

def camera(pos, look, lens=50, fstop=2.8, focus=None):
    cd = bpy.data.cameras.new("Cam"); cd.lens = lens
    c = bpy.data.objects.new("Cam", cd); col.objects.link(c); c.location = pos
    c.rotation_euler = (Vector(look) - Vector(pos)).to_track_quat("-Z", "Y").to_euler()
    f = bpy.data.objects.new("Focus", None); col.objects.link(f); f.location = focus or look
    cd.dof.use_dof = True; cd.dof.focus_object = f; cd.dof.aperture_fstop = fstop; scn.camera = c

def world(hexc, s=.5):
    w = bpy.data.worlds.new("W"); w.use_nodes = True; scn.world = w
    w.node_tree.nodes["Background"].inputs["Color"].default_value = lin(hexc)
    w.node_tree.nodes["Background"].inputs["Strength"].default_value = s

S = A.scene
if S == "kestrel":
    # Agent core: faceted glass shell, glowing blue core, three tool chips in orbit, one orange approval chip.
    cyclorama("#E7E6E1", .7); world("#EEEFEA", .35)
    glass = mat("Glass", "#F4F5F7", 0, .04, trans=1, ior=1.5)
    core = mat("Core", "#2B47C9", 0, .3, emit="#3D5BF0", strength=3.5)
    chip = mat("Chip", "#FBFBF9", 0, .25, coat=.5); ink = mat("Ink", "#16181B", 0, .4)
    blue = mat("BlueLine", "#3654D6", 0, .3, emit="#3654D6", strength=3)
    orange = mat("Orange", "#C8440F", 0, .3, emit="#E5621F", strength=5)
    sphere("Shell", 1.6, (0, 0, 2.2), glass, sub=2, ico=True)
    sphere("CoreGlow", .62, (0, 0, 2.2), core)
    torus("Orbit", 2.6, .012, (0, 0, 2.2), ink, rot=(math.radians(72), 0, math.radians(20)))
    torus("Orbit2", 2.25, .01, (0, 0, 2.2), ink, rot=(math.radians(64), math.radians(18), math.radians(-30)))
    for i, (ang, z, m2) in enumerate(((-.5, 2.9, blue), (1.7, 1.5, blue), (3.3, 2.6, orange))):
        p = (2.6 * math.cos(ang), 2.6 * math.sin(ang) * .35, z)
        rbox(f"Chip{i}", (1.3, .12, .62), p, chip, .05, rot=(0, 0, ang + math.pi / 2))
        rbox(f"ChipLine{i}a", (.7, .13, .07), (p[0], p[1], p[2] + .1), m2, .02, rot=(0, 0, ang + math.pi / 2))
        rbox(f"ChipLine{i}b", (.45, .13, .07), (p[0], p[1], p[2] - .1), ink, .02, rot=(0, 0, ang + math.pi / 2))
    torus("ApproveRing", .55, .03, (2.6 * math.cos(3.3), 2.6 * math.sin(3.3) * .35, 2.6), orange, rot=(math.pi / 2, 0, 3.3 + math.pi / 2))
    area("Key", (-6, -7, 8), (0, 0, 2), 2600, "#FFFFFF", 6); area("Rim", (6, 6, 5), (0, 0, 2), 1500, "#9DB0FF", 4)
    area("Fill", (6, -6, 2), (0, 0, 2), 500, "#FFE9DD", 5)
    camera((5.4, -10.4, 4.0), (0, 0, 2.2), 50, 3.5, (0, -1.6, 2.2))

elif S == "harbor":
    # Floating stack of deal cards; the top card carries the copilot sparkle and gradient edge.
    cyclorama("#E9E6F3", .7); world("#F4F0FF", .35)
    card = mat("Card", "#FFFFFF", 0, .18, coat=.8); frost = mat("Frost", "#EDE8FF", 0, .25, trans=.85, ior=1.3)
    purple = mat("Purple", "#6941C6", 0, .3, emit="#7F56D9", strength=6); blue = mat("Blue", "#2E90FA", 0, .3, emit="#2E90FA", strength=5)
    ink = mat("Ink", "#101828", 0, .4); green = mat("Green", "#17B26A", 0, .4); amber = mat("Amber", "#F79009", 0, .4)
    for i in range(4):
        z = 1.2 + i * .55; rz = math.radians(-14 + i * 7); m = frost if i < 3 else card
        rbox(f"Card{i}", (3.2, 2.0, .06), (i * .12, -i * .08, z), m, .12, rot=(math.radians(8), 0, rz))
        tag = (green, amber, blue, purple)[i]
        rbox(f"Pill{i}", (.6, .16, .07), (-1.0 + i * .12, .55 - i * .08, z + .03), tag, .07, rot=(math.radians(8), 0, rz))
        for k in range(3): rbox(f"Line{i}{k}", (1.6 - k * .35, .07, .07), (-.4 + i * .12, .1 - k * .28 - i * .08, z + .03), ink, .03, rot=(math.radians(8), 0, rz))
    top = 1.2 + 3 * .55
    torus("Edge", 1.95, .02, (.36, -.24, top), purple, rot=(math.radians(8), 0, 0))
    # four-point sparkle
    bm = bmesh.new(); pts = []
    for k in range(8):
        a = k / 8 * 2 * math.pi; r = .55 if k % 2 == 0 else .12
        pts.append(bm.verts.new((r * math.cos(a), r * math.sin(a), 0)))
    c0 = bm.verts.new((0, 0, .08)); c1 = bm.verts.new((0, 0, -.08))
    for k in range(8): bm.faces.new((pts[k], pts[(k+1) % 8], c0)); bm.faces.new((pts[(k+1) % 8], pts[k], c1))
    s = ob("Sparkle", bm, purple, smooth=False); s.location = (1.7, -.9, top + .9); s.rotation_euler = (math.radians(70), 0, math.radians(20))
    sphere("Spark2", .09, (2.3, -.5, top + 1.4), blue)
    area("Key", (-6, -7, 8), (0, 0, 2), 2400, "#FFFFFF", 6); area("Rim", (6, 6, 5), (0, 0, 2), 1400, "#C3B5FF", 4)
    area("Fill", (6, -6, 2), (0, 0, 2), 500, "#FFFFFF", 5)
    camera((5.2, -7.8, 5.2), (.3, 0, 2.3), 55, 3.2, (.36, -.24, top))

elif S == "tidewell":
    # Revenue skyline: twelve brushed-metal bars for twelve months, tops lit, a thin line tracing MRR.
    cyclorama("#141413", .55); world("#121211", .4)
    metal = mat("Brushed", "#8C8C88", 1, .28); top = mat("Top", "#2a78d6", 0, .3, emit="#3987e5", strength=1.6)
    aqua = mat("Aqua", "#1baf7a", 0, .3, emit="#1baf7a", strength=2.5); line = mat("Line", "#FFFFFF", 0, .3, emit="#DCE9FF", strength=1.2)
    mrr = [618, 645, 668, 690, 731, 769, 806, 850, 890, 950, 1012, 1080]
    pts = []
    for i, v in enumerate(mrr):
        h = (v - 500) / 600 * 4.2 + .4; x = -3.3 + i * .6
        rbox(f"Bar{i}", (.42, .42, h), (x, 0, h / 2), metal, .03)
        rbox(f"Cap{i}", (.43, .43, .06), (x, 0, h + .02), aqua if i == 11 else top, .02)
        pts.append((x, 0, h + .35))
    cu = bpy.data.curves.new("Trend", "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = .025
    sp = cu.splines.new("BEZIER"); sp.bezier_points.add(len(pts) - 1)
    for p, c in zip(sp.bezier_points, pts): p.co = c; p.handle_left_type = p.handle_right_type = "AUTO"
    o = bpy.data.objects.new("Trend", cu); col.objects.link(o); cu.materials.append(line)
    sphere("Now", .12, pts[-1], aqua)
    area("Key", (-6, -7, 9), (0, 0, 2), 2200, "#FFFFFF", 5); area("Rim", (7, 6, 6), (0, 0, 2), 1600, "#3987e5", 4)
    area("Fill", (6, -7, 2), (0, 0, 2), 400, "#FFFFFF", 5)
    camera((7.4, -10.6, 3.2), (.9, 0, 2.3), 46, 2.8, pts[9])

elif S == "dos":
    # Decision OS core: amber wireframe icosahedron, chart rings, project markers in state colors.
    cyclorama("#0B0E14", .5); world("#090C11", .4)
    amber = mat("Amber", "#F2A93B", 0, .3, emit="#F2A93B", strength=3.5); cyan = mat("Cyan", "#5CC8D6", 0, .3, emit="#5CC8D6", strength=4)
    violet = mat("Violet", "#CFC6F2", 0, .3, emit="#CFC6F2", strength=5); bone = mat("Bone", "#ECE7DC", 0, .4, emit="#ECE7DC", strength=.35)
    dark = mat("Dark", "#1A2130", .4, .35)
    bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=1, radius=1.2)
    o = ob("Core", bm, amber, smooth=False); o.location = (0, 0, 2.4)
    w = o.modifiers.new("Wire", "WIREFRAME"); w.thickness = .035
    sphere("Inner", .5, (0, 0, 2.4), amber, sub=1, ico=True)
    for r in (2.3, 3.6, 5.0): torus(f"Ring{r}", r, .008, (0, 0, 2.4), bone)
    for k in range(5):
        a = k / 5 * 2 * math.pi
        p = Vector((3.6 * math.cos(a), 3.6 * math.sin(a), 2.4))
        bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=4, radius1=.35, radius2=0, depth=.5)
        bmesh.ops.create_cone(bm, cap_ends=True, segments=4, radius1=0, radius2=.35, depth=.5)
        oc = ob(f"Proj{k}", bm, dark, smooth=False); oc.location = p
        ow = oc.modifiers.new("W", "WIREFRAME"); ow.thickness = .02; ow.use_replace = False
        for j, m2 in enumerate((amber, cyan, violet)):
            if (k + j) % 2 == 0: sphere(f"Item{k}{j}", .09, p + Vector((.6 * math.cos(j * 2.1), .3, .4 * math.sin(j * 2.1))), m2)
    area("Key", (-6, -7, 8), (0, 0, 2), 900, "#FFD9A8", 6); area("Rim", (6, 6, 5), (0, 0, 2), 900, "#5CC8D6", 4)
    camera((4.6, -10.8, 7.4), (0, 0, 2.2), 42, 2.8, (0, 0, 2.4))

scn.render.engine = "CYCLES"; scn.cycles.device = "CPU"; scn.cycles.samples = A.samples; scn.cycles.use_denoising = True
W, H = map(int, A.res.split("x")); scn.render.resolution_x = W; scn.render.resolution_y = H
try: scn.view_settings.view_transform = "AgX"; scn.view_settings.look = "AgX - Medium High Contrast"
except Exception: pass
if A.blend: bpy.ops.wm.save_as_mainfile(filepath=A.blend)
if A.still: scn.render.filepath = A.still; bpy.ops.render.render(write_still=True)
print("DONE", S)
