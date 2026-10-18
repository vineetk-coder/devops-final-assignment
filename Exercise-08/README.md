# Exercise-08 — Creating a "Hello World" Jenkins Job

**Reference:** `Exercises/8-Jenkins-Hello-World-Job.md`

## Objective
Put a `hello-world.sh` script in a GitHub repository and run it from a Jenkins
**Freestyle** job that pulls from Git.

## Requirements
1. Create GitHub repo **devops-sample-code** (public)
2. Create a fine-grained Personal Access Token (used as the password when pushing)
3. Create `hello-world.sh` (`#!/bin/bash` + `echo "Hello, Jenkins!"`), `chmod +x`
4. `git init`, `git add`, `git status`, `git commit -m "Add hello-world.sh"`
5. `git remote add origin ...`, 6. `git push -u origin main`, 7. verify on GitHub
8. Jenkins (from Exercise-07) → New Item `HelloWorld` → Freestyle project
9. Description `Hello World! Jenkins job.`; SCM = Git (your repo URL);
   Build step *Execute shell*: `sh hello-world.sh`
10. Save → Build Now → Console Output shows `Hello, Jenkins!` / `Finished: SUCCESS`

## Files
| File | Purpose |
|------|---------|
| `hello-world.sh` | The script Jenkins runs |
| `tests/test_exercise08.py` | Checks content/LF endings and runs it with bash |

## How to run

### A. Local check (from `Exercise-08/`)
```bash
touch hello-world.sh      # (file already provided; content: #!/bin/bash + echo "Hello, Jenkins!")
chmod +x hello-world.sh
./hello-world.sh          # -> Hello, Jenkins!
```

### B. GitHub steps — **you run these manually** (nothing was pushed by the assistant)
Work in a separate folder for the `devops-sample-code` repo:
```bash
mkdir devops-sample-code && cd devops-sample-code
cp ../<path-to-this-project>/Exercise-08/hello-world.sh .
chmod +x hello-world.sh
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
git init
git add hello-world.sh
git status
git commit -m "Add hello-world.sh"
git branch -M main
git remote add origin https://github.com/<your-GitHub-username>/devops-sample-code.git
git push -u origin main     # username + your PAT when prompted (never store the PAT in files)
```
> Alternatively, push this whole project and point Jenkins at it — then set the build step to
> `sh Exercise-08/hello-world.sh`.

### C. Jenkins job
1. http://localhost:8080 → **New Item** → name `HelloWorld` → **Freestyle project** → OK
2. Description: `Hello World! Jenkins job.`
3. Source Code Management → **Git** → `https://github.com/<your-username>/devops-sample-code.git`
   (branch `*/main`)
4. Build Steps → **Execute shell** → `sh hello-world.sh`
5. **Save** → **Build Now** → Build History `#1` → **Console Output**

## Expected output
```
Started by user Admin
Building in workspace /var/jenkins_home/workspace/HelloWorld
[HelloWorld] $ /bin/sh -xe /tmp/jenkins1281930102.sh
+ echo 'Hello, Jenkins!'
Hello, Jenkins!
Finished: SUCCESS
```

## Testing
```bash
python -m unittest discover -s Exercise-08/tests -v   # from project root
```

## Notes
- `.gitattributes` at the project root forces LF endings on `*.sh` so the script works in
  the Linux Jenkins container even when committed from Windows.
- The PAT is a secret: type it at the prompt or use a credential manager; never commit it.
