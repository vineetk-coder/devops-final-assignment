"""Exercise-05 Task 5: test restricted actions inside the AppArmor-confined container.

Run from the Exercise-05 folder:  python test_restricted_actions.py
Expect non-zero exit codes (access denied / permission denied).
"""
import docker


def as_text(output):
    """exec_run returns bytes (non-streaming mode); decode it for printing."""
    return output.decode() if isinstance(output, bytes) else str(output)


# Create a Docker client
client = docker.from_env()

# Run the container with the AppArmor profile
container = client.containers.run(
    "flask-apparmor",
    ports={'5000/tcp': 5000},
    security_opt=["apparmor=my-apparmor-profile"],
    detach=True
)
print(f"Container started: {container.short_id}\n")

try:
    # Test restricted actions
    exit_code, output = container.exec_run("cat /etc/passwd")
    print(f"Attempt to read /etc/passwd: Exit Code {exit_code}, Output: {as_text(output)}")

    exit_code, output = container.exec_run("/bin/bash")
    print(f"Attempt to execute /bin/bash: Exit Code {exit_code}, Output: {as_text(output)}")
finally:
    # Stop the container (always, even if a check raised an error)
    container.stop()
    container.remove()
    print("Container stopped")
