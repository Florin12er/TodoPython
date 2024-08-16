from django.db import models


# Storing Auth0 user ID
class Todo(models.Model):
    task = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.task

    def get_short_description(self):
        return (
            (self.description[:50] + "...")
            if self.description and len(self.description) > 50
            else self.description
        )
