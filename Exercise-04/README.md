# Exercise-04 — Docker Networking with Multiple Containers

**Reference:** `Exercises/4-Docker-Networking.md`

## Objective
Understand Docker networking and configure a multi-container application:
Flask web server (container 1), MySQL (container 2), Redis (container 3).

## Requirements / Tasks
1. Create bridge network `my-bridge-net`
2. Verify with `docker network ls`
3. Inspect with `docker network inspect my-bridge-net`
4. Flask app (`/about` on port 5001), `requirements.txt`, `Dockerfile`; build `flask-api`;
   launch `mysql`, `redis`, `flask` on the network (`-p 5001:5001` for flask)
5. `docker exec -it flask bash` → `ping mysql`, `ping redis`
6. Stop/remove containers and remove the network
7. Answer the 4 questions

## Files
| File | Purpose |
|------|---------|
| `app.py` | Flask REST API (`GET /about`) |
| `requirements.txt` | Flask 2.0.1 (+ Werkzeug pin) |
| `Dockerfile` | Image `flask-api` |
| `scripts/run.sh` | Tasks 1–5 |
| `scripts/cleanup.sh` | Task 6 |
| `tests/test_exercise04.py` | API + asset tests |

## How to run (working directory: `Exercise-04/`)
```bash
docker network create --driver bridge my-bridge-net
docker network ls
docker network inspect my-bridge-net
docker build -t flask-api .
docker run -d --name mysql --net=my-bridge-net -e MYSQL_RANDOM_ROOT_PASSWORD=yes mysql:latest
docker run -d --name redis --net=my-bridge-net redis:latest
docker run -d --name flask --net=my-bridge-net -p 5001:5001 flask-api
docker exec -it flask bash
  ping mysql
  ping redis
  exit
curl http://localhost:5001/about
docker stop mysql redis flask && docker rm mysql redis flask
docker network rm my-bridge-net
```
Shortcut: `bash scripts/run.sh` then `bash scripts/cleanup.sh`

## Expected output
```
PING mysql (172.18.0.2) 56(84) bytes of data.
64 bytes from mysql.my-bridge-net (172.18.0.2): icmp_seq=1 ttl=64 time=0.078 ms
PING redis (172.18.0.3) ...
{"description":"This is a simple REST API built with Flask.","name":"Simple REST API","version":"1.0"}
my-bridge-net
```

## Testing
```bash
python -m unittest discover -s Exercise-04/tests -v    # from project root
```

## Answers
1. `--net` specifies the network the container joins.
2. By container name (Docker embedded DNS) or IP on the same network.
3. Bridge = isolated private network ("private room with a door"); host = shares the host's
   network stack ("same room as the host").
4. Use `-p host:container`, e.g. `-p 5001:5001`.

## Assumptions / changes (documented, minimal)
| Change | Reason |
|--------|--------|
| `app.run(host='0.0.0.0', ...)` | Default 127.0.0.1 inside a container is unreachable via `-p` |
| `iputils-ping` installed in image | `python:3.9-slim` has no `ping`; Task 5 needs it |
| `Werkzeug==2.0.3` pin | Flask 2.0.1 crashes with Werkzeug 3 |
| `-e MYSQL_RANDOM_ROOT_PASSWORD=yes` | `mysql:latest` exits without a password option; random avoids any hard-coded secret |
