# Gunicorn configuration file
# Para producción en AWS EC2

bind = "0.0.0.0:8000"
workers = 3
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 50

