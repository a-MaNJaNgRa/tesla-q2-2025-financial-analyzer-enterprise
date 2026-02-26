cat > Dockerfile << 'EOF'
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

RUN useradd -U -u 1000 appuser && chown -R 1000:1000 /app
USER 1000

CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "--config", "gunicorn.conf.py"]
EOF
