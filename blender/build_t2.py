# Builds Transformer T2 in Blender: detailed model, warm studio lighting, camera.
# Usage: python3 build_t2.py [--still out.png] [--glb out.glb] [--blend out.blend] [--samples N] [--res WxH]
import bpy, bmesh, math, sys, argparse
from mathutils import Vector, Matrix

ap = argparse.ArgumentParser()
ap.add_argument("--still"); ap.add_argument("--glb"); ap.add_argument("--blend")
ap.add_argument("--samples", type=int, default=96); ap.add_argument("--res", default="1600x1200")
ap.add_argument("--cam", default="hero")
A = ap.parse_args(sys.argv[1:])

bpy.ops.wm.read_factory_settings(use_empty=True)
scn = bpy.context.scene
model = bpy.data.collections.new("Model"); scn.collection.children.link(model)
env = bpy.data.collections.new("Env"); scn.collection.children.link(env)

def lin(h):
    h = h.lstrip("#"); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((x + .055) / 1.055) ** 2.4 if x > .04045 else x / 12.92 for x in c) + (1,)

def mat(name, hexc, metal=0., rough=.5, coat=0., emit=None, strength=0., bump=0., grunge=None):
    m = bpy.data.materials.new(name); m.use_nodes = True; m["hex"] = hexc; m["rough"] = rough
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = lin(hexc)
    b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = rough
    if coat: b.inputs["Coat Weight"].default_value = coat
    if emit:
        b.inputs["Emission Color"].default_value = lin(emit)
        b.inputs["Emission Strength"].default_value = strength
    if grunge:
        n = nt.nodes.new("ShaderNodeTexNoise"); n.inputs["Scale"].default_value = 2.5; n.inputs["Detail"].default_value = 10
        cr = nt.nodes.new("ShaderNodeValToRGB"); cr.color_ramp.elements[0].position = .42; cr.color_ramp.elements[1].position = .62
        mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"
        mix.inputs["A"].default_value = lin(hexc); mix.inputs["B"].default_value = lin(grunge)
        nt.links.new(n.outputs["Fac"], cr.inputs["Fac"]); nt.links.new(cr.outputs["Color"], mix.inputs["Factor"])
        nt.links.new(mix.outputs["Result"], b.inputs["Base Color"])
        rr = nt.nodes.new("ShaderNodeMapRange"); rr.inputs["To Min"].default_value = rough - .12; rr.inputs["To Max"].default_value = rough + .2
        nt.links.new(n.outputs["Fac"], rr.inputs["Value"]); nt.links.new(rr.outputs["Result"], b.inputs["Roughness"])
    if bump:
        n = nt.nodes.new("ShaderNodeTexNoise"); n.inputs["Scale"].default_value = 40
        bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = bump
        nt.links.new(n.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    return m

M = dict(
    paint=mat("Paint", "#2F241D", .45, .46, coat=.15, grunge="#3E2E22"),
    gauge=mat("GaugeFace", "#F4E7D7", 0., .3, emit="#F4E7D7", strength=.4),
    warn=mat("WarnSign", "#E07A34", 0., .45),
    bronze=mat("Bronze", "#B07A48", 1., .3),
    copper=mat("Copper", "#C98A5A", 1., .2),
    porcelain=mat("Porcelain", "#4A2C1C", 0., .1, coat=.6),
    steel=mat("Steel", "#2A211B", .6, .55, grunge="#3A2B20"),
    fin=mat("Fin", "#3A2C22", .5, .5),
    concrete=mat("Concrete", "#2E241D", 0., .9, bump=.15),
    ground=mat("Ground", "#140F0C", 0., .85, bump=.08),
    teal=mat("GlowTeal", "#6FE3D0", 0., .4, emit="#6FE3D0", strength=8),
    orange=mat("GlowOrange", "#E07A34", 0., .4, emit="#E07A34", strength=8),
    ring=mat("ChartRing", "#C08A57", 0., .5, emit="#C08A57", strength=.6),
)

def link(o, coll=model):
    for c in o.users_collection: c.objects.unlink(o)
    coll.objects.link(o); return o

def obj_from_bm(name, bm, m, coll=model, smooth=False, bevel=0., segs=2):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    if smooth:
        for p in me.polygons: p.use_smooth = True
    o = bpy.data.objects.new(name, me); coll.objects.link(o); me.materials.append(m)
    if bevel:
        bv = o.modifiers.new("Bevel", "BEVEL"); bv.width = bevel; bv.segments = segs; bv.limit_method = "ANGLE"
    return o

def bm_box(bm, size, loc, rot=None):
    r = bmesh.ops.create_cube(bm, size=1)
    vs = r["verts"]; S = Matrix.Diagonal((*size, 1))
    mtx = Matrix.Translation(loc) @ (rot.to_4x4() if rot else Matrix()) @ S
    bmesh.ops.transform(bm, matrix=mtx, verts=vs)

def box(name, size, loc, m, bevel=.03, coll=model):
    bm = bmesh.new(); bm_box(bm, size, loc); return obj_from_bm(name, bm, m, coll, bevel=bevel)

def bm_cyl(bm, r, depth, loc, axis="Z", seg=32, r2=None):
    res = bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r2 if r2 is not None else r, depth=depth)
    rot = {"Z": Matrix(), "X": Matrix.Rotation(math.pi/2, 4, "Y"), "Y": Matrix.Rotation(math.pi/2, 4, "X")}[axis]
    bmesh.ops.transform(bm, matrix=Matrix.Translation(loc) @ rot, verts=res["verts"])

def cyl(name, r, depth, loc, m, axis="Z", seg=48, r2=None, bevel=.015):
    bm = bmesh.new(); bm_cyl(bm, r, depth, loc, axis, seg, r2)
    o = obj_from_bm(name, bm, m, smooth=True, bevel=bevel)
    return o

def lathe(name, prof, loc, m, seg=64):
    """Revolve a (radius, z) profile around Z."""
    bm = bmesh.new(); rings = []
    for (r, z) in prof:
        ring = []
        for i in range(seg):
            a = i / seg * 2 * math.pi
            ring.append(bm.verts.new((loc[0] + r * math.cos(a), loc[1] + r * math.sin(a), loc[2] + z)))
        rings.append(ring)
    for k in range(len(rings) - 1):
        for i in range(seg):
            j = (i + 1) % seg
            bm.faces.new((rings[k][i], rings[k][j], rings[k+1][j], rings[k+1][i]))
    bm.faces.new(list(reversed(rings[0]))); bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return obj_from_bm(name, bm, m, smooth=True)

def torus(name, R, r, loc, m, rot=(0, 0, 0), coll=model):
    bm = bmesh.new(); seg, sides = 64, 12
    rings = []
    for i in range(seg):
        a = i / seg * 2 * math.pi
        ring = []
        for j in range(sides):
            b = j / sides * 2 * math.pi
            ring.append(bm.verts.new(((R + r * math.cos(b)) * math.cos(a), (R + r * math.cos(b)) * math.sin(a), r * math.sin(b))))
        rings.append(ring)
    for i in range(seg):
        for j in range(sides):
            bm.faces.new((rings[i][j], rings[(i+1) % seg][j], rings[(i+1) % seg][(j+1) % sides], rings[i][(j+1) % sides]))
    o = obj_from_bm(name, bm, m, coll, smooth=True)
    o.location = loc; o.rotation_euler = rot
    return o

def tube(name, pts, r, m):
    cu = bpy.data.curves.new(name, "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = r; cu.bevel_resolution = 4
    sp = cu.splines.new("BEZIER"); sp.bezier_points.add(len(pts) - 1)
    for p, c in zip(sp.bezier_points, pts):
        p.co = c; p.handle_left_type = p.handle_right_type = "AUTO"
    o = bpy.data.objects.new(name, cu); model.objects.link(o); cu.materials.append(m); return o

# ---------------- model (front faces -Y, toward camera) ----------------
box("Plinth", (10.5, 7, .6), (0, 0, .3), M["concrete"], .08)
box("PlinthTrim", (10.6, 7.1, .04), (0, 0, .62), M["bronze"], .01)
box("Tank", (6, 3.4, 4.2), (0, 0, 2.75), M["paint"], .14, )
box("Lid", (6.5, 3.9, .22), (0, 0, 4.92), M["bronze"], .05)
box("Skirt", (6.3, 3.7, .18), (0, 0, .74), M["bronze"], .04)

# bolts on the lid flange
bm = bmesh.new()
for x in [-3.05 + i * .305 for i in range(21)]:
    for y in (-1.8, 1.8): bm_cyl(bm, .045, .08, (x, y, 5.06), seg=6)
for y in [-1.5 + i * .3 for i in range(11)]:
    for x in (-3.08, 3.08): bm_cyl(bm, .045, .08, (x, y, 5.06), seg=6)
obj_from_bm("LidBolts", bm, M["bronze"])

# stiffener ribs front and back
bm = bmesh.new()
for y in (-1.74, 1.74):
    for k in range(9): bm_box(bm, (.12, .16, 3.9), (-2.6 + k * .65, y, 2.75))
obj_from_bm("Ribs", bm, M["fin"], bevel=.02)

# radiator banks + headers
bm = bmesh.new()
for s in (-1, 1):
    for k in range(16): bm_box(bm, (.05, 2.6, 3.3), (s * (3.38 + k * .13), 0, 2.65))
obj_from_bm("RadiatorFins", bm, M["fin"], bevel=.012)
for s in (-1, 1):
    for z in (1.05, 4.25): cyl(f"Header_{s}_{z}", .12, 2.5, (s * 4.3, 0, z), M["bronze"], axis="X")
    for y in (-1.1, 1.1): box(f"RadFrame_{s}_{y}", (2.2, .06, .1), (s * 4.3, y, .78), M["steel"], .01)

# fans under radiators
for s in (-1, 1):
    for y in (-.7, .7):
        n = f"Fan_{'L' if s < 0 else 'R'}{'F' if y < 0 else 'B'}"
        torus(n + "_Shroud", .42, .05, (s * 4.3, y, .5), M["steel"])
        cyl(n + "_Hub", .09, .12, (s * 4.3, y, .5), M["bronze"])
        bm = bmesh.new()
        for b in range(5):
            a = b / 5 * 2 * math.pi
            bm_box(bm, (.34, .11, .015), (.19 * math.cos(a), .19 * math.sin(a), 0), Matrix.Rotation(a, 3, "Z") @ Matrix.Rotation(.35, 3, "X"))
        o = obj_from_bm(n + "_Blades", bm, M["bronze"]); o.location = (s * 4.3, y, .5)

# conservator, supports, Buchholz pipe, relay
cyl("Conservator", .62, 4.4, (-.4, 1.15, 6.15), M["paint"], axis="X", seg=64)
for x, sgn in ((-2.6, -1), (1.8, 1)):
    bm = bmesh.new(); r = bmesh.ops.create_uvsphere(bm, u_segments=48, v_segments=24, radius=.62)
    bmesh.ops.delete(bm, geom=[v for v in r["verts"] if v.co.x * sgn < -1e-4], context="VERTS")
    bmesh.ops.translate(bm, vec=(x, 1.15, 6.15), verts=bm.verts)
    obj_from_bm(f"ConsEnd_{sgn}", bm, M["paint"], smooth=True)
for x in (-1.8, 1.0):
    box(f"ConsSupport_{x}", (.14, .14, 1.15), (x, 1.15, 5.5), M["steel"], .01)
    torus(f"ConsBand_{x}", .64, .03, (x, 1.15, 6.15), M["bronze"], rot=(0, math.pi/2, 0))
tube("Buchholz", [(1.1, 1.15, 5.6), (1.1, .9, 5.3), (1.1, .5, 5.06)], .06, M["copper"])
box("Relay", (.28, .22, .22), (1.1, .95, 5.35), M["steel"], .02)
cyl("OilGauge", .14, .05, (1.3, .52, 6.15), M["bronze"], axis="Y")
cyl("OilGaugeFace", .1, .055, (1.3, .515, 6.15), M["teal"], axis="Y")

# HV bushings: turned porcelain with sloped sheds, bronze flange, copper cap, energy ring
def bushing(tag, x, y, z0, height=2.9, sheds=13, big=.40, small=.31, core=.19, ring_mat=None):
    lathe(f"Bushing{tag}_Flange", [(0, 0), (.5, 0), (.5, .06), (.44, .12), (.42, .28), (0, .28)], (x, y, z0), M["bronze"])
    prof = [(0, .26), (core, .26)]
    step = (height - .5) / sheds
    for k in range(sheds):
        zb = .4 + k * step; R = big if k % 2 == 0 else small
        prof += [(core, zb), (R, zb + .035), (R - .015, zb + .06), (core + .02, zb + step * .55)]
    prof += [(core, height + .1), (0, height + .1)]
    lathe(f"Bushing{tag}_Porcelain", prof, (x, y, z0), M["porcelain"], seg=72)
    lathe(f"Bushing{tag}_Cap", [(0, 0), (.25, 0), (.25, .3), (.2, .34), (.12, .36), (0, .36)], (x, y, z0 + height + .1), M["copper"])
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=12, radius=.13)
    bmesh.ops.translate(bm, vec=(x, y, z0 + height + .55), verts=bm.verts); obj_from_bm(f"Bushing{tag}_Terminal", bm, M["copper"], smooth=True)
    if ring_mat: torus(f"Ring_{tag}", .44, .022, (x, y, z0 + 1.5), ring_mat)

for tag, x in (("A", -1.7), ("B", 0.), ("C", 1.7)):
    bushing(tag, x, -.7, 5.03, ring_mat=M["orange"] if tag == "B" else M["teal"])
    tube(f"Busbar{tag}", [(x, -.7, 8.6), (x * .92, .6, 10.0), (x * .8, 4.2, 10.55)], .05, M["copper"])
for tag, x in (("a", -1.2), ("b", 0.), ("c", 1.2)):
    bushing(tag, x, .3, 5.03, height=1.0, sheds=4, big=.24, small=.2, core=.12)

# gantry
for x in (-3.4, 3.4):
    box(f"GantryPost_{x}", (.32, .32, 11), (x, 4.4, 5.5), M["steel"], .02)
box("GantryBeamTop", (7.6, .34, .34), (0, 4.4, 10.7), M["steel"], .02)
box("GantryBeamLow", (7.6, .18, .18), (0, 4.4, 9.7), M["steel"], .01)
bm = bmesh.new()
for k in range(6): bm_box(bm, (.06, .06, 1.35), (-3.0 + k * 1.2, 4.4, 10.2), Matrix.Rotation(.7 if k % 2 else -.7, 3, "Y"))
obj_from_bm("GantryLattice", bm, M["steel"])
for x in (-1.36, 0, 1.36):
    lathe(f"StringInsulator_{x}", [(0, 0)] + sum(([(.06, -k * .12), (.16, -k * .12 - .03), (.06, -k * .12 - .06)] for k in range(5)), []) + [(0, -.66)], (x, 4.2, 10.55), M["porcelain"], seg=32)

# control cabinet
box("Cabinet", (1.3, .8, 1.9), (3.7, -2.75, 1.6), M["steel"], .05)
box("CabinetDoorLine", (.02, .6, 1.6), (4.36, -2.75, 1.6), M["bronze"], 0)
box("CabinetHandle", (.04, .04, .3), (4.38, -2.5, 1.6), M["bronze"], .01)
bm = bmesh.new()
for k in range(6): bm_box(bm, (.5, .02, .04), (3.7, -3.16, 2.2 - k * .09))
obj_from_bm("CabinetVents", bm, M["bronze"])
bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=12, v_segments=8, radius=.05); bmesh.ops.translate(bm, vec=(3.95, -3.16, 2.35), verts=bm.verts)
obj_from_bm("LED", bm, M["teal"], smooth=True)

# nameplate + engraved label
box("Nameplate", (1.5, .03, .7), (-1.6, -1.86, 3.2), M["bronze"], .01)
for txt, size, z in (("T2", .34, 3.24), ("230/115 kV  240 MVA", .1, 3.0)):
    cu = bpy.data.curves.new("txt", "FONT"); cu.body = txt; cu.size = size; cu.extrude = .006; cu.align_x = "CENTER"
    o = bpy.data.objects.new("Label_" + txt[:2], cu); model.objects.link(o); cu.materials.append(M["steel"])
    o.location = (-1.6, -1.88, z); o.rotation_euler = (math.pi/2, 0, 0)


# ---------------- details: valves, gauges, lugs, earthing, conduit, signage ----------------
def handwheel(name, loc):
    torus(name + "_Wheel", .16, .022, loc, M["bronze"], rot=(math.pi/2, 0, 0))
    bm = bmesh.new()
    for k in range(3):
        bm_box(bm, (.3, .02, .02), (0, 0, 0), Matrix.Rotation(k * math.pi / 3, 3, "Y"))
    o = obj_from_bm(name + "_Spokes", bm, M["bronze"]); o.location = loc
    cyl(name + "_Stem", .04, .25, (loc[0], loc[1] + .12, loc[2]), M["steel"], axis="Y")
    cyl(name + "_Body", .12, .18, (loc[0], loc[1] + .25, loc[2]), M["bronze"], axis="Y")
handwheel("DrainValve", (2.3, -1.98, 1.2))
handwheel("FilterValve", (-2.3, -1.98, 4.3))
for i, (x, z) in enumerate(((.325, 3.6), (.975, 3.6))):
    cyl(f"Gauge{i}_Bezel", .2, .07, (x, -1.86, z), M["bronze"], axis="Y")
    cyl(f"Gauge{i}_Post", .05, .12, (x, -1.78, z), M["steel"], axis="Y")
    cyl(f"Gauge{i}_Face", .16, .075, (x, -1.865, z), M["gauge"], axis="Y")
    nd = box(f"Gauge{i}_Needle", (.026, .012, .14), (0, 0, .055), M["steel"], 0); nd.location = (x, -1.91, z); nd.rotation_euler = (0, -.6 - i * .5, 0)
    cyl(f"Gauge{i}_Pin", .018, .02, (x, -1.915, z), M["steel"], axis="Y")
    bm = bmesh.new()
    for k in range(11):
        a = math.radians(-135 + k * 27)
        bm_box(bm, (.006, .005, .03 if k % 5 else .045), (x + .125 * math.sin(a), -1.905, z + .125 * math.cos(a)), Matrix.Rotation(a, 3, "Y"))
    obj_from_bm(f"Gauge{i}_Ticks", bm, M["steel"])
for x in (-3.0, 3.0):
    for y in (-1.6, 1.6):
        lathe(f"Lug_{x}_{y}", [(0, 0), (.09, 0), (.09, .16), (.05, .2), (0, .2)], (x, y, 5.03), M["bronze"], seg=16)
tube("EarthStrap", [(-2.9, -1.75, 1.0), (-3.4, -2.6, .7), (-3.9, -3.2, .66)], .03, M["copper"])
box("EarthBar", (.5, .08, .04), (-3.9, -3.25, .66), M["copper"], .005)
tube("Conduit", [(3.05, -2.4, 2.4), (3.05, -1.9, 2.6), (3.0, -1.72, 2.9)], .06, M["steel"])
box("WarnPlate", (.42, .015, .36), (3.7, -3.16, 1.15), M["warn"], .01)

# ---------------- environment ----------------
g = box("Ground", (120, 120, .1), (0, 0, -.05), M["ground"], 0, coll=env)
for r in (8, 11.5, 15): torus(f"ChartRing_{r}", r, .012, (0, 0, .01), M["ring"], coll=env)

def area(name, loc, target, energy, color, size):
    L = bpy.data.lights.new(name, "AREA"); L.energy = energy; L.color = lin(color)[:3]; L.size = size
    o = bpy.data.objects.new(name, L); env.objects.link(o); o.location = loc
    d = Vector(target) - Vector(loc); o.rotation_euler = d.to_track_quat("-Z", "Y").to_euler(); return o
area("Key", (-10, -11, 15), (0, 0, 3), 9000, "#FFD2A8", 8)
area("Top", (0, -2, 18), (0, 0, 4), 3500, "#FFE6CC", 9)
area("Rim", (11, 12, 9), (0, 0, 4), 1300, "#6FE3D0", 5)
area("Fill", (9, -13, 4), (0, 0, 3), 1400, "#E9A46E", 6)
area("Under", (0, -6, .6), (0, 0, 1.5), 600, "#E9A46E", 3)
w = bpy.data.worlds.new("World"); w.use_nodes = True; scn.world = w
w.node_tree.nodes["Background"].inputs["Color"].default_value = lin("#120E0B")
w.node_tree.nodes["Background"].inputs["Strength"].default_value = .6

# camera
CAMS = {"hero": ((12.4, -14.6, 8.2), (0, 0, 4.4), 46),
        "detail": ((4.2, -6.2, 3.6), (.6, -1.7, 3.4), 70),
        "macro": ((1.6, -4.2, 9.6), (0, -.7, 8.2), 50),
        "front": ((0, -24, 7.5), (0, 0, 4.2), 55)}
pos, look, lens = CAMS[A.cam]
cd = bpy.data.cameras.new("Cam"); cd.lens = lens; cd.sensor_width = 36
cam = bpy.data.objects.new("Cam", cd); env.objects.link(cam); cam.location = pos
cam.rotation_euler = (Vector(look) - Vector(pos)).to_track_quat("-Z", "Y").to_euler()
foc = bpy.data.objects.new("Focus", None); env.objects.link(foc); foc.location = (0, -.7, 7.0)
cd.dof.use_dof = True; cd.dof.focus_object = foc; cd.dof.aperture_fstop = {"hero": 5.6, "detail": 2.2}.get(A.cam, 2.0)
if A.cam == "detail": foc.location = (.6, -1.87, 3.6)
scn.camera = cam

# render settings
scn.render.engine = "CYCLES"; scn.cycles.device = "CPU"
scn.cycles.samples = A.samples; scn.cycles.use_denoising = True
scn.cycles.max_bounces = 6
W, H = map(int, A.res.split("x")); scn.render.resolution_x = W; scn.render.resolution_y = H
try:
    scn.view_settings.view_transform = "AgX"; scn.view_settings.look = "AgX - Medium High Contrast"; scn.view_settings.exposure = .45
except Exception:
    pass

if A.blend: bpy.ops.wm.save_as_mainfile(filepath=A.blend)
if A.glb:
    # web export: Blender-only node effects (weathering) don't carry into glTF, so bake them to flat values
    for m in bpy.data.materials:
        if not m.use_nodes or "hex" not in m: continue
        b = m.node_tree.nodes.get("Principled BSDF")
        for inp, val in (("Base Color", lin(m["hex"])), ("Roughness", m["rough"])):
            for l in list(b.inputs[inp].links): m.node_tree.links.remove(l)
            b.inputs[inp].default_value = val
    for o in bpy.data.objects: o.select_set(o.name in model.all_objects)
    bpy.context.view_layer.objects.active = model.all_objects[0]
    bpy.ops.export_scene.gltf(filepath=A.glb, export_format="GLB", use_selection=True, export_apply=True, export_yup=True)
if A.still:
    scn.render.filepath = A.still; bpy.ops.render.render(write_still=True)
print("DONE", len(model.all_objects), "objects")
