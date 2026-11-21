# Building the Isaac Sim scene

Do this once, then save the scene (File > Save As) and reuse it.

## 1. Generate a plain URDF

Isaac's importer reads URDF, not xacro:

```cmd
cd /d WS
pixi run xacro src\my_robot_description\urdf\my_robot.urdf.xacro -o C:\arm_pkgs\my_robot.urdf
```

## 2. Import

`File > Import`, choose `my_robot.urdf`. In the dialog: **Base Type = Fixed**; leave *Collision From Visuals* and
*Allow Self-Collision* off (the URDF has its own collision boxes); leave the ROS package list empty (no meshes). Import.
The robot appears under `/my_robot`.

Add a ground plane (`Create > Physics > Ground Plane`) and make sure it is **outside** `/my_robot` (drag it under `World`).

## 3. Know your articulation root

For this robot it is **`/my_robot/Geometry`**, not `/my_robot`. Confirm with `isaac_sim/scripts/list_joints.py`.
Using `/my_robot` produces `Pattern '/my_robot' did not match any articulations` and nothing publishes.
The Gain Tuner cannot select this path (it lists only two joints and defaults to Velocity mode), so do not use it.

## 4. Configure the drives

Run `isaac_sim/scripts/configure_drives.py` in `Window > Script Editor` (paste with no leading indentation on line 1).
It sets position drives: angular stiffness 17.5 and damping 5.0 per degree on the revolute joints, and linear
stiffness 1000 and damping 100 on both finger joints. Tuning notes: sag means raise stiffness; shaking means raise damping.
`disable_link_gravity.py` is optional and was not confirmed on 6.0.1.

## 5. Action Graph (`Window > Graph Editors > Action Graph`)

Node display names differ slightly between versions; search by the key words.

| Node | Settings |
|---|---|
| On Playback Tick | none |
| ROS2 Context | Domain ID 0 |
| Isaac Read Simulation Time | none |
| ROS2 Subscribe Joint State | topic `/isaac_joint_commands` |
| ROS2 Publish Joint State | topic `/isaac_joint_states`, target prim `/my_robot/Geometry` |
| Articulation Controller | target prim `/my_robot/Geometry` |

Wiring:
- On Playback Tick `Tick` to the Exec In of the Subscribe, Publish and Articulation Controller nodes.
- ROS2 Context `Context` to the `Context` input of the Subscribe and Publish nodes.
- Isaac Read Simulation Time `Simulation Time` to Publish Joint State `Time Stamp`.
- Subscribe `Joint Names` to Articulation Controller `Joint Names`; Subscribe `Position Command` to Articulation Controller `Position Command`.

(The Isaac ROS 2 clock graph can also be created from `Tools > Robotics > ROS 2 OmniGraphs > Clock`.)

## 6. Test without MoveIt

With Zenoh and Isaac (Play) running:

```cmd
cd /d WS
pixi run ros2 topic echo /isaac_joint_states --once --field position
pixi run ros2 topic pub -r 2 /isaac_joint_commands sensor_msgs/msg/JointState "{name: ['joint1'], position: [0.5]}"
```

The first prints 8 values (joint1-joint6 and both fingers). The second should rotate `joint1` to about 0.5 rad
(check with the echo command in a second window). Stop publishing with Ctrl+C before running MoveIt, or the two
will fight over the arm.

## 7. Save

`File > Save As`, then put the file in `isaac_sim/scene/` (see its README for Git LFS).
