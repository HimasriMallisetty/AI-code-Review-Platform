from django.contrib import admin
from .models import CodeReview


@admin.register(CodeReview)
class CodeReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "language", "status", "quality_score", "created_at")
    list_filter = ("language", "status")
    search_fields = ("title", "code_snippet")
