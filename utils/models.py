from django.contrib.admin.models import LogEntry as DefaultLogEntry

class LogEntry(DefaultLogEntry):
    class Meta:
        proxy = True
        app_label = 'auth'
        verbose_name = 'Log Entry'
        verbose_name_plural = 'Log Entries'
