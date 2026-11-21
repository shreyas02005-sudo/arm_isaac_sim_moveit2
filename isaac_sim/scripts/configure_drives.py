# Paste into Isaac Sim: Window > Script Editor, then Run. Then File > Save.
# Imported joints default to Velocity drives with zero damping; MoveIt needs POSITION drives.
# USD angular drive gains are per DEGREE: 17.5 per degree is roughly 1000 per radian.
import omni.usd
from pxr import Usd, UsdPhysics
ANGULAR_STIFFNESS = 17.5
ANGULAR_DAMPING = 5.0      # started at 1.75; raised to remove end-of-move shaking
LINEAR_STIFFNESS = 1000.0
LINEAR_DAMPING = 100.0
stage = omni.usd.get_context().get_stage()
for prim in Usd.PrimRange(stage.GetPrimAtPath("/my_robot")):
    if prim.IsA(UsdPhysics.RevoluteJoint):
        d = UsdPhysics.DriveAPI.Apply(prim, "angular")
        d.CreateTypeAttr("force")
        d.CreateStiffnessAttr(ANGULAR_STIFFNESS)
        d.CreateDampingAttr(ANGULAR_DAMPING)
        print("angular drive set:", prim.GetPath())
    elif prim.IsA(UsdPhysics.PrismaticJoint):
        d = UsdPhysics.DriveAPI.Apply(prim, "linear")
        d.CreateTypeAttr("force")
        d.CreateStiffnessAttr(LINEAR_STIFFNESS)
        d.CreateDampingAttr(LINEAR_DAMPING)
        print("linear drive set:", prim.GetPath())
