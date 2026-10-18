# Image for the delivery metrics simulator.
# The reference Jenkinsfile runs `docker build -t delivery_metrics .` but did not supply a
# Dockerfile, so this one is provided.
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt delivery_metrics.py ./
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
# -u = unbuffered so the [DEBUG]/[INFO] lines appear in `docker logs`
CMD ["python", "-u", "delivery_metrics.py"]
