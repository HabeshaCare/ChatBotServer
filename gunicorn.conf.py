wsgi_app = "main:app"
workers = 1
worker_class = "gevent"
timeout = 1200
graceful_timeout = 30
errorlog = "-"  # Print errors to stdout
