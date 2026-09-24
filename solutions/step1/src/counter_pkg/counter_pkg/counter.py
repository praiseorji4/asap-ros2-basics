"""
Step 1 - counter: counts up once a second and logs the number.

Run it:     ros2 run counter_pkg counter
Check it:   ros2 node list        (shows /counter)
            rqt_graph
"""

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node


class Counter(Node):
    """A node that counts."""

    def __init__(self):
        super().__init__('counter')
        self.count = 0
        # on_timer runs every 1.0 s; rclpy.spin is the loop.
        self.timer = self.create_timer(1.0, self.on_timer)

    def on_timer(self):
        self.count += 1
        self.get_logger().info(f'count = {self.count}')


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
