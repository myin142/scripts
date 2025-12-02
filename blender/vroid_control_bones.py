import bpy
from mathutils import Vector, Euler
from math import radians

def move_layer(bone, coll):
    collection = None
    if not coll in bpy.context.object.data.collections:
        collection = bpy.context.object.data.collections.new(coll)
    else:
        collection = bpy.context.object.data.collections[coll]
    
    if bone != None:
        for c in bone.collections:
            c.unassign(bone)
        collection.assign(bone)

def hide_layer(coll):
    bpy.context.object.data.collections[coll].is_visible = False

def has_bone(name):
    return name in bpy.context.active_object.data.edit_bones

def get_bone(name):
    return bpy.context.active_object.data.edit_bones[name]

# Collections
DefaultLayer = "Bones"
HairLayer = "Hair"
HandLayer = "Hand"
ClothLayer = "Cloth"
IKLayer = "IK"
CTRLLayer = "CTRL"

HairBoneNames = "Hair"
HandBoneNames = ["Index", "Thumb", "Middle", "Ring", "Little"]

# Shapes (needs to be created beforehand!)
ik_shape = bpy.data.objects["cs_box"]
pole_shape = bpy.data.objects["cs_sphere"]
circle_shape = bpy.data.objects["cs_circle"]

# Bones should exist
RootBone = "Root"
EyeBone = "FaceEye"
HandBone = "_Hand"
FootBone = "_Foot"
ToeBone = "_Toe"
LegBone = "_LowerLeg"
ArmPoleExtendBone = "_UpperArm"
LegPoleExtendBone = "_UpperLeg"
HipsBone = "_Hips"
ArmsBone = "Arm_"
LegsBone = "Leg_"
HeadBone = "_Head"

# Custom Bones
BoneSidePrefix = "_L"
IKPrefix = ".IK"

EyeCtrlBone = "Eye.CTRL"
HipsIkBone = "Hips" + IKPrefix
HandIkBone = "Hand" + IKPrefix + BoneSidePrefix
FootCtrlIkBone = "Foot.CTRL" + BoneSidePrefix
FootAngleIkBone = "Foot.Angle" + BoneSidePrefix
FootIkBone = "Foot" + IKPrefix + BoneSidePrefix
ToeIkBone = "Toe" + IKPrefix + BoneSidePrefix
LegIkBone = "Leg" + IKPrefix + BoneSidePrefix
ArmPoleBone = "Arm.Pole" + IKPrefix + BoneSidePrefix
LegPoleBone = "Leg.Pole" + IKPrefix + BoneSidePrefix

# actual bone names, we can only use the names because switching between
# edit and pose mode will make the bone references invalid
hips_bone = None
eye_bone = None
hand_bone = None
leg_bone = None
toe_bone = None
head_bone = None
foot_bone = None
arm_pole_extend_bone = None
leg_pole_extend_bone = None

def find_bones():
    global hips_bone, head_bone, hand_bone, foot_bone, toe_bone, leg_bone, eye_bone, arm_pole_extend_bone, leg_pole_extend_bone

    bpy.ops.object.mode_set(mode='EDIT')
    for bone in bpy.context.active_object.data.edit_bones:
        if IKPrefix in bone.name:
            continue

        if HairBoneNames in bone.name:
            move_layer(bone, HairLayer)
        elif ArmsBone in bone.name or LegsBone in bone.name:
            move_layer(bone, IKLayer)
        else:
            move_layer(bone, DefaultLayer)
            
        for name in HandBoneNames:
            if name in bone.name:
                move_layer(bone, HandLayer)
                break

        if HipsBone in bone.name:
            hips_bone = bone.name
        elif HeadBone in bone.name:
            head_bone = bone.name

        if not bone.name.endswith(BoneSidePrefix):
            continue

        if EyeBone in bone.name:
            eye_bone = bone.name
            move_layer(bone, IKLayer)
        elif HandBone in bone.name:
            hand_bone = bone.name
            move_layer(bone, IKLayer)
        elif FootBone in bone.name:
            foot_bone = bone.name
            move_layer(bone, IKLayer)
        elif ToeBone in bone.name:
            toe_bone = bone.name
            move_layer(bone, IKLayer)
        elif LegBone in bone.name:
            leg_bone = bone.name
        elif ArmPoleExtendBone in bone.name:
            arm_pole_extend_bone = bone.name
        elif LegPoleExtendBone in bone.name:
            leg_pole_extend_bone = bone.name

    if not has_bone(RootBone):
        raise Exception("Root bone not found")
    if head_bone is None:
        raise Exception("Head bone not found")
    if hips_bone is None:
        raise Exception("Hips bone not found")
    if hand_bone is None:
        raise Exception("Hand bone not found")
    if foot_bone is None:
        raise Exception("Foot bone not found")
    if toe_bone is None:
        raise Exception("Toe bone not found")
    if leg_bone is None:
        raise Exception("Leg bone not found")
    if arm_pole_extend_bone is None:
        raise Exception("Arm pole extend bone not found")
    if leg_pole_extend_bone is None:
        raise Exception("Leg pole extend bone not found")

find_bones()

root = get_bone(RootBone)
hips = get_bone(hips_bone)
hand = get_bone(hand_bone)
foot = get_bone(foot_bone)
toe = get_bone(toe_bone)
leg = get_bone(leg_bone)
eye = get_bone(eye_bone)
arm_extend_pole = get_bone(arm_pole_extend_bone)
leg_extend_pole = get_bone(leg_pole_extend_bone)

def create_ik_bone(name, parent, head_pos, tail_pos):
    if has_bone(name):
        return get_bone(name)

    armature = bpy.context.active_object
    new_bone = armature.data.edit_bones.new(name)

    if parent:
        new_bone.parent = parent

    new_bone.head = head_pos
    new_bone.tail = tail_pos
    new_bone.use_connect = False
    new_bone.use_deform = False
    return new_bone

def create_ik_constraint(edit_bone, target, chain, pole = None, angle = -90, use_tail = True):
    bone = bpy.context.object.pose.bones[edit_bone]
    constraint = bone.constraints.new("IK")
    constraint.target = bpy.context.object
    constraint.subtarget = target
    constraint.chain_count = chain
    constraint.use_tail = use_tail

    if pole:
        constraint.pole_target = bpy.context.object
        constraint.pole_subtarget = pole
        constraint.pole_angle = radians(angle)

def create_rotation_constraint(edit_bone, target, lock_axis = False):
    bone = bpy.context.object.pose.bones[edit_bone]
    constraint = bone.constraints.new("COPY_ROTATION")
    constraint.target = bpy.context.object
    constraint.subtarget = target

    if lock_axis:
        constraint.use_y = False

def set_custom_shape(edit_bone, shape, rot = (0, 0, 0), scale = (1, 1, 1), pos = (0, 0, 0)):
    if shape:
        bone = bpy.context.object.pose.bones[edit_bone]
        bone.custom_shape = shape
        bone.custom_shape_rotation_euler = Euler(rot)
        bone.custom_shape_scale_xyz = Vector(scale)
        bone.custom_shape_translation = Vector(pos)

def create_root_ik():
    bpy.ops.object.mode_set(mode='EDIT')
    move_layer(root, CTRLLayer)
    bpy.ops.object.mode_set(mode='POSE')
    set_custom_shape(RootBone, circle_shape, (radians(90), 0, 0), (1.5, 1.5, 1.5))

def create_hip_ik():
    bpy.ops.object.mode_set(mode='EDIT')
    hips_ik_bone = create_ik_bone(HipsIkBone, root, hips.head, hips.tail + (hips.tail - hips.head) * 1)
    hips.use_connect = False
    hips.parent = hips_ik_bone
    move_layer(hips_ik_bone, CTRLLayer)

    bpy.ops.object.mode_set(mode='POSE')
    create_rotation_constraint(hips_bone, HipsIkBone)
    set_custom_shape(HipsIkBone, circle_shape, (radians(90), 0, 0), (5, 5, 5))

def create_arm_ik():
    bpy.ops.object.mode_set(mode='EDIT')
    hand_ik_bone = create_ik_bone(HandIkBone, root, hand.head, hand.tail + Vector((.1, 0, 0)))
    arm_pole_bone = create_ik_bone(ArmPoleBone, root, arm_extend_pole.tail + Vector((0, .2, 0)), arm_extend_pole.tail + Vector((0, .3, 0)))
    move_layer(hand_ik_bone, CTRLLayer)
    move_layer(arm_pole_bone, CTRLLayer)

    bpy.ops.object.mode_set(mode='POSE')
    create_ik_constraint(hand_bone, HandIkBone, 2, ArmPoleBone, 180, False)
    create_rotation_constraint(hand_bone, HandIkBone)
    set_custom_shape(HandIkBone, ik_shape, (0, 0, 0), (1, 1, 1), (0, .05, 0))
    set_custom_shape(ArmPoleBone, pole_shape, (0, 0, 0), (0.5, 0.5, 0.5))

def create_leg_ik():
    bpy.ops.object.mode_set(mode='EDIT')
    foot_ctrl_ik_bone = create_ik_bone(FootCtrlIkBone, root, Vector((foot.head[0], foot.head[1], 0)) + Vector((0, .05, 0)), Vector((foot.tail[0], foot.tail[1], 0))  + Vector((0, -.05, 0)))
    foot_angle_ik_bone = create_ik_bone(FootAngleIkBone, foot_ctrl_ik_bone, foot.tail, foot.head + (foot.head - foot.tail).normalized() * .1)
    foot_ik_bone = create_ik_bone(FootIkBone, foot_ctrl_ik_bone, foot.tail, foot.tail + Vector((0, 0, .1)))

    toe.tail[2] = toe.head[2]
    toe_ik_bone = create_ik_bone(ToeIkBone, foot_ctrl_ik_bone, toe.tail, toe.tail + Vector((0, 0, .1)))

    leg_ik_bone = create_ik_bone(LegIkBone, foot_angle_ik_bone, leg.tail, leg.tail + Vector((0, .1, 0)))
    leg_pole_bone = create_ik_bone(LegPoleBone, leg_ik_bone, leg.head + Vector((0, -.5, 0)), leg.head + Vector((0, -.6, 0)))

    move_layer(foot_ctrl_ik_bone, CTRLLayer)
    move_layer(foot_angle_ik_bone, CTRLLayer)
    move_layer(leg_pole_bone, CTRLLayer)
    move_layer(foot_ik_bone, IKLayer)
    move_layer(toe_ik_bone, IKLayer)
    move_layer(leg_ik_bone, IKLayer)

    bpy.ops.object.mode_set(mode='POSE')
    create_ik_constraint(leg_bone, LegIkBone, 2, LegPoleBone, -90)
    create_ik_constraint(foot_bone, FootIkBone, 1, ToeIkBone, -90)
    create_ik_constraint(toe_bone, ToeIkBone, 1)
    set_custom_shape(FootCtrlIkBone, circle_shape, (0, 0, 0), (1, 2, 1), (0, .1, 0))
    set_custom_shape(LegPoleBone, pole_shape)

def create_eye_ctrl():
    bpy.ops.object.mode_set(mode='EDIT')
    eye_pos = Vector((0, eye.head[1], eye.head[2]))
    eye_ctrl_bone = create_ik_bone(EyeCtrlBone, root, eye_pos, eye_pos + Vector((0, -.1, 0)))
    eye_ctrl_bone.parent = get_bone(head_bone)
    move_layer(eye_ctrl_bone, CTRLLayer)

    bpy.ops.object.mode_set(mode='POSE')
    create_rotation_constraint(eye_bone, EyeCtrlBone, True)

def symmetrize_bones():
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.object.select_pattern(pattern=f'*{BoneSidePrefix}')
    bpy.ops.armature.symmetrize()

create_root_ik()
create_hip_ik()
create_arm_ik()
create_leg_ik()
create_eye_ctrl()
# symmetrize_bones()

# hide_layer(IKLayer)
# hide_layer(HairLayer)