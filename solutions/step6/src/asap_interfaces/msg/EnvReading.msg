# EnvReading.msg - one sensor reading plus the validator's verdict on it.
builtin_interfaces/Time stamp   # when the sensor took it
float64 temperature             # degrees Celsius
float64 humidity                # percent, 0-100
bool valid                      # false: the robot is too hot, or the reading failed
string reason                   # empty when valid, otherwise why not
