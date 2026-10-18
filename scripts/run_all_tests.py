"""Run every exercise's tests plus repository-wide checks, and write reports/test_results.md.

Usage (from the project root):
    python -m venv .venv
    .venv/Scripts/activate        # Windows   (Linux/macOS: source .venv/bin/activate)
    pip install -r requirements-dev.txt
    python scripts/run_all_tests.py
"""
import datetime
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXERCISES = sorted(p for p in ROOT.glob("Exercise-*") if p.is_dir())
SKIP_DIRS = {".venv", "venv", ".git", "__pycache__", "python-app-deploy", ".vscode"}

# Child processes (tests, servers) must not leave __pycache__ folders in the project
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True


def project_files():
    for p in ROOT.rglob("*"):
        if p.is_file() and not (set(p.relative_to(ROOT).parts) & SKIP_DIRS) and p.suffix != ".zip":
            yield p


def find_bash():
    git = shutil.which("git")
    if git:
        c = pathlib.Path(git).resolve().parent.parent / "bin" / "bash.exe"
        if c.exists():
            return str(c)
    return shutil.which("bash")


results = []  # (check, target, status, detail)


def record(check, target, ok, detail=""):
    status = "PASS" if ok is True else ("SKIP" if ok is None else "FAIL")
    results.append((check, target, status, detail))
    print(f"[{status}] {check:<22} {target} {detail}")


# 1. Per-exercise unit tests (separate processes so module names like `app` don't clash)
for ex in EXERCISES:
    tests = ex / "tests"
    if not tests.is_dir():
        record("unit tests", ex.name, False, "no tests/ folder")
        continue
    r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", str(tests)],
                       cwd=ex, capture_output=True, text=True)
    summary = [ln for ln in r.stderr.splitlines() if ln.startswith(("Ran ", "OK", "FAILED"))]
    record("unit tests", ex.name, r.returncode == 0, " | ".join(summary))
    if r.returncode != 0:
        print(r.stderr)

# 2. README present in every exercise
for ex in EXERCISES:
    record("README", ex.name, (ex / "README.md").is_file())

# 2b. Live HTTP smoke test: start each Flask app as a real server and call its endpoints
SMOKE = [  # (exercise dir, module, path, expected substring)
    ("Exercise-02", "app", "/", "Hello from Flask on Kubernetes!"),
    ("Exercise-03", "app", "/buy?user=42", '"served_by_pod"'),
    ("Exercise-03", "app", "/health", '"healthy"'),
    ("Exercise-04", "app", "/about", "Simple REST API"),
    ("Exercise-05", "app", "/", "secure Flask application"),
    ("Exercise-09/python-flask-app", "app", "/", "Hello, Jenkins Multi-Stage Pipeline!"),
    ("Exercise-10", "product_catalog", "/products", "Headphones"),
    ("Exercise-10", "shopping_cart", "/cart", "[]"),
]
import socket  # noqa: E402
import time  # noqa: E402
import urllib.request  # noqa: E402

for folder, module, path, expected in SMOKE:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    code = f"import {module} as m; m.app.run(host='127.0.0.1', port={port})"
    proc = subprocess.Popen([sys.executable, "-c", code], cwd=ROOT / folder,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    body, err = "", ""
    try:
        for _ in range(40):
            try:
                body = urllib.request.urlopen(f"http://127.0.0.1:{port}{path}", timeout=2).read().decode()
                break
            except OSError as e:
                err = str(e)
                time.sleep(0.25)
    finally:
        proc.terminate()
        proc.wait(timeout=10)
    shown = (body[:80] or err).replace(socket.gethostname(), "<hostname>")
    record("live HTTP", f"{folder}:{module} GET {path}", expected in body, shown)

# 2c. POST to the shopping cart over real HTTP
with socket.socket() as s:
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
proc = subprocess.Popen([sys.executable, "-c", f"import shopping_cart as m; m.app.run(port={port})"],
                        cwd=ROOT / "Exercise-10", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    time.sleep(2)
    req = urllib.request.Request(f"http://127.0.0.1:{port}/cart", method="POST",
                                 data=b'{"id": 1, "name": "Laptop", "quantity": 1}',
                                 headers={"Content-Type": "application/json"})
    resp = urllib.request.urlopen(req, timeout=5)
    body = resp.read().decode()
    record("live HTTP", "Exercise-10:shopping_cart POST /cart", resp.status == 201 and "Laptop" in body, body[:80])
finally:
    proc.terminate()
    proc.wait(timeout=10)

# 2d. Editor/type check (same engine as VS Code Pylance) — catches "red squiggles"
pyright = shutil.which("pyright", path=str(pathlib.Path(sys.executable).parent))
if pyright:
    r = subprocess.run([pyright], cwd=ROOT, capture_output=True, text=True)
    last = [ln for ln in r.stdout.splitlines() if "error" in ln][-1:] or ["0 errors"]
    record("pyright (editor)", "repository", r.returncode == 0, last[0].strip())
else:
    record("pyright (editor)", "repository", None, "pyright not installed")

# 3. Shell scripts: LF endings + bash -n syntax check
bash = find_bash()
for sh in sorted(ROOT.glob("Exercise-*/**/*.sh")):
    rel = sh.relative_to(ROOT).as_posix()
    if b"\r\n" in sh.read_bytes():
        record("shell LF", rel, False, "CRLF line endings")
        continue
    if bash:
        r = subprocess.run([bash, "-n", sh.name], cwd=sh.parent, capture_output=True, text=True)
        record("bash -n", rel, r.returncode == 0, r.stderr.strip())
    else:
        record("bash -n", rel, None, "bash not found")

# 4. YAML / JSON syntax
for f in project_files():
    rel = f.relative_to(ROOT).as_posix()
    try:
        if f.suffix in (".yml", ".yaml"):
            list(yaml.safe_load_all(f.read_text(encoding="utf-8")))
            record("YAML syntax", rel, True)
        elif f.suffix == ".json":
            json.loads(f.read_text(encoding="utf-8"))
            record("JSON syntax", rel, True)
    except Exception as e:  # noqa: BLE001
        record("YAML/JSON syntax", rel, False, str(e))

# 5. Python syntax + flake8 for all project python files
py_files = [str(f) for f in project_files() if f.suffix == ".py"]
syntax_errors = []
for f in py_files:
    try:  # compile in memory only: no .pyc files are written
        compile(pathlib.Path(f).read_text(encoding="utf-8"), f, "exec")
    except SyntaxError as e:
        syntax_errors.append(f"{pathlib.Path(f).relative_to(ROOT).as_posix()}:{e.lineno} {e.msg}")
record("python syntax", f"{len(py_files)} files", not syntax_errors, "; ".join(syntax_errors))
if shutil.which("flake8") or subprocess.run([sys.executable, "-m", "flake8", "--version"],
                                            capture_output=True).returncode == 0:
    r = subprocess.run([sys.executable, "-m", "flake8", "--max-line-length=120", *py_files],
                       capture_output=True, text=True)
    record("flake8", f"{len(py_files)} files", r.returncode == 0, r.stdout.strip()[:500])

# 6. No absolute / personal paths. The current user's home folder and username are detected
#    at runtime, so no personal value is ever written into this file.
home = pathlib.Path.home()
personal = {re.escape(str(home)), re.escape(home.as_posix()), r"\b" + re.escape(home.name) + r"\b"}
abs_pat = re.compile(r"([A-Za-z]:\\(?:Users|Documents and Settings)\\|/home/[a-z]|/Users/[A-Za-z]|"
                     + "|".join(sorted(personal)) + ")", re.I)
hits = []
for f in project_files():
    if f.suffix in (".png", ".jpg"):
        continue
    m = abs_pat.search(f.read_text(encoding="utf-8", errors="ignore"))
    if m:
        hits.append(f.relative_to(ROOT).as_posix())
record("no absolute paths", "repository", not hits, ", ".join(hits))

# 7. Secret scan
secret_pat = re.compile(
    r"(ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----"
    r"|(password|passwd|secret|token|api_key)\s*[:=]\s*['\"][^'\"<>{}$\s,]{4,}['\"])", re.I)
hits = []
for f in project_files():
    if f.name == "run_all_tests.py":
        continue
    m = secret_pat.search(f.read_text(encoding="utf-8", errors="ignore"))
    if m:
        hits.append(f"{f.relative_to(ROOT).as_posix()}: {m.group(0)[:40]}")
record("secret scan", "repository", not hits, "; ".join(hits))
record(".env not present", "repository", not (ROOT / ".env").exists())
record(".gitignore present", "repository", (ROOT / ".gitignore").is_file())

# 8. Reference ZIP untouched (present, not extracted into repo)
record("reference ZIP present", "DevOps-Lab-main.zip", (ROOT / "DevOps-Lab-main.zip").is_file())
record("ZIP not extracted", "repository", not (ROOT / "DevOps-Lab-main").exists())

# ---- report ----
fails = [r for r in results if r[2] == "FAIL"]
out = ROOT / "reports" / "test_results.md"
out.parent.mkdir(exist_ok=True)
lines = [
    "# Automated Test Results", "",
    f"Generated: {datetime.datetime.now():%Y-%m-%d %H:%M} by `python scripts/run_all_tests.py`", "",
    f"Python: {sys.version.split()[0]} | bash: {'available' if bash else 'not found'}", "",
    f"**Summary:** {sum(r[2] == 'PASS' for r in results)} PASS, {len(fails)} FAIL, "
    f"{sum(r[2] == 'SKIP' for r in results)} SKIP", "",
    "| Check | Target | Status | Detail |", "|---|---|---|---|",
]
lines += [f"| {c} | {t} | {s} | {d.replace('|', '/')[:200]} |" for c, t, s, d in results]
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"\nReport written to {out.relative_to(ROOT).as_posix()}  ({len(fails)} failures)")
sys.exit(1 if fails else 0)
