# Isaac Sim scene

The scene is `my_robot_1/my_robot.usda`. Open it in Isaac Sim 6.0.1 with File > Open. It references the files in
`my_robot_1/payloads/` by relative path, so keep the folder together.

It contains the imported arm at `/my_robot` (articulation root `/my_robot/Geometry`) and the Action Graph that
exchanges joint commands and states with ROS (see `docs/ISAAC_SCENE.md`).

The files are plain-text USD, so they are stored in git normally. Only binary `.usd` and `.usdc` files use Git LFS.

This scene is a copy of the one used in the tested run. Its internal references were checked to resolve, but it
was not re-run from this repository.
