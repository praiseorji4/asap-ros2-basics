#!/usr/bin/env bash
# catchup.sh N - puts the finished step N into your workspace and builds it.
#
#   bash ~/asap-kit/scripts/catchup.sh 3
#
# The current ~/ros2_ws/src is moved to ~/ros2_ws_backups/src_<time> first.
#
# WS=/some/other_ws bash catchup.sh 3   uses a different workspace (the default is ~/ros2_ws).

set -e
KIT="$(cd "$(dirname "$0")/.." && pwd)"
WS="${WS:-$HOME/ros2_ws}"
N="$1"

case "$N" in
  1 | 2) SOL=step1; VENDOR=no ;;
  3) SOL=step3; VENDOR=no ;;
  4) SOL=step4; VENDOR=no ;;
  5) SOL=step4; VENDOR=yes ;;
  6) SOL=step6; VENDOR=yes ;;
  *) echo "usage: bash $0 N    (N = 1..6, the step you want finished)" >&2; exit 1 ;;
esac

if [ -z "$ROS_DISTRO" ]; then
  source /opt/ros/jazzy/setup.bash
fi

mkdir -p "$WS/src"
if [ -n "$(ls -A "$WS/src")" ]; then
  # Outside the workspace: colcon searches every folder under it and would find duplicates.
  BACKUP="${WS}_backups/src_$(date +%Y%m%d_%H%M%S)"
  mkdir -p "$(dirname "$BACKUP")"
  mv "$WS/src" "$BACKUP"
  echo "your old src/ is saved in: $BACKUP"
  mkdir -p "$WS/src"
fi

cp -r "$KIT/solutions/$SOL/src/." "$WS/src/"
[ "$VENDOR" = yes ] && cp -r "$KIT/vendor/dht11_ros" "$WS/src/"
echo "copied step $N into $WS/src: $(ls "$WS/src" | tr '\n' ' ')"

# Old build products can point at files that no longer exist, so build from clean.
cd "$WS"
rm -rf build install log
colcon build --symlink-install

echo
echo "Done. In EVERY open terminal, run:"
echo "    source $WS/install/setup.bash"
