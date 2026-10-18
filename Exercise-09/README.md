# Exercise-09 — Jenkins Multi-Stage Pipeline: Deploying a Python Application

**Reference:** `Exercises/9-Jenkins-Multi-Stage-Pipeline.md`

## Objective
Create and run a Jenkins Pipeline with **Build**, **Test** and **Deploy** stages (plus Run
Application and Test Application) for a Python Flask app.

## Requirements
1. Jenkins running (Exercise-07) with the **Pipeline** plugin
2. `python-flask-app/` with `app.py`, `requirements.txt` (`flask==2.1.2`), `test_app.py`
3. Push to GitHub (`devops-sample-code`)
4. Jenkins → New Item → `Python-MultiStage-Pipeline` → Pipeline
5. `Jenkinsfile` with Build / Test / Deploy / Run Application / Test Application + `post`
6. Pipeline script from SCM → Git → repo URL
7. Build Now and observe stages
8. Fix missing python3/pip inside the Jenkins container (`apt install ...` as root)
- Enhancements: Code Quality (flake8) stage; Docker deploy; notifications

## Files
| File | Purpose |
|------|---------|
| `python-flask-app/app.py` | Flask app |
| `python-flask-app/requirements.txt` | Dependencies |
| `python-flask-app/test_app.py` | Unit test |
| `python-flask-app/Jenkinsfile` | Multi-stage pipeline |
| `scripts/simulate_pipeline.sh` | Runs the same stages locally without Jenkins |
| `tests/test_exercise09.py` | Runs the unit test + validates Jenkinsfile |

## How to run

### Local (working directory: `Exercise-09/python-flask-app/`)
```bash
mkdir python-flask-app && cd python-flask-app   # reference step; folder already provided here
pip install -r requirements.txt
python -m unittest discover -s .
bash ../scripts/simulate_pipeline.sh        # all stages, locally
```

### Additional enhancements (reference, optional)
- **Code Quality (flake8)**: implemented as a pipeline stage.
- **Deploy to a Docker container**: `python-flask-app/Dockerfile` is provided. Optional stage:
  ```groovy
  stage('Docker Deploy') {
      steps {
          dir("${params.APP_DIR}") {
              sh 'docker build -t python-flask-app .'
              sh 'docker rm -f python-flask-app || true'
              sh 'docker run -d --name python-flask-app -p 5000:5000 python-flask-app'
          }
      }
  }
  ```
- **Notifications (email/Slack)**: add `mail to: ...` or `slackSend ...` inside `post { }`.
  Both need Jenkins plugins and credentials configured in the Jenkins UI, so they are not
  hard-coded here.

### Jenkins
1. Prepare the Jenkins container once (Step 8):
   ```bash
   docker exec -it -u root jenkins bash
   apt-get update
   apt install -y python3 python3-pip python3-venv
   exit
   ```
2. Push your code (manual — see project root README for git commands).
3. New Item → `Python-MultiStage-Pipeline` → **Pipeline** → *Pipeline script from SCM* →
   Git → your repo URL → Script Path:
   - `Exercise-09/python-flask-app/Jenkinsfile` if you pushed this whole project
     (default `APP_DIR` works), or
   - `Jenkinsfile` if the repo contains only the app (build with parameter `APP_DIR=.`).
4. **Build Now** (first run registers the parameter; use *Build with Parameters* afterwards).

## Expected output (console, abridged)
```
[Pipeline] { (Build)
Creating virtual environment and installing dependencies...
[Pipeline] { (Test)
+ python3 -m unittest discover -s .
Hello, Jenkins Multi-Stage Pipeline!
Ran 1 test in 0.004s
OK
[Pipeline] { (Deploy)
+ cp .../app.py .../python-app-deploy/
[Pipeline] { (Run Application)
[Pipeline] { (Test Application)
OK
Pipeline completed successfully!
Finished: SUCCESS
```

## Testing
```bash
python -m unittest discover -s Exercise-09/tests -v    # from project root
```

## Assumptions / changes
| Change | Reason |
|--------|--------|
| Build stage really creates a venv and runs `pip install` | Reference echoes this text and its "Expected Outcome" says pip installs Flask; Debian's Python blocks system-wide pip, so a venv is used |
| `APP_DIR` parameter + `dir()` | Works whether the repo is this project or just the app folder; no absolute paths |
| Code Quality (flake8) stage added | Listed under "Additional Enhancements" |
| `JENKINS_NODE_COOKIE=dontKillMe`; old PID killed first | Jenkins otherwise kills background processes when the step ends; re-runs don't clash on port 5000 |
| `Werkzeug==2.1.2` pin | Flask 2.1.2 crashes with Werkzeug 3 |
| Deploy dir = `${WORKSPACE}/python-app-deploy` | As in the reference Jenkinsfile (its prose mentions `/tmp`; the code uses WORKSPACE) |
