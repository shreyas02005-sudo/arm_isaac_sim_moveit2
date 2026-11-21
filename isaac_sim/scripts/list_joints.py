# Paste into Isaac Sim: Window > Script Editor, then Run.
# Lists every joint under /my_robot with its applied drive schemas, then every articulation root.
import omni.usd
from pxr import Usd, UsdPhysics
stage = omni.usd.get_context().get_stage()
for prim in Usd.PrimRange(stage.GetPrimAtPath("/my_robot")):
    if prim.IsA(UsdPhysics.Joint):
        drives = [s for s in prim.GetAppliedSchemas() if "Drive" in s]
        print(prim.GetPath(), prim.GetTypeName(), drives)
for prim in stage.Traverse():
    if prim.HasAPI(UsdPhysics.ArticulationRootAPI):
        print("ARTICULATION ROOT:", prim.GetPath())
