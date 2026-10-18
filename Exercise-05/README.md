# Exercise-05 — Docker Security with AppArmor and Python

**Reference:** `Exercises/5-Docker-Security-AppArmor.md`

## Objective
Secure a containerised Flask app with an AppArmor profile, apply it with the Docker CLI and
the **Docker SDK for Python**, and verify restricted actions are blocked.

## Requirements / Tasks
- Prerequisite: `sudo apt-get install apparmor-utils`
1. Flask app (`app.py`, port 5000)
2. `Dockerfile` (python:3.8-slim) → image `flask-apparmor`
3. AppArmor profile `my-apparmor-profile` in `/etc/apparmor.d/`: deny `/etc/**` read,
   `/var/**` rw, exec in `/bin` & `/usr/bin`, deny `sys_admin`; allow `/app/**`, inet stream,
   `net_bind_service`. Load with `apparmor_parser -r`, run with `--security-opt`.
4. `apply_apparmor.py` — build, run with profile, inspect `HostConfig.SecurityOpt`, stop
5. `test_restricted_actions.py` — try `cat /etc/passwd` and `/bin/bash`
6. Answer the 5 questions

## Files
| File | Purpose |
|------|---------|
| `app.py`, `Dockerfile` | App + image |
| `apparmor/my-apparmor-profile` | Profile (copy to `/etc/apparmor.d/`) |
| `scripts/load_profile.sh` | Install utils, load profile, run container |
| `apply_apparmor.py` | Task 4 (Docker SDK) |
| `test_restricted_actions.py` | Task 5 |
| `tests/test_exercise05.py` | Offline checks (app, profile rules, script syntax) |

## How to run (Linux host with AppArmor; working directory: `Exercise-05/`)
```bash
sudo apt-get update && sudo apt-get install apparmor-utils
docker build -t flask-apparmor .
sudo cp apparmor/my-apparmor-profile /etc/apparmor.d/my-apparmor-profile
sudo apparmor_parser -r /etc/apparmor.d/my-apparmor-profile
docker run --security-opt="apparmor=my-apparmor-profile" -p 5000:5000 flask-apparmor

pip install docker
python apply_apparmor.py
python test_restricted_actions.py
```

## Expected output
```
Container started: f8c2a7f9b9b8
AppArmor profile applied: ['apparmor=my-apparmor-profile']
Stopping the container...

Attempt to read /etc/passwd: Exit Code 1 (or 126), Output: ...Permission denied
Attempt to execute /bin/bash: Exit Code 126, Output: ...permission denied
Container stopped
```
Exit codes are non-zero → the actions are blocked. (`/bin/cat` itself lives in a denied
exec path, so 126 is also a valid "blocked" result.)

## Testing
```bash
python -m unittest discover -s Exercise-05/tests -v   # offline, from project root
```

## Answers
1. AppArmor enforces mandatory access-control policies, confining a container to a limited
   set of files, network and capabilities.
2. Profiles define what the app may/may not do: directories, network, exec, capabilities.
3. `/etc` and `/var` hold configuration, user data and logs; blocking them prevents
   reading/modifying sensitive system data.
4. Network access, port binding, executing binaries, writing to paths, `cap_sys_admin` and
   other capabilities, mounts, signals, ptrace.
5. `docker inspect` / Docker SDK → `HostConfig.SecurityOpt` (and `AppArmorProfile`).

## Assumptions / changes
| Change | Reason |
|--------|--------|
| Profile declared as `profile my-apparmor-profile flags=(attach_disconnected,mediate_deleted)` instead of `/usr/bin/python3 {` | Docker looks up the profile **by name**; the original header would make `apparmor=my-apparmor-profile` fail |
| Added baseline `file, capability, signal` allows + `abstractions/base` | A profile with only the original allow-rules blocks Python from reading its own libraries, so the container could not start. All original deny rules still apply (deny wins) |
| Scripts also `remove()` the container | Lets you re-run the scripts without port/name conflicts |
| Dockerfile copies only `app.py` | Keeps host-side scripts out of the image |

> AppArmor is Linux-only. On Windows use WSL2 Ubuntu or a Linux VM; Docker Desktop's VM does
> not let you load custom profiles.
