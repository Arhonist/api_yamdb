from api.permissions import IsAdminOrReadOnly
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter


class CategoryGenreMixin(mixins.ListModelMixin, mixins.CreateModelMixin,
                         mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Миксин для вьюсетов категорий и жанров."""
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('=name',)
