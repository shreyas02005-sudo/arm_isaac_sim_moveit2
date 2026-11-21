cmake_minimum_required(VERSION 3.8)
project(my_robot_commander_cpp)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(moveit_ros_planning_interface REQUIRED)

add_executable(test_moveit src/test_moveit.cpp)
ament_target_dependencies(test_moveit rclcpp moveit_ros_planning_interface)

add_executable(sequence_demo src/sequence_demo.cpp)
ament_target_dependencies(sequence_demo rclcpp moveit_ros_planning_interface)

install(TARGETS test_moveit sequence_demo DESTINATION lib/${PROJECT_NAME}/)

ament_package()
