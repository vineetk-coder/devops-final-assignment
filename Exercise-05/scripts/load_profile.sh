#!/usr/bin/env bash
# Exercise-05 Task 3: install + load the AppArmor profile, then run the container with it.
# Linux host with AppArmor only (Ubuntu/Debian or WSL2 Ubuntu with AppArmor enabled).
# Run from the Exercise-05 folder:  bash scripts/load_profile.sh
set -euo pipefail

sudo apt-get update
sudo apt-get install -y apparmor-utils

# Copy the profile from this repo (relative path) into the system location
sudo cp apparmor/my-apparmor-profile /etc/apparmor.d/my-apparmor-profile
sudo apparmor_parser -r /etc/apparmor.d/my-apparmor-profile

# Confirm it is loaded
sudo aa-status | grep my-apparmor-profile

docker build -t flask-apparmor .
echo "Starting container with the profile (Ctrl+C to stop)..."
docker run --rm --security-opt="apparmor=my-apparmor-profile" -p 5000:5000 flask-apparmor
