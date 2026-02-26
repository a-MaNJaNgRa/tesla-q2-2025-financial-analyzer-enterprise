cat > gunicorn.conf.py << 'EOF'
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
bind = "0.0.0.0:8000"
timeout = 180
graceful_timeout = 120
keepalive = 5
EOF
