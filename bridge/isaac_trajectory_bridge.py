"""Isaac Sim trajectory bridge for MoveIt 2.

Stands in for ros2_control_node (which crashes on Windows in pal_statistics.dll).

  * Serves  /arm_controller/follow_joint_trajectory
            /gripper_controller/follow_joint_trajectory
    (the action names configured in moveit_controllers.yaml).
  * Turns each trajectory into timed JointState messages on /isaac_joint_commands.
  * Waits until Isaac's joints settle at the final point before reporting success,
    so MoveIt's next start-state check passes.
  * Mirrors the left gripper finger onto the right finger (URDF mimic, multiplier -1),
    because Isaac's URDF importer does not carry the mimic joint over.
  * Republishes /isaac_joint_states as /joint_states, limited to the 7 controlled
    joints (the right finger is derived by robot_state_publisher from the mimic).
"""
import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from sensor_msgs.msg import JointState
from control_msgs.action import FollowJointTrajectory

CONTROLLED = ["joint1", "joint2", "joint3", "joint4", "joint5", "joint6",
              "gripper_left_finger_joint"]
SETTLE_TOL = 0.005
SETTLE_TIMEOUT = 4.0


class Bridge(Node):
    def __init__(self):
        super().__init__("isaac_trajectory_bridge")
        self.cbg = ReentrantCallbackGroup()
        self.latest = {}
        self.cmd_pub = self.create_publisher(JointState, "/isaac_joint_commands", 10)
        self.state_pub = self.create_publisher(JointState, "/joint_states", 10)
        self.create_subscription(JointState, "/isaac_joint_states", self.on_state, 10,
                                 callback_group=self.cbg)
        self.servers = []
        for ctrl in ("arm_controller", "gripper_controller"):
            self.servers.append(ActionServer(
                self, FollowJointTrajectory, ctrl + "/follow_joint_trajectory",
                execute_callback=self.execute,
                goal_callback=lambda g: GoalResponse.ACCEPT,
                cancel_callback=lambda c: CancelResponse.ACCEPT,
                callback_group=self.cbg))
        self.get_logger().info("Isaac trajectory bridge ready")

    def on_state(self, msg):
        self.latest = dict(zip(msg.name, msg.position))
        out = JointState()
        out.header.stamp = self.get_clock().now().to_msg()
        for n, p in zip(msg.name, msg.position):
            if n in CONTROLLED:
                out.name.append(n)
                out.position.append(p)
        self.state_pub.publish(out)

    def send(self, names, positions):
        names = list(names)
        positions = [float(x) for x in positions]
        if "gripper_left_finger_joint" in names:
            i = names.index("gripper_left_finger_joint")
            names.append("gripper_right_finger_joint")
            positions.append(-positions[i])
        m = JointState()
        m.name = names
        m.position = positions
        self.cmd_pub.publish(m)

    def execute(self, goal_handle):
        traj = goal_handle.request.trajectory
        names = list(traj.joint_names)
        pts = traj.points
        result = FollowJointTrajectory.Result()
        if not pts:
            goal_handle.succeed()
            return result

        def t(p):
            return p.time_from_start.sec + p.time_from_start.nanosec * 1e-9

        total = t(pts[-1])
        start = time.time()
        i = 0
        while True:
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                return result
            now = time.time() - start
            while i < len(pts) - 1 and now >= t(pts[i + 1]):
                i += 1
            if i >= len(pts) - 1:
                pos = list(pts[-1].positions)
            else:
                t0, t1 = t(pts[i]), t(pts[i + 1])
                a = 0.0 if t1 <= t0 else min(max((now - t0) / (t1 - t0), 0.0), 1.0)
                pos = [x0 + a * (x1 - x0)
                       for x0, x1 in zip(pts[i].positions, pts[i + 1].positions)]
            self.send(names, pos)
            if now >= total:
                break
            time.sleep(0.02)

        final = dict(zip(names, pts[-1].positions))
        deadline = time.time() + SETTLE_TIMEOUT
        settled = False
        while time.time() < deadline:
            self.send(names, pts[-1].positions)
            errs = [abs(self.latest[n] - final[n]) for n in names if n in self.latest]
            if errs and max(errs) < SETTLE_TOL:
                settled = True
                break
            time.sleep(0.02)
        if not settled:
            self.get_logger().warn("Arm did not settle within %.1f s" % SETTLE_TIMEOUT)

        goal_handle.succeed()
        result.error_code = FollowJointTrajectory.Result.SUCCESSFUL
        return result


def main():
    rclpy.init()
    node = Bridge()
    ex = MultiThreadedExecutor()
    ex.add_node(node)
    ex.spin()


main()
