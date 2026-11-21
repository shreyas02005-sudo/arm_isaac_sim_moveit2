# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.1.0] - 2026-11-21

### Added
- Python trajectory bridge (`bridge/isaac_trajectory_bridge.py`) connecting MoveIt `FollowJointTrajectory` actions to Isaac Sim, with a settle wait and gripper finger mirroring.
- Launch file for MoveIt, RViz and the bridge (`bridge/isaac_arm.launch.xml`).
- `sequence_demo` C++ program: home, pose_2, gripper_closed, pose_1, gripper_open.
- ROS 2 packages for the 6-DOF arm and gripper, plus an overlay of the files changed for Windows and Isaac Sim.
- Isaac Sim scene (`isaac_sim/scene/my_robot_1`) and Script Editor snippets.
- Documentation: setup, Isaac scene, architecture, troubleshooting.
- GitHub Actions CI (lint and ROS 2 Jazzy build) and Dependabot for workflow updates.
