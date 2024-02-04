wsgi_app = "main:app"
bind = "0.0.0.0:5000"
workers = 1
worker_class = "gevent"
timeout = 1200
graceful_timeout = 30
errorlog = "-"  # Print errors to stdout
