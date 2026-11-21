# Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `could not find pixi.toml` | Wrong folder | `cd /d WS` first |
| `VisualStudioVersion is not set` | Compiler environment not loaded | Run `vcvars64.bat` in the same window |
| `Unknown / unsupported VS version '18.0'` | colcon does not know VS 2026 | Add `-G Ninja` |
| `python_d.exe doesn't exist`, `Could NOT find PythonExtra` | Ninja assumed a Debug build | Add `-DCMAKE_BUILD_TYPE=Release` |
| `my_robot_commander_cpp` fails on `example_interfaces` | Package not in the pixi environment | Build only `test_moveit`/`sequence_demo` (the overlay CMakeLists does) |
| `ros2_control_node` exit code `3221225477` | Crash in `pal_statistics.dll` | Use the bridge launch (`isaac_arm.launch.xml`) |
| `malformed launch argument 'my_robot.launch.xml'` | `ros2 launch <pkg> <file>` form | Launch by full path |
| `Could not find parameter robot_description` (commander) | MoveIt launch or Zenoh not running | Start Zenoh, Isaac (Play), then the launch; check `ros2 node list` |
| `Invalid Trajectory: start point deviates ... joint 'joint4'` | Arm not settled when the next move started | Use the bridge with the settle wait; start tolerance 0.03 |
| `Controller is taking too long to execute trajectory` / `TIMED_OUT` | Simulated arm lags the plan | `allowed_execution_duration_scaling` / `allowed_goal_duration_margin` in `moveit_controllers.yaml` |
| YAML `ParserError ... expected <block end>` after editing `moveit_controllers.yaml` | Stray space before `trajectory_execution:` | Keys must start in column 1 |
| `Pattern '/my_robot' did not match any articulations` | Wrong target prim | Use `/my_robot/Geometry` |
| Gain Tuner shows 2 joints, Velocity mode | It cannot select the articulation root | Use `configure_drives.py` |
| Arm sags or shakes | Drive gains | Raise stiffness (sag) or damping (shake) |
| Right finger does not follow the left | Isaac ignores URDF mimic | Bridge mirrors it; also run `configure_drives.py` so both fingers have drives |
| New launch misbehaves after closing the old window | Orphaned `move_group`/`rviz2`/bridge processes | Run `scripts\stop_arm.bat`; Ctrl+C once and wait next time |
| `Cannot create a symlink to latest log directory (WinError 1314)` | Windows privilege | Harmless; optional Developer Mode |
| RViz: `No active joints or end effectors found for group 'arm'` | RViz not given kinematics params | Harmless; marker dragging unavailable |
| `/clock` visible in WSL never appears (Isaac on Windows, ROS in WSL2) | Windows-to-WSL DDS discovery | Not supported here; use the pixi/Zenoh setup |
