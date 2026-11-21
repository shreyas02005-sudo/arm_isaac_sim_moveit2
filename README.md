# 6-DOF Arm: MoveIt 2 + NVIDIA Isaac Sim on Windows

A custom 6-DOF robot arm with a parallel gripper, planned with **MoveIt 2** (ROS 2 Jazzy) and executed
in **NVIDIA Isaac Sim 6.0.1**, all running natively on **Windows**. A small Python trajectory bridge
connects MoveIt's `FollowJointTrajectory` actions to Isaac's articulation, and a C++ program drives a full
pick-style sequence through the MoveIt API.

> Demo video: [Google Drive folder](https://drive.google.com/drive/folders/19aJNf1vs4xFFC0ChF1kgxgATa8SNTinV?usp=sharing)

## What it does

```
home -> pose_2 -> gripper_closed -> pose_1 -> gripper_open
```

planned by MoveIt (OMPL) and followed by the simulated arm in Isaac Sim, with joint states fed back to MoveIt.

![Isaac Sim](media/isaac_simulation.jpeg)

## Architecture

```
 MoveIt 2: move_group, RViz, sequence_demo (C++)
        |  FollowJointTrajectory actions
        |    /arm_controller/follow_joint_trajectory
        |    /gripper_controller/follow_joint_trajectory
        v
 bridge/isaac_trajectory_bridge.py  --- /isaac_joint_commands (JointState) --->  Isaac Sim
        ^                                                                   Action Graph ->
        |                                                                   Articulation Controller
        +---------- /joint_states  <---  /isaac_joint_states (JointState) ---  (arm at /my_robot/Geometry)

 Transport: rmw_zenoh_cpp through a Zenoh router (`pixi run zenoh`)
```

The bridge replaces `ros2_control_node`, which crashes on this Windows setup (details in
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)).

## Tested environment

| Item | Version |
|---|---|
| OS | Windows 11 (preview build 26300) |
| GPU / RAM | NVIDIA RTX 4060 Laptop (8 GB VRAM), 16 GB RAM |
| Isaac Sim | 6.0.1 (installed through pixi: `isaacsim==6.0.1.0`) |
| ROS 2 | Jazzy via RoboStack/pixi, MoveIt 2 (`ros-jazzy-moveit >=2.12.4`) |
| RMW | `rmw_zenoh_cpp` |
| Build | colcon + CMake + Ninja, Visual Studio Build Tools (MSVC 19.51) |

## Repository layout

| Path | What it is |
|---|---|
| `bridge/` | `isaac_trajectory_bridge.py` (MoveIt-to-Isaac bridge) and `isaac_arm.launch.xml` |
| `isaac_sim/scripts/` | Script Editor snippets: configure joint drives, list joints, optional gravity tweak |
| `isaac_sim/scene/` | The saved Isaac scene (`my_robot_1/my_robot.usda`) |
| `overlay/` | Files that **replace or add to** the arm's ROS packages (see `overlay/README.md`) |
| `ros2_ws/src/` | The arm's ROS packages (copy in from your machine; see `docs/SETUP_WINDOWS.md`) |
| `scripts/stop_arm.bat` | Clean shutdown of the MoveIt/bridge stack without closing Isaac |
| `docs/` | Setup, Isaac scene, architecture, troubleshooting |

## Quick start

Full instructions: [docs/SETUP_WINDOWS.md](docs/SETUP_WINDOWS.md). Once everything is built, run each of these
in its own Command Prompt, in this order (`WS` = your pixi workspace, e.g. `C:\IsaacSim-ros_workspaces\jazzy_ws`):

```cmd
:: 1. Zenoh router
cd /d WS
pixi run zenoh

:: 2. Isaac Sim, then open isaac_sim\scene\my_robot_1\my_robot.usda and press Play
cd /d WS
pixi run sim

:: 3. MoveIt + RViz + bridge (after Isaac is in Play)
cd /d WS
pixi run ros2 launch C:\arm_pkgs\isaac_arm.launch.xml

:: 4. The demo sequence
cd /d WS
pixi run ros2 run my_robot_commander_cpp sequence_demo
```

Stop the stack with `scripts\stop_arm.bat` (press Ctrl+C once in the launch window first and wait for the prompt).

## Named poses (from the SRDF)

| Group | State | Values |
|---|---|---|
| arm | `home` | all joints 0 |
| arm | `pose_1` | 0, 0.7873, 1.1464, 0.2255, 0.9108, 1.3364 |
| arm | `pose_2` | 0, 0.1796, 1.4503, 0, -0.9281, 2.7597 |
| gripper | `gripper_open` | left finger 0 |
| gripper | `gripper_half_closed` | left finger 0.04 |
| gripper | `gripper_closed` | left finger 0.06 |

## Known limitations

- `ros2_control_node` is not used (Windows crash); control is through the bridge, which is open-loop with a settle check.
- RViz shows `No active joints or end effectors found for group 'arm'` because the plain `rviz2` node is not given the kinematics parameters, so the **draggable end-effector marker is unavailable**. Planning from the MotionPlanning panel and from code works.
- `commander_template.cpp` (the original commander) is not built on Windows because it needs `example_interfaces`, which is not in the pixi environment. Only `test_moveit` and `sequence_demo` are built.
- Isaac Sim ignores the URDF `mimic` rule, so the bridge mirrors the finger itself.
- Connecting Isaac Sim on Windows to ROS inside WSL2 over DDS was tried at length and never worked. Do not use that path.

## Troubleshooting

See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md).

## Author

Shreyas R ([@shreyas02005-sudo](https://github.com/shreyas02005-sudo))

## License

Apache-2.0, see [LICENSE](LICENSE).
