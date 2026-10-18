#!/usr/bin/env bash
# Exercise-07: stop and remove the Jenkins container
set -uo pipefail
docker stop jenkins && docker rm jenkins
