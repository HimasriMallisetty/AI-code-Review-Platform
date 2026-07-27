from django.db import models


class CodeReview(models.Model):
    LANGUAGE_CHOICES = [
        ("python", "Python"),
        ("javascript", "JavaScript"),
        ("java", "Java"),
        ("sql", "SQL"),
        ("other", "Other"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    title = models.CharField(max_length=200, blank=True)
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default="python")
    code_snippet = models.TextField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    ai_feedback = models.TextField(blank=True)
    quality_score = models.PositiveSmallIntegerField(null=True, blank=True)  # 0-100
    issues_found = models.JSONField(default=list, blank=True)  # list of {severity, line, message}

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title or 'Untitled'} ({self.language}) - {self.status}"
