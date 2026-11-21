#include <rclcpp/rclcpp.hpp>
#include <moveit/move_group_interface/move_group_interface.hpp>
#include <chrono>
#include <string>
#include <thread>

using MGI = moveit::planning_interface::MoveGroupInterface;

static bool go(MGI &group, const std::string &name, const rclcpp::Logger &log)
{
    group.setStartStateToCurrentState();
    group.setNamedTarget(name);

    MGI::Plan plan;
    if (!(group.plan(plan) == moveit::core::MoveItErrorCode::SUCCESS)) {
        RCLCPP_ERROR(log, "Planning to '%s' failed", name.c_str());
        return false;
    }
    if (!(group.execute(plan) == moveit::core::MoveItErrorCode::SUCCESS)) {
        RCLCPP_ERROR(log, "Execution to '%s' failed", name.c_str());
        return false;
    }
    RCLCPP_INFO(log, "Reached '%s'", name.c_str());
    std::this_thread::sleep_for(std::chrono::milliseconds(500));
    return true;
}

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);

    auto node = std::make_shared<rclcpp::Node>("sequence_demo");
    rclcpp::executors::SingleThreadedExecutor executor;
    executor.add_node(node);
    auto spinner = std::thread([&executor]() { executor.spin(); });

    MGI arm(node, "arm");
    arm.setMaxVelocityScalingFactor(0.3);
    arm.setMaxAccelerationScalingFactor(0.3);

    MGI gripper(node, "gripper");

    auto log = node->get_logger();
    bool ok = go(arm, "home", log)
           && go(arm, "pose_2", log)
           && go(gripper, "gripper_closed", log)
           && go(arm, "pose_1", log)
           && go(gripper, "gripper_open", log);

    RCLCPP_INFO(log, ok ? "Sequence finished" : "Sequence stopped early");

    rclcpp::shutdown();
    spinner.join();
    return ok ? 0 : 1;
}
