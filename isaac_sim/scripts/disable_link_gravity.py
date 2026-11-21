# OPTIONAL and NOT CONFIRMED on Isaac Sim 6.0.1 (the PhysxSchema import was never verified).
# Try only if the arm sags under gravity even after configure_drives.py.
import omni.usd
from pxr import Usd, UsdPhysics, PhysxSchema
stage = omni.usd.get_context().get_stage()
for prim in Usd.PrimRange(stage.GetPrimAtPath("/my_robot")):
    if prim.HasAPI(UsdPhysics.RigidBodyAPI):
        PhysxSchema.PhysxRigidBodyAPI.Apply(prim).CreateDisableGravityAttr(True)
        print("gravity off:", prim.GetPath())
