from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import CodeReview
from .serializers import CodeReviewSerializer, CodeReviewCreateSerializer
from .services.ai_reviewer import review_code, AIReviewError


class CodeReviewViewSet(viewsets.ModelViewSet):
    """
    list:    GET  /api/reviews/
    create:  POST /api/reviews/          -> creates + runs AI review synchronously
    retrieve: GET /api/reviews/{id}/
    """
    queryset = CodeReview.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return CodeReviewCreateSerializer
        return CodeReviewSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = serializer.save(status="pending")

        try:
            result = review_code(review.code_snippet, review.language)
            review.status = "completed"
            review.quality_score = result["quality_score"]
            review.ai_feedback = result["summary"]
            review.issues_found = result["issues"] + [
                {"severity": "suggestion", "line": None, "message": s}
                for s in result["suggestions"]
            ]
        except AIReviewError as exc:
            review.status = "failed"
            review.ai_feedback = str(exc)

        review.save()
        output_serializer = CodeReviewSerializer(review)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def re_review(self, request, pk=None):
        """Re-run the AI review on an existing submission."""
        review = self.get_object()
        try:
            result = review_code(review.code_snippet, review.language)
            review.status = "completed"
            review.quality_score = result["quality_score"]
            review.ai_feedback = result["summary"]
            review.issues_found = result["issues"] + [
                {"severity": "suggestion", "line": None, "message": s}
                for s in result["suggestions"]
            ]
        except AIReviewError as exc:
            review.status = "failed"
            review.ai_feedback = str(exc)

        review.save()
        return Response(CodeReviewSerializer(review).data)
