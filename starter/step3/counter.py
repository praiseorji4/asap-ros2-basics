"""
Step 3 - counter: counts up once a second and publishes the number on /count.

Copy to:  ~/ros2_ws/src/counter_pkg/counter_pkg/counter.py
Run:      ros2 run counter_pkg counter
Check:    ros2 topic echo /count
          ros2 topic hz /count
"""

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

# TODO(3.1): import the message type:  from std_msgs.msg import Int32


class Counter(Node):
    """A node that counts and publishes the count."""

    def __init__(self):
        super().__init__('counter')
        self.count = 0
        # TODO(3.2): publisher: type Int32, topic 'count', queue depth 10.
        #            API:  self.publisher = self.create_publisher(<type>, '<topic>', 10)
        self.timer = self.create_timer(1.0, self.on_timer)

    def on_timer(self):
        self.count += 1
        self.get_logger().info(f'count = {self.count}')
        # TODO(3.3): build and publish the message.
        #            msg = Int32()
        #            msg.data = self.count
        #            self.publisher.publish(msg)


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
