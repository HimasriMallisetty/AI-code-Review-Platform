from rest_framework import serializers
from .models import CodeReview


class CodeReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeReview
        fields = [
            "id", "title", "language", "code_snippet",
            "status", "ai_feedback", "quality_score", "issues_found",
            "created_at", "updated_at",
        ]
        read_only_fields = [
            "status", "ai_feedback", "quality_score", "issues_found",
            "created_at", "updated_at",
        ]


class CodeReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeReview
        fields = ["title", "language", "code_snippet"]
