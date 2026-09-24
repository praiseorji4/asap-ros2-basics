"""
Step 4 - counter: publishes asap_interfaces/msg/Count on /count.

Copy to:  ~/ros2_ws/src/counter_pkg/counter_pkg/counter.py
Needs:    asap_interfaces built (TODO 4.1-4.3); <depend>asap_interfaces</depend> (TODO 4.6)
Run:      ros2 run counter_pkg counter
Check:    ros2 topic echo /count     (count, source, stamp)
"""

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Int32

# TODO(4.4a): import Count:  from asap_interfaces.msg import Count


class Counter(Node):
    """A node that counts and says who counted and when."""

    def __init__(self):
        super().__init__('counter')
        self.count = 0
        # TODO(4.4b): publish Count instead of Int32 (same topic).
        self.publisher = self.create_publisher(Int32, 'count', 10)
        self.timer = self.create_timer(1.0, self.on_timer)

    def on_timer(self):
        self.count += 1
        # TODO(4.4c): build a Count and fill all three fields:
        #             msg = Count()
        #             msg.count = self.count
        #             msg.source = self.get_name()
        #             msg.stamp = self.get_clock().now().to_msg()
        msg = Int32()
        msg.data = self.count
        self.publisher.publish(msg)
        self.get_logger().info(f'published {self.count}')


def main(args=None):
    rclpy.init(args=args)
    node = Counter()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
