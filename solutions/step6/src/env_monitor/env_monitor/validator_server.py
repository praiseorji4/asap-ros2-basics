"""
Step 6 - validator_server: says whether a robot temperature reading is within the safe limit.

Service:    /validate_reading   (asap_interfaces/srv/ValidateReading)
Parameter:  max_temp (deg C, default 35.0) - above this the robot is too hot.

Run it:     ros2 run env_monitor validator_server
Check it:   ros2 service call /validate_reading asap_interfaces/srv/ValidateReading \
                "{temperature: 40.0}"
            ros2 param set /validator_server max_temp 30.0
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
        self.service = self.create_service(ValidateReading, 'validate_reading', self.on_validate)
        self.get_logger().info('ready: /validate_reading')

    def on_validate(self, request, response):
        t = request.temperature
        # Read the limit on every call, so `ros2 param set` takes effect immediately.
        max_temp = self.get_parameter('max_temp').value

        if math.isnan(t):
            response.valid = False
            response.reason = 'no reading (the sensor did not answer)'
        elif t > max_temp:
            response.valid = False
            response.reason = f'temperature {t:.1f} C is above max_temp {max_temp:.1f} C'
        else:
            response.valid = True
            response.reason = ''
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
