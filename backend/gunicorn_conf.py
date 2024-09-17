from multiprocessing import cpu_count

bind = 'unix:/tmp/gunicorn.sock'
workers = cpu_count() + 1
worker_class = 'uvicorn.workers.UvicornWorker'
loglevel = 'info'
accesslog = '/var/log/gunicorn/access.log'
errorlog = '/var/log/gunicorn/error.log'