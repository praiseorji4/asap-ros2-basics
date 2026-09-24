"""
Step 1 - counter: counts up once a second and logs the number.

Copy to:  ~/ros2_ws/src/counter_pkg/counter_pkg/counter.py
Run:      ros2 run counter_pkg counter
Check:    ros2 node list     (/counter)
"""

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node


class Counter(Node):
    """A node that counts."""

    def __init__(self):
        # TODO(1.1): name the node 'counter'.
        super().__init__('change_me')
        self.count = 0

        # TODO(1.2): call self.on_timer every 1.0 s.
        #            API:  self.timer = self.create_timer(<seconds>, <callback>)

    def on_timer(self):
        # TODO(1.3): add 1 to self.count and log it.
        #            API:  self.get_logger().info(f'count = {self.count}')
        pass


def main(args=None):
    rclpy.init(args=args)
    node = Counter()
    try:
        # TODO(1.4): spin the node so its timer fires.
        #            API:  rclpy.spin(node)
        pass
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
