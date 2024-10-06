from django.db import models
from django.utils import timezone

class DataSet(models.Model):
    name = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class DataAnalysisTask(models.Model):
    dataset = models.ForeignKey(DataSet, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='pending')
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    result = models.TextField(blank=True)

    def start_task(self):
        self.status = 'processing'
        self.started_at = timezone.now()
        self.save()

    def complete_task(self, result):
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.result = result
        self.save()

