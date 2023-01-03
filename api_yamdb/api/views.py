from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import viewsets

from .serializers import (CommentSerializer, ReviewSerializer)
from reviews.models import Category, Genre, Review, Title


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет ревью. При создании: тайтл из запроса, автор - текущий юзер."""
    serializer_class = ReviewSerializer
    # permission_classes = классы пермишнов ещё не написаны

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, id=self.kwargs['title_id'])
        )

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет коментов. Создание: ревью из запроса, автор - текущий юзер."""
    serializer_class = CommentSerializer
    # permission_classes = классы пермишнов ещё не написаны

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, id=self.kwargs['review_id'])
        )

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        return review.comments.all()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()


class CategoryeViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
