"""
Step 4 - counter: counts up once a second and publishes our own Count message on /count.

Run it:     ros2 run counter_pkg counter
Check it:   ros2 topic echo /count           (count, source and stamp)
            ros2 interface show asap_interfaces/msg/Count
"""

from asap_interfaces.msg import Count
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node


class Counter(Node):
    """A node that counts and says who counted and when."""

    def __init__(self):
        super().__init__('counter')
        self.count = 0
        self.publisher = self.create_publisher(Count, 'count', 10)
        self.timer = self.create_timer(1.0, self.on_timer)

    def on_timer(self):
        self.count += 1
        msg = Count()
        msg.count = self.count
        msg.source = self.get_name()
        msg.stamp = self.get_clock().now().to_msg()
        self.publisher.publish(msg)
        self.get_logger().info(f'published {msg.count}')


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
