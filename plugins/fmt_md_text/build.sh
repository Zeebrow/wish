#!/bin/bash
bin_output_name=${1:-fmt_md_text}
randomname=$(uuidgen)
container=wish/"$bin_output_name"

d=`pwd`
[ ${d##*/} != "fmt_md_text" ] && echo "must run build from ./plugins/fmt_md_text" && exit 1
printf "building...\n"
docker build --build-arg BIN_OUTPUT_NAME="$bin_output_name" -t "$container" . || exit 1
printf "standup...\n"
docker container create --name "$randomname" "$container" || exit 1
printf "copying binary...\n"
docker container cp "$randomname":/output/fmt_md_text ../../src/scripts/helpers || exit 1
printf "rm...\n"
docker container rm "$randomname" || exit 1
