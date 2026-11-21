@echo off
rem Stops the MoveIt/bridge stack WITHOUT touching Isaac Sim (which also runs on python).
taskkill /f /im move_group.exe 2>nul
taskkill /f /im rviz2.exe 2>nul
taskkill /f /im robot_state_publisher.exe 2>nul
taskkill /f /im ros2_control_node.exe 2>nul
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*isaac_trajectory_bridge*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"
echo Arm stack stopped.
