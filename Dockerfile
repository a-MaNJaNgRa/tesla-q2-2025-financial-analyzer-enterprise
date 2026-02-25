FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "--config", "gunicorn.conf.py"]