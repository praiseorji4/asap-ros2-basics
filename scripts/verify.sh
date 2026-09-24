#!/usr/bin/env bash
# verify.sh N - checks step N: starts what it needs, checks the output, stops everything.
#
#   bash ~/asap-kit/scripts/verify.sh 3
#
# Build your workspace first. Every check has a timeout.
# WS=/some/other_ws bash verify.sh 3   checks a different workspace (the default is ~/ros2_ws).

WS="${WS:-$HOME/ros2_ws}"
N="$1"
LOGDIR="$(mktemp -d)"
export PYTHONUNBUFFERED=1
export QT_QPA_PLATFORM="${QT_QPA_PLATFORM:-offscreen}"  # turtlesim without opening a window

[ -z "$ROS_DISTRO" ] && source /opt/ros/jazzy/setup.bash
if [ "$N" != 2 ]; then
  if [ ! -f "$WS/install/setup.bash" ]; then
    echo "FAIL: $WS/install/setup.bash not found - build first: cd $WS && colcon build --symlink-install"
    exit 1
  fi
  source "$WS/install/setup.bash"
fi

FAILS=0
PIDS=()
check() {  # check "what" command...   PASS if the command succeeds
  local what="$1"
  shift
  if "$@" >/dev/null 2>&1; then
    printf 'PASS  %s\n' "$what"
  else
    printf 'FAIL  %s\n' "$what"
    FAILS=$((FAILS + 1))
  fi
}
start() {  # start <logname> command...   run in the background, in its own process group
  local log="$LOGDIR/$1.log"
  shift
  setsid "$@" >"$log" 2>&1 &
  PIDS+=($!)
}
cleanup() {
  for p in "${PIDS[@]}"; do kill -INT -- "-$p" 2>/dev/null; done
  sleep 1
  for p in "${PIDS[@]}"; do kill -KILL -- "-$p" 2>/dev/null; done
}
trap cleanup EXIT
eventually() {  # eventually <seconds> command...   retry until it succeeds or time runs out
  local t="$1"
  shift
  local end=$((SECONDS + t))
  while [ $SECONDS -lt $end ]; do
    "$@" >/dev/null 2>&1 && return 0
    sleep 1
  done
  return 1
}
has_node() { ros2 node list --no-daemon | grep -qx "$1"; }
has_topic() { ros2 topic list -t --no-daemon | grep -qF "$1 [$2]"; }
has_service() { ros2 service list -t --no-daemon | grep -qF "$1 [$2]"; }
log_has() { grep -qE "$2" "$LOGDIR/$1.log"; }
echo_once() { timeout 10 ros2 topic echo --once --no-daemon "$1" "$2"; }
interface_has() { local t="$1"; shift; local out; out="$(ros2 interface show "$t")" || return 1
  for f in "$@"; do grep -qE "^$f( |$)" <<<"$out" || return 1; done; }
call_says() { timeout 10 ros2 service call /validate_reading asap_interfaces/srv/ValidateReading \
  "$1" | grep -q "valid=$2"; }

echo "verify step $N   (ROS_DOMAIN_ID=${ROS_DOMAIN_ID:-0}, workspace $WS)"
echo "---------------------------------------------------------------"
case "$N" in
  1)
    check "counter_pkg has an executable 'counter'" \
      bash -c "ros2 pkg executables counter_pkg | grep -q ' counter$'"
    start counter ros2 run counter_pkg counter
    check "node /counter is running" eventually 10 has_node /counter
    check "it counts (log shows 2 or more)" eventually 5 log_has counter '(count = |published )[2-9]'
    ;;
  2)
    start turtlesim ros2 run turtlesim turtlesim_node
    check "topic   /turtle1/pose" eventually 10 has_topic /turtle1/pose turtlesim/msg/Pose
    check "topic   /turtle1/cmd_vel" has_topic /turtle1/cmd_vel geometry_msgs/msg/Twist
    check "service /spawn" has_service /spawn turtlesim/srv/Spawn
    check "param   background_r" timeout 10 ros2 param get --no-daemon /turtlesim background_r
    check "action  /turtle1/rotate_absolute" \
      bash -c "ros2 node info --no-daemon /turtlesim | grep -q '/turtle1/rotate_absolute:'"
    ;;
  3)
    check "counter_pkg has 'count_listener' (setup.py entry point)" \
      bash -c "ros2 pkg executables counter_pkg | grep -q ' count_listener$'"
    start counter ros2 run counter_pkg counter
    start listener ros2 run counter_pkg count_listener
    check "topic /count is std_msgs/msg/Int32" eventually 10 has_topic /count std_msgs/msg/Int32
    check "a message arrives on /count" echo_once /count std_msgs/msg/Int32
    check "count_listener hears it" eventually 5 log_has listener 'heard [0-9]+'
    ;;
  4)
    check "asap_interfaces/msg/Count has count, source, stamp" \
      interface_has asap_interfaces/msg/Count 'int64 count' 'string source' \
      'builtin_interfaces/Time stamp'
    start counter ros2 run counter_pkg counter
    start listener ros2 run counter_pkg count_listener
    check "topic /count is asap_interfaces/msg/Count" \
      eventually 10 has_topic /count asap_interfaces/msg/Count
    check "a Count arrives with source: counter" \
      bash -c "timeout 10 ros2 topic echo --once --no-daemon /count asap_interfaces/msg/Count | grep -q 'source: counter'"
    check "count_listener hears who counted" eventually 5 log_has listener 'heard [0-9]+ from counter'
    ;;
  5)
    check "package dht11_ros is built" ros2 pkg prefix dht11_ros
    start dht11 ros2 launch dht11_ros dht11.launch.py
    check "topic /temperature is sensor_msgs/msg/Temperature" \
      eventually 10 has_topic /temperature sensor_msgs/msg/Temperature
    check "topic /humidity is sensor_msgs/msg/RelativeHumidity" \
      has_topic /humidity sensor_msgs/msg/RelativeHumidity
    check "a temperature arrives" echo_once /temperature sensor_msgs/msg/Temperature
    ;;
  6)
    check "asap_interfaces/srv/ValidateReading is built" \
      interface_has asap_interfaces/srv/ValidateReading 'float64 temperature' 'bool valid' \
      'string reason'
    check "asap_interfaces/msg/EnvReading has the reading and the verdict" \
      interface_has asap_interfaces/msg/EnvReading 'float64 temperature' 'float64 humidity' \
      'bool valid' 'string reason'
    check "env_monitor has validator_server and env_validator" bash -c \
      "ros2 pkg executables env_monitor | grep -q validator_server && ros2 pkg executables env_monitor | grep -q env_validator"
    start dht11 ros2 launch dht11_ros dht11.launch.py glitch_rate:=0.0
    start server ros2 run env_monitor validator_server
    check "service /validate_reading is up" \
      eventually 10 has_service /validate_reading asap_interfaces/srv/ValidateReading
    check "25 C is valid (max_temp 35)" call_says "{temperature: 25.0}" True
    check "40 C is not valid" call_says "{temperature: 40.0}" False
    start validator ros2 run env_monitor env_validator
    check "readings arrive on /env/validated with valid: true" \
      bash -c "timeout 15 ros2 topic echo --no-daemon /env/validated asap_interfaces/msg/EnvReading | grep -m1 -q 'valid: true'"
    check "heat the robot: ros2 param set /dht11_sim target_temperature 45.0" \
      timeout 10 ros2 param set --no-daemon /dht11_sim target_temperature 45.0
    check "too-hot readings are published too, with valid: false" \
      bash -c "timeout 40 ros2 topic echo --no-daemon /env/validated asap_interfaces/msg/EnvReading | grep -m1 -q 'valid: false'"
    check "env_validator logs the reason" eventually 5 log_has validator 'above max_temp'
    ;;
  *)
    echo "usage: bash $0 N    (N = 1..6)"
    exit 1
    ;;
esac

echo "---------------------------------------------------------------"
if [ "$FAILS" -eq 0 ]; then
  echo "STEP $N OK"
  exit 0
fi
echo "STEP $N: $FAILS check(s) failed. Logs of what ran: $LOGDIR"
exit 1
