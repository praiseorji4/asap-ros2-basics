"""
dht11_serial: stream a DHT11 on an Arduino into ROS 2.

Reads `T:<celsius>,H:<percent>` lines from the Arduino's USB serial port and publishes:

    humidity      sensor_msgs/msg/RelativeHumidity   (0.0-1.0, as the message defines it)
    temperature   sensor_msgs/msg/Temperature        (degrees Celsius)

Humidity is published first, then temperature, for every reading.

Parameters: port (/dev/ttyACM0), baud (9600), frame_id (dht11).
Retries every 2 s if the port is missing. Without hardware, use dht11_sim (same topics and types).
"""

from dht11_ros.parsing import parse_line
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from sensor_msgs.msg import RelativeHumidity, Temperature


class Dht11Serial(Node):
    """Bridge between the Arduino's serial text and two ROS topics."""

    def __init__(self) -> None:
        super().__init__('dht11_serial')
        self.port = self.declare_parameter('port', '/dev/ttyACM0').value
        self.baud = self.declare_parameter('baud', 9600).value
        self.frame_id = self.declare_parameter('frame_id', 'dht11').value

        self.temp_pub = self.create_publisher(Temperature, 'temperature', 10)
        self.hum_pub = self.create_publisher(RelativeHumidity, 'humidity', 10)

        self.ser = None
        self.buffer = b''
        self.create_timer(0.05, self.poll)
        self.create_timer(2.0, self.ensure_open)
        self.ensure_open()

    def ensure_open(self) -> None:
        """Open the serial port if it is not open yet."""
        if self.ser is not None:
            return
        try:
            import serial  # imported here so the sim node works without pyserial
        except ImportError:
            self.get_logger().error(
                'pyserial is missing: sudo apt install python3-serial (or use mode:=sim)')
            return
        try:
            self.ser = serial.Serial(self.port, self.baud, timeout=0)
            self.buffer = b''
            self.get_logger().info(f'reading DHT11 from {self.port} at {self.baud} baud')
        except (serial.SerialException, OSError) as err:
            self.get_logger().error(
                f'cannot open {self.port}: {err}. Retrying every 2 s. '
                'No Arduino? run: ros2 launch dht11_ros dht11.launch.py mode:=sim',
                throttle_duration_sec=10.0)

    def poll(self) -> None:
        """Read whatever bytes arrived and publish every complete line."""
        if self.ser is None:
            return
        try:
            self.buffer += self.ser.read(self.ser.in_waiting or 1)
        except OSError as err:  # serial.SerialException is an OSError
            self.get_logger().error(f'lost {self.port}: {err}')
            self.ser.close()
            self.ser = None
            return
        while b'\n' in self.buffer:
            raw, self.buffer = self.buffer.split(b'\n', 1)
            line = raw.decode('ascii', errors='ignore').strip()
            reading = parse_line(line)
            if reading is None:
                if line:
                    self.get_logger().warn(f'skipped line from sensor: {line!r}')
                continue
            self.publish(*reading)

    def publish(self, temperature_c: float, humidity_pct: float) -> None:
        """Publish one reading on both topics with the same timestamp."""
        stamp = self.get_clock().now().to_msg()
        hum = RelativeHumidity()
        hum.header.stamp = stamp
        hum.header.frame_id = self.frame_id
        hum.relative_humidity = humidity_pct / 100.0
        self.hum_pub.publish(hum)

        temp = Temperature()
        temp.header.stamp = stamp
        temp.header.frame_id = self.frame_id
        temp.temperature = temperature_c
        self.temp_pub.publish(temp)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = Dht11Serial()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        if node.ser is not None:
            node.ser.close()
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
