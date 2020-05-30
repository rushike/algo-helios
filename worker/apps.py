from django.apps import AppConfig

class WorkerConfig(AppConfig):
    name = 'worker'
    verbose_name = "Worker Application"
    def ready(self):
        from worker import eventhub