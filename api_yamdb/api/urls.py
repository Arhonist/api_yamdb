from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TitleViewSet, GenreViewSet, CategoryeViewSet


router_v1 = DefaultRouter()
router_v1.register('titles', TitleViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('categoties', CategoryeViewSet)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
]