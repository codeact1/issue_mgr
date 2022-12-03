from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

class Status(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()

    def __str__(self):
        return self.name

class Priority(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()

    def __str__(self):
        return self.name

class Issue(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        null=True
    )
    priority = models.ForeignKey(
        Priority,
        on_delete=models.CASCADE,
        null=True
    )
    assigned_to = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title[:500]

    def get_absolute_url(self):
        return reverse('detail', args=[self.id]) 