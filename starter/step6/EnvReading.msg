# EnvReading.msg - one sensor reading plus the validator's verdict on it.
# Copy to: ~/ros2_ws/src/asap_interfaces/msg/EnvReading.msg
builtin_interfaces/Time stamp   # when the sensor took it
float64 temperature             # degrees Celsius
float64 humidity                # percent, 0-100
# TODO(6.1b): add the verdict fields:  valid (bool), reason (string)
