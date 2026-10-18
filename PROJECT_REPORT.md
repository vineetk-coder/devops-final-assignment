# PROJECT REPORT: DevOps Lab Exercises (Pre-push Audit)

Audit type: repository hygiene and verification pass before a manual GitHub push.
Nothing has been committed or pushed, and no remote is configured.

## 1. Summary
| Category | Status |
|----------|--------|
| Total exercises in reference ZIP (`Exercises/`) | **10**, all implemented |
| Exercise implementation | PASS |
| Offline testing (unit + live HTTP + lint + editor type-check) | PASS (71/71 checks) |
| Live infrastructure runs (Docker / Minikube / Jenkins / AppArmor) | WARNING: not run, tools not installed on this machine |
| Git repository hygiene | PASS |
| `.gitignore` | PASS |
| Secret / security check | PASS |
| Absolute-path / personal-data check | PASS |
| Generated-file check | PASS |
| Docker / Jenkins / CI files | PASS (static validation) |
| Reference ZIP handling | PASS (unchanged; tracked as reference, see §8) |

## 2. Reference ZIP
`DevOps-Lab-main.zip` was read only. It was never modified, renamed, extracted into the repo or
deleted.

| ZIP folder | Content | Handling |
|---|---|---|
| `Exercises/` (10 `.md`) | Lab exercises | All 10 implemented as `Exercise-01` … `Exercise-10` |
| `Assignments/` | 3 PDFs + 1 md, open-ended graded projects | Not lab exercises, so not implemented (see §10) |
| `Images/`, `Notes/`, `References/`, `Syllabus/` | Supporting material | Background only |

## 3. Exercise-by-exercise status
"Checked" means it was actually verified in this pass. Results come from
`scripts/run_all_tests.py` (see `reports/test_results.md`) and the reference-command
compliance check.

| Exercise | Required files | README | Syntax / config valid | Scripts | Tests | Docker / Jenkins / K8s files | Ref. commands covered* | Status |
|---|---|---|---|---|---|---|---|---|
| 01 Hello Pod | PASS | PASS | PASS (YAML) | PASS (`bash -n`) | PASS 2/2 | PASS (`k8s/hello-k8s.yaml`) | 5/5 | **PASS** |
| 02 Flask on Minikube | PASS | PASS | PASS (py, YAML) | PASS | PASS 3/3 + live HTTP | PASS (Dockerfile, 2 manifests) | 25/28 | **PASS** |
| 03 ReplicaSets | PASS | PASS | PASS | PASS | PASS 7/7 + live HTTP ×2 | PASS (Dockerfile, RS + challenge Deployment) | 12/16 | **PASS** |
| 04 Docker networking | PASS | PASS | PASS | PASS | PASS 4/4 + live HTTP (also with pinned Flask 2.0.1) | PASS (Dockerfile) | 4/4 | **PASS** |
| 05 AppArmor | PASS | PASS | PASS (py, profile rules) | PASS | PASS 6/6 + live HTTP | PASS (Dockerfile, AppArmor profile) | 8/8 | **PASS** |
| 06 Monitoring | PASS | PASS | PASS (py, 2 YAML, JSON dashboard, Jenkinsfile structure) | PASS | PASS 6/6 (metrics server started and scraped) | PASS (Dockerfile, Jenkinsfile, Prometheus, alert rules) | 20/23 | **PASS** |
| 07 Jenkins install | PASS | PASS | n/a | PASS | PASS 3/3 | PASS (Docker run scripts) | 2/3 | **PASS** |
| 08 Hello World job | PASS | PASS | PASS | PASS (executed: `Hello, Jenkins!`) | PASS 2/2 | n/a (Jenkins UI job) | 10/10 | **PASS** |
| 09 Multi-stage pipeline | PASS | PASS | PASS (py, Jenkinsfile structure) | PASS | PASS 3/3 + live HTTP (also with pinned Flask 2.1.2) | PASS (Jenkinsfile, optional Dockerfile) | 1/1 | **PASS** |
| 10 Multi-node | PASS | PASS | PASS (4 YAML) | PASS | PASS 5/5 + live GET/POST | PASS (2 Dockerfiles, 4 manifests) | 17/20 | **PASS** |

\*The remaining uncovered reference "commands" are all intentional. They are author-specific
values (pod name `flask-app-b8cd75b6f-tpdpr`, container ID `d350facb3a26`, ports `36157`,
`35855` and `38975`), sample output lines, a command already present split over several lines,
or reference typos that were corrected and documented (`flask-app-rs` → `flashsale-rs`;
`docker build -t flask-app` → `flashsale:1.0`). Each exercise README documents these.

## 4. Testing status
| Check | Result |
|---|---|
| Unit tests, 10 suites (41 tests) | PASS |
| Live HTTP: every Flask app started as a real server and called (8 GETs + 1 POST) | PASS |
| Pinned dependency stacks (Ex04 Flask 2.0.1, Ex09 Flask 2.1.2), in separate venvs | PASS |
| Python syntax (in-memory compile, 22 files) | PASS |
| flake8 strict (no ignored rules) | PASS |
| Pyright, the engine behind the VS Code editor checks | PASS (0 errors, 0 warnings) |
| `bash -n` on 20 shell scripts + LF line endings | PASS |
| YAML / JSON parse (all files) | PASS |
| Live runs on Docker / Minikube / Jenkins / AppArmor | WARNING: not executed (tools not installed) |

How to reproduce:
```bash
python -m venv .venv
.venv\Scripts\activate          # Linux/macOS: source .venv/bin/activate
pip install -r requirements-dev.txt
python scripts/run_all_tests.py
```

## 5. Git repository hygiene: PASS
- The repo is initialised on branch `main`. It has **no commits** and **no remote**.
- **Why about 87 items show in Source Control:** the repo has no commits yet, so every project
  file appears as a newly added file (`A`). That is normal before a first commit. None of them
  are generated or environment files.

| Class | Count | Items |
|---|---|---|
| 1. Required project files | 86 | `Exercise-01` … `Exercise-10` (77 files), `README.md`, `PROJECT_REPORT.md`, `.gitignore`, `.gitattributes`, `.env.example`, `requirements-dev.txt`, `pyrightconfig.json`, `scripts/run_all_tests.py`, `reports/test_results.md` |
| 2. Generated files that should be ignored | 0 staged | `__pycache__/` and `.pyc` are removed and ignored |
| 3. Environment files | 0 staged | `.venv/` (ignored, kept locally for testing), `.vscode/` (ignored, local editor setting); no `.env` exists |
| 4. Unnecessary files | 0 | none |
| 5. Needs attention | 1 | `DevOps-Lab-main.zip` (15.4 MB): tracked as reference material, see §8 |

Per-folder staged counts: Ex01 5 · Ex02 8 · Ex03 9 · Ex04 7 · Ex05 8 · Ex06 11 · Ex07 5 ·
Ex08 3 · Ex09 8 · Ex10 13 · root and support 10.

## 6. `.gitignore`: PASS
Every required rule is present. Each one was confirmed with `git check-ignore` against a
sample path:
`.venv/ venv/ env/ ENV/ __pycache__/ *.py[cod] .env .env.* .vscode/ .idea/ *.log build/ dist/
*.egg-info/ .DS_Store Thumbs.db`. All of these are ignored, and `!.env.example` is kept
tracked. The existing extra rules were preserved: `*.pem`, `*.key`, `id_rsa*`, `secrets/`,
`initialAdminPassword`, `*.pid`, `nohup.out`, `python-app-deploy/`, `jenkins_home/` and
caches. Only `ENV/` was added.
`.gitattributes` forces LF line endings on `*.sh`, Jenkinsfile, Dockerfile and YAML.

## 7. Security and personal-data checks
| Check | Method | Result |
|---|---|---|
| Passwords, tokens, API keys, private keys | regex scan of all files + `git grep --cached` | PASS. The only match is the scanner's own pattern definition in `run_all_tests.py`, which is not a secret |
| `.env` committed | file check | PASS (none exists; ignored) |
| Hard-coded credentials | review | PASS. MySQL uses `MYSQL_RANDOM_ROOT_PASSWORD`; the Jenkins unlock password is only printed to the terminal; the GitHub PAT is typed at the prompt |
| Absolute Windows paths (drive-letter user folders, Program Files, Desktop folders) | `git grep --cached` on staged content | PASS (0 hits) |
| Local username / home folder | detected at runtime and searched for in staged content | PASS (0 hits). The scanner no longer contains the username literally |
| Machine hostname in reports | masked as `<hostname>` | PASS |

## 8. Reference ZIP handling: PASS (decision recorded)
The project requirements place `DevOps-Lab-main.zip` in the project root and forbid modifying
or deleting it, so it stays in place and is **tracked** as the reference material. It is
15.4 MB, well under GitHub's 100 MB per-file limit.
If you prefer not to publish third-party course material, untrack it **without deleting it**:
`git rm --cached DevOps-Lab-main.zip`, then add `DevOps-Lab-main.zip` to `.gitignore`.

## 9. Docker / Jenkins / CI check
| Item | Static check | Live run |
|---|---|---|
| 8 Dockerfiles (Ex02, 03, 04, 05, 06, 09, 10×2) | PASS: base images and COPY/CMD consistent with the files; tests assert key lines | WARNING: not built (no Docker) |
| Kubernetes manifests (Ex01, 02, 03, 10) | PASS: YAML valid; selectors match labels; Services and Deployments share a namespace | WARNING: not applied (no Minikube) |
| Jenkinsfiles (Ex06, Ex09) | PASS: required stages present, braces balanced, relative paths only | WARNING: not run in Jenkins |
| Prometheus config + alert rules (Ex06) | PASS: YAML valid; expressions and thresholds match the reference | WARNING: Prometheus not run |
| AppArmor profile (Ex05) | PASS: all reference rules present; profile name matches `--security-opt` | WARNING: needs a Linux host |

## 10. Remaining issues / manual attention
| # | Item | Severity |
|---|---|---|
| 1 | Live Docker/Minikube/Jenkins/AppArmor runs not performed here; follow each exercise README on a machine with those tools (WSL2 recommended) | WARNING |
| 2 | Git `user.name` / `user.email` are not configured, so the first commit needs them | WARNING (manual) |
| 3 | Decide whether to keep `DevOps-Lab-main.zip` in the public repo (§8) | WARNING (decision) |
| 4 | `Assignments/` (open-ended graded projects) are not implemented; out of scope for the lab exercises | INFO |

## 11. Reference fixes documented in exercise READMEs
| Exercise | Fix |
|---|---|
| 03 | Dockerfile/module name mismatch; image and ReplicaSet names made consistent |
| 04 | Flask binds to 0.0.0.0; `ping` installed; MySQL random root password; Werkzeug pinned |
| 05 | AppArmor profile named so Docker can find it; baseline allows added, all denies kept |
| 06 | Absolute Jenkinsfile path replaced by a relative parameter; missing Dockerfile added |
| 09 | Real venv + pip build stage; Werkzeug pinned; flake8 stage; optional Docker deploy |
| 10 | Undefined namespace `devops-exercise` changed to `default` |
