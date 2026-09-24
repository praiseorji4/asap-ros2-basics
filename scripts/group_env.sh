#!/usr/bin/env bash
# group_env.sh N - export ROS_DOMAIN_ID for group N (groups 1-9 use domains 11-19).
#
# Use `source`, so the export lands in your shell:
#   source ~/asap-kit/scripts/group_env.sh 3
#   source ~/asap-kit/scripts/group_env.sh 3 --persist     # also append to ~/.bashrc

_group_env_main() {
  local n="$1" persist="$2"
  if ! [[ "$n" =~ ^[1-9]$ ]]; then
    echo "usage: source ~/asap-kit/scripts/group_env.sh N [--persist]   (N = 1..9)" >&2
    return 1
  fi
  export ROS_DOMAIN_ID=$((10 + n))
  export ROS_GROUP="group_$n"
  export RMW_IMPLEMENTATION="${RMW_IMPLEMENTATION:-rmw_fastrtps_cpp}"
  echo "group $n -> ROS_DOMAIN_ID=$ROS_DOMAIN_ID  ROS_GROUP=$ROS_GROUP  RMW_IMPLEMENTATION=$RMW_IMPLEMENTATION"
  if [ "$persist" = "--persist" ]; then
    {
      echo "# added by asap group_env.sh"
      echo "export ROS_DOMAIN_ID=$ROS_DOMAIN_ID"
      echo "export ROS_GROUP=$ROS_GROUP"
      echo "export RMW_IMPLEMENTATION=$RMW_IMPLEMENTATION"
    } >>"$HOME/.bashrc"
    echo "appended to ~/.bashrc"
  fi
}
_group_env_main "$@"
_rc=$?
unset -f _group_env_main
return $_rc 2>/dev/null || exit $_rc
