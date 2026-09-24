#!/usr/bin/env bash
# check_env.sh - laptop check. Prints PASS/FAIL, exits non-zero on failure.
#
#   bash ~/asap-kit/scripts/check_env.sh
#
# Checks the OS, ROS, tools, the kit location and the group's domain.

FAILS=0
row() {  # row PASS|FAIL|WARN "what" "detail"
  printf '%-5s | %-34s | %s\n' "$1" "$2" "$3"
  [ "$1" = "FAIL" ] && FAILS=$((FAILS + 1))
}
ok_if() {  # ok_if "what" "fix" command...
  local what="$1" fix="$2"
  shift 2
  if "$@" >/dev/null 2>&1; then row PASS "$what" ""; else row FAIL "$what" "$fix"; fi
}

printf '%-5s | %-34s | %s\n' RESULT CHECK DETAIL
printf -- '------+------------------------------------+------------------------------\n'

. /etc/os-release 2>/dev/null
if [ "$VERSION_ID" = "24.04" ]; then
  row PASS "Ubuntu 24.04" "$PRETTY_NAME"
else
  row FAIL "Ubuntu 24.04" "found ${PRETTY_NAME:-unknown}"
fi

if [ "$ROS_DISTRO" = "jazzy" ]; then
  row PASS "ROS 2 Jazzy sourced" ""
else
  row FAIL "ROS 2 Jazzy sourced" "run: source /opt/ros/jazzy/setup.bash"
fi

ok_if "colcon installed" "sudo apt install python3-colcon-common-extensions" command -v colcon
ok_if "git installed" "sudo apt install git" command -v git
ok_if "turtlesim installed" "sudo apt install ros-jazzy-turtlesim" dpkg -s ros-jazzy-turtlesim
ok_if "rqt_graph installed" "sudo apt install ros-jazzy-rqt-graph" dpkg -s ros-jazzy-rqt-graph
ok_if "kit at ~/asap-kit" "copy the kit folder to ~/asap-kit (see SETUP.md)" \
  test -f "$HOME/asap-kit/scripts/catchup.sh"

if [ -n "$ROS_DOMAIN_ID" ] && [ "$ROS_DOMAIN_ID" -ge 11 ] 2>/dev/null && [ "$ROS_DOMAIN_ID" -le 19 ] 2>/dev/null; then
  row PASS "ROS_DOMAIN_ID for your group" "$ROS_DOMAIN_ID = group $((ROS_DOMAIN_ID - 10))"
else
  row FAIL "ROS_DOMAIN_ID for your group" "got '${ROS_DOMAIN_ID}': source ~/asap-kit/scripts/group_env.sh N"
fi

# Only the instructor's laptop talks to the Arduino; students use the simulator.
if python3 -c 'import serial' 2>/dev/null; then
  row PASS "pyserial (instructor only)" ""
else
  row WARN "pyserial (instructor only)" "not needed for students; instructor: sudo apt install python3-serial"
fi

# Any other sourced workspace can shadow packages.
stale=""
IFS=':' read -ra prefixes <<<"${AMENT_PREFIX_PATH}"
for p in "${prefixes[@]}"; do
  case "$p" in
    /opt/ros/jazzy | "" | "$HOME/ros2_ws/install/"* | "$HOME/demo_ws/install/"*) ;;
    *) stale="$stale $p" ;;
  esac
done
if [ -z "$stale" ]; then
  row PASS "no other workspace sourced" ""
else
  row FAIL "no other workspace sourced" "found:$stale (open a new terminal; check ~/.bashrc)"
fi

echo
if [ "$FAILS" -eq 0 ]; then
  echo "ALL GREEN: this laptop is ready."
  exit 0
fi
echo "$FAILS check(s) failed. Fix the DETAIL column, open a new terminal, and run this again."
exit 1
