# ROS 2 packages

The five packages of the arm. The files listed in [`../../overlay/README.md`](../../overlay/README.md) are already applied here.

| Package | Purpose |
|---|---|
| `my_robot_description` | URDF/xacro for the arm and parallel gripper |
| `my_robot_moveit_config` | MoveIt 2 configuration (SRDF, kinematics, controllers) |
| `my_robot_bringup` | Launch file, RViz configuration |
| `my_robot_interfaces` | `PoseCommand` message |
| `my_robot_commander_cpp` | C++ programs; `test_moveit` and `sequence_demo` are built on Windows |

Build instructions: [`../../docs/SETUP_WINDOWS.md`](../../docs/SETUP_WINDOWS.md).