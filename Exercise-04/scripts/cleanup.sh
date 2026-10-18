#!/usr/bin/env bash
# Exercise-04 Task 6: stop/remove containers and the network
set -uo pipefail
docker stop mysql redis flask && docker rm mysql redis flask
docker network rm my-bridge-net
