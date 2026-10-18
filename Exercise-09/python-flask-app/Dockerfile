# Optional enhancement: run the app in a container (Exercise-09 "Deploy to a Docker container")
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt app.py ./
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
# app.py's __main__ binds to 127.0.0.1; inside a container we must listen on 0.0.0.0
CMD ["python", "-c", "from app import app; app.run(host='0.0.0.0', port=5000)"]
