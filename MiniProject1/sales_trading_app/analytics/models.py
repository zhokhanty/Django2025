from django.db import models

class AnalyticsReport(models.Model):
    name = models.CharField(max_length=100)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)