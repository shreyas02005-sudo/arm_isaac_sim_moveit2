# Overlay files

These files are new or changed compared with the original arm packages. Copy them over the matching package
inside your pixi workspace (`WS\src\<package>\...`) after copying the packages in.

| File | Change |
|---|---|
| `my_robot_description/urdf/my_robot.ros2_control.xacro` | Hardware plugin switched from `mock_components/GenericSystem` to `topic_based_ros2_control/TopicBasedSystem` with the Isaac joint topics (not loaded by the bridge launch, kept for reference) |
| `my_robot_moveit_config/config/moveit_controllers.yaml` | Added `trajectory_execution` timing keys |
| `my_robot_commander_cpp/CMakeLists.txt` | Builds `test_moveit` and `sequence_demo` only; drops `commander` and its `example_interfaces` dependency |
| `my_robot_commander_cpp/package.xml` | Removes the `example_interfaces` dependency |
| `my_robot_commander_cpp/src/sequence_demo.cpp` | New: home, pose_2, gripper close, pose_1, gripper open |

`my_robot_commander_cpp/src/test_moveit.cpp` and `commander_template.cpp` are unchanged and come from your original package.
