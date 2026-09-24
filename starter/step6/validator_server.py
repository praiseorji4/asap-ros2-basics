"""
Step 6 - validator_server: says whether a robot temperature reading is within the safe limit.

Copy to:  ~/ros2_ws/src/env_monitor/env_monitor/validator_server.py
Run:      ros2 run env_monitor validator_server
Check:    ros2 service call /validate_reading asap_interfaces/srv/ValidateReading \
              "{temperature: 40.0}"          -> valid=False, with a reason
"""

import math

from asap_interfaces.srv import ValidateReading
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node


class ValidatorServer(Node):
    """Answers one question: is this temperature safe for the robot."""

    def __init__(self):
        super().__init__('validator_server')
        self.declare_parameter('max_temp', 35.0)

        # TODO(6.2): service type ValidateReading, name 'validate_reading', callback self.on_validate.
        #            API:  self.service = self.create_service(<type>, '<name>', <callback>)
        self.get_logger().info('ready: /validate_reading')

    def on_validate(self, request, response):
        t = request.temperature
        max_temp = self.get_parameter('max_temp').value

        # TODO(6.3): set response.valid and response.reason:
        #   t is NaN (math.isnan(t))  -> False, 'no reading (the sensor did not answer)'
        #   t > max_temp              -> False, f'temperature {t:.1f} C is above max_temp {max_temp:.1f} C'
        #   otherwise                 -> True, ''
        response.valid = True
        response.reason = 'not checked yet: TODO(6.3)'
        _ = (math, t, max_temp)  # remove this line when you use them
        return response


def main(args=None):
    rclpy.init(args=args)
    node = ValidatorServer()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
