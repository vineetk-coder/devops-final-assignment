# Automated Test Results

Generated: 2026-10-17 14:48 by `python scripts/run_all_tests.py`

Python: 3.10.0 | bash: available

**Summary:** 71 PASS, 0 FAIL, 0 SKIP

| Check | Target | Status | Detail |
|---|---|---|---|
| unit tests | Exercise-01 | PASS | Ran 2 tests in 0.004s / OK |
| unit tests | Exercise-02 | PASS | Ran 3 tests in 0.020s / OK |
| unit tests | Exercise-03 | PASS | Ran 7 tests in 0.024s / OK |
| unit tests | Exercise-04 | PASS | Ran 4 tests in 0.015s / OK |
| unit tests | Exercise-05 | PASS | Ran 6 tests in 0.020s / OK |
| unit tests | Exercise-06 | PASS | Ran 6 tests in 5.048s / OK |
| unit tests | Exercise-07 | PASS | Ran 3 tests in 0.001s / OK |
| unit tests | Exercise-08 | PASS | Ran 2 tests in 0.041s / OK |
| unit tests | Exercise-09 | PASS | Ran 3 tests in 0.407s / OK |
| unit tests | Exercise-10 | PASS | Ran 5 tests in 0.310s / OK |
| README | Exercise-01 | PASS |  |
| README | Exercise-02 | PASS |  |
| README | Exercise-03 | PASS |  |
| README | Exercise-04 | PASS |  |
| README | Exercise-05 | PASS |  |
| README | Exercise-06 | PASS |  |
| README | Exercise-07 | PASS |  |
| README | Exercise-08 | PASS |  |
| README | Exercise-09 | PASS |  |
| README | Exercise-10 | PASS |  |
| live HTTP | Exercise-02:app GET / | PASS | Hello from Flask on Kubernetes! |
| live HTTP | Exercise-03:app GET /buy?user=42 | PASS | {"item":"Headphones","served_by_pod":"<hostname>","status":"success","time":"14:48:0 |
| live HTTP | Exercise-03:app GET /health | PASS | {"pod":"<hostname>","status":"healthy"}
 |
| live HTTP | Exercise-04:app GET /about | PASS | {"description":"This is a simple REST API built with Flask.","name":"Simple REST |
| live HTTP | Exercise-05:app GET / | PASS | Hello, this is a secure Flask application running inside a Docker container! |
| live HTTP | Exercise-09/python-flask-app:app GET / | PASS | Hello, Jenkins Multi-Stage Pipeline! |
| live HTTP | Exercise-10:product_catalog GET /products | PASS | [{"id":1,"name":"Laptop","price":1200},{"id":2,"name":"Phone","price":800},{"id" |
| live HTTP | Exercise-10:shopping_cart GET /cart | PASS | []
 |
| live HTTP | Exercise-10:shopping_cart POST /cart | PASS | [{"id":1,"name":"Laptop","quantity":1}]
 |
| pyright (editor) | repository | PASS | 0 errors, 0 warnings, 0 informations |
| bash -n | Exercise-01/scripts/cleanup.sh | PASS |  |
| bash -n | Exercise-01/scripts/run.sh | PASS |  |
| bash -n | Exercise-02/scripts/cleanup.sh | PASS |  |
| bash -n | Exercise-02/scripts/deploy.sh | PASS |  |
| bash -n | Exercise-03/scripts/cleanup.sh | PASS |  |
| bash -n | Exercise-03/scripts/push-image.sh | PASS |  |
| bash -n | Exercise-03/scripts/run.sh | PASS |  |
| bash -n | Exercise-04/scripts/cleanup.sh | PASS |  |
| bash -n | Exercise-04/scripts/run.sh | PASS |  |
| bash -n | Exercise-05/scripts/load_profile.sh | PASS |  |
| bash -n | Exercise-06/scripts/cleanup.sh | PASS |  |
| bash -n | Exercise-06/scripts/run_stack.sh | PASS |  |
| bash -n | Exercise-07/scripts/get-initial-password.sh | PASS |  |
| bash -n | Exercise-07/scripts/start-jenkins.sh | PASS |  |
| bash -n | Exercise-07/scripts/stop-jenkins.sh | PASS |  |
| bash -n | Exercise-08/hello-world.sh | PASS |  |
| bash -n | Exercise-09/scripts/simulate_pipeline.sh | PASS |  |
| bash -n | Exercise-10/scripts/cleanup.sh | PASS |  |
| bash -n | Exercise-10/scripts/curl_tests.sh | PASS |  |
| bash -n | Exercise-10/scripts/run.sh | PASS |  |
| JSON syntax | pyrightconfig.json | PASS |  |
| YAML syntax | Exercise-01/k8s/hello-k8s.yaml | PASS |  |
| YAML syntax | Exercise-02/k8s/flask-deployment-step5.yaml | PASS |  |
| YAML syntax | Exercise-02/k8s/flask-deployment.yaml | PASS |  |
| YAML syntax | Exercise-03/k8s/challenge-flashsale-deployment.yaml | PASS |  |
| YAML syntax | Exercise-03/k8s/flashsale-replicaset.yaml | PASS |  |
| YAML syntax | Exercise-06/delivery_monitoring/alert_rules.yml | PASS |  |
| JSON syntax | Exercise-06/delivery_monitoring/grafana-dashboard.json | PASS |  |
| YAML syntax | Exercise-06/delivery_monitoring/prometheus.yml | PASS |  |
| YAML syntax | Exercise-10/k8s/product_catalog_deployment.yaml | PASS |  |
| YAML syntax | Exercise-10/k8s/product_catalog_service.yaml | PASS |  |
| YAML syntax | Exercise-10/k8s/shopping_cart_deployment.yaml | PASS |  |
| YAML syntax | Exercise-10/k8s/shopping_cart_service.yaml | PASS |  |
| python syntax | 22 files | PASS |  |
| flake8 | 22 files | PASS |  |
| no absolute paths | repository | PASS |  |
| secret scan | repository | PASS |  |
| .env not present | repository | PASS |  |
| .gitignore present | repository | PASS |  |
| reference ZIP present | DevOps-Lab-main.zip | PASS |  |
| ZIP not extracted | repository | PASS |  |
