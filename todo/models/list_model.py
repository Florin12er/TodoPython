from django.db import models


class List(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name
