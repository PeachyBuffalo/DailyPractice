# Gunicorn configuration file
bind = "0.0.0.0:5000"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
keepalive = 5 