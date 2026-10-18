"""Exercise-05 Task 4: use the Docker SDK for Python to apply the AppArmor profile.

Run from the Exercise-05 folder:  python apply_apparmor.py
Requires: pip install docker, Docker running, profile loaded (scripts/load_profile.sh).
"""
import os

import docker

# Build context = the folder containing this script (works from any working directory)
HERE = os.path.dirname(os.path.abspath(__file__))

# Create a Docker client
client = docker.from_env()

# Build the Docker image
print("Building image from Dockerfile...")
image, logs = client.images.build(path=HERE, tag="flask-apparmor")
for chunk in logs:
    # each chunk is a dict like {"stream": "Step 1/5 : FROM python:3.8-slim\n"}
    line = chunk.get("stream") if isinstance(chunk, dict) else None
    if isinstance(line, str) and line.strip():
        print(f"[INFO] {line.strip()}")

# Run the container with the AppArmor profile
print("\nRunning container with AppArmor profile...\n")
container = client.containers.run(
    "flask-apparmor",
    ports={'5000/tcp': 5000},
    security_opt=["apparmor=my-apparmor-profile"],
    detach=True
)

print(f"Container started: {container.short_id}\n")

# Verify AppArmor profile applied
print("Inspecting container to verify AppArmor profile...\n")
container_info = client.api.inspect_container(str(container.id))
apparmor_profile = container_info['HostConfig']['SecurityOpt']

print(f"AppArmor profile applied: {apparmor_profile}\n")
print(f"Kernel-reported AppArmorProfile: {container_info.get('AppArmorProfile')}\n")

# Stop the container (and remove it so the script can be re-run)
print("Stopping the container...")
container.stop()
container.remove()
