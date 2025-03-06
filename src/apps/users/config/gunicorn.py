import multiprocessing

# Workers
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000

# Binding
bind = "0.0.0.0:1000"

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Timeout configurations
timeout = 120
keepalive = 65
graceful_timeout = 120

# Restart workers after N requests
max_requests = 1000
max_requests_jitter = 50

# Process naming
proc_name = "users_app"

# Security
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190
