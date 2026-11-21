# Architecture and design decisions

## Data flow

1. `move_group` plans in joint space (OMPL by default) for the groups `arm` and `gripper`.
2. Execution goes through MoveIt's simple controller manager to two `FollowJointTrajectory` action servers
   named `arm_controller/follow_joint_trajectory` and `gripper_controller/follow_joint_trajectory`.
3. `bridge/isaac_trajectory_bridge.py` serves both actions. For each goal it interpolates the trajectory
   linearly in wall-clock time at about 50 Hz and publishes `sensor_msgs/JointState` on `/isaac_joint_commands`.
4. In Isaac Sim, an Action Graph subscribes to `/isaac_joint_commands` and feeds an Articulation Controller
   (position commands) targeting `/my_robot/Geometry`. A second node publishes `/isaac_joint_states`.
5. The bridge republishes `/isaac_joint_states` as `/joint_states` for the 7 controlled joints. `robot_state_publisher`
   computes the right finger from the URDF mimic joint.

## Bridge behaviour worth knowing

- **Settle wait.** After the last trajectory point is sent, the bridge keeps sending it until every joint is within
  0.005 rad (timeout 4 s) before reporting success. Without this, MoveIt's next move was rejected with
  `Invalid Trajectory: start point deviates from current robot state more than 0.01 at joint 'joint4'`.
- **Gripper mirroring.** When `gripper_left_finger_joint` is commanded, the bridge also sends
  `gripper_right_finger_joint` = minus the same value (the URDF mimic multiplier is -1).
- **Timing limits.** `overlay/.../moveit_controllers.yaml` adds `allowed_execution_duration_scaling: 2.0`,
  `allowed_goal_duration_margin: 5.0` and `allowed_start_tolerance: 0.03`, because the simulated arm lags the plan
  and the default limits caused `TIMED_OUT` aborts.

## Why not ros2_control_node?

`ros2_control_node` was launched with both `mock_components/GenericSystem` and
`topic_based_ros2_control/TopicBasedSystem`, under both Zenoh and Fast DDS. Every time it died with exit code
`3221225477` (0xC0000005) immediately after "Subscribing to '/robot_description' topic". Windows' Application Error
log named the faulting module as `pal_statistics.dll` in the pixi environment. Because the crash is in a bundled
Windows package, the bridge replaces the controller manager instead.

## Why Zenoh and pixi?

NVIDIA's `IsaacSim-ros_workspaces` ships a pixi workspace (`jazzy_ws`) in which Isaac Sim, ROS 2 Jazzy and
`rmw_zenoh_cpp` are installed together and talk over a Zenoh router. This is the only Isaac-to-ROS connection that
worked here. Earlier attempts to connect a standalone Isaac Sim on Windows to ROS in WSL2 over Fast DDS (mirrored
networking, discovery server, loopback-only profiles) never produced a working link, and the WSL distro
hung repeatedly while Isaac was running.

## Joints and frames

| Joint | Type | Controller |
|---|---|---|
| joint1 - joint5 | revolute | `arm_controller` |
| joint6 | continuous | `arm_controller` |
| gripper_left_finger_joint | prismatic, 0 to 0.06 m | `gripper_controller` |
| gripper_right_finger_joint | prismatic, mimic of left with multiplier -1 | none (derived) |

Planning groups: `arm` (joint1-joint6 plus the fixed `hand_tool_joint` and virtual joint) and `gripper`.
The arm is built from box and cylinder primitives, so there are no mesh files.
