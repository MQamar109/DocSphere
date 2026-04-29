# DocSphere/celery.py

import os
from celery import Celery

# tell celery which django settings to use
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DocSphere.settings")

app = Celery("DocSphere")

# pull celery config from settings.py (any key starting with CELERY_)
app.config_from_object("django.conf:settings", namespace="CELERY")

# auto-discover tasks.py in every installed app
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
