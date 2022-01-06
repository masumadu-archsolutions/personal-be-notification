from app import init_celery

celery = init_celery()
celery.conf.imports = celery.conf.imports + ("app.tasks.sms_task",)
