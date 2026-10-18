FROM python:3.11-slim
WORKDIR /app
# Reference copied "ex3-flash-sale.py" but started gunicorn with "app:app";
# the file is named app.py so the module name matches (see README "Assumptions").
COPY app.py .
RUN pip install --no-cache-dir flask gunicorn
EXPOSE 5000
CMD ["gunicorn","-b","0.0.0.0:5000","app:app","--workers","1","--threads","2"]
