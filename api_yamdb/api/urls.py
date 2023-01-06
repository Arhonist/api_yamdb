from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

v1_router = DefaultRouter()
v1_router.register('users', views.UserViewSet, basename='user')
v1_router.register('genres',
                   views.GenreViewSet, basename='genre')
v1_router.register('categories',
                   views.CategoryeViewSet, basename='category')
v1_router.register('titles',
                   views.TitleViewSet, basename='title')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews',
                   views.ReviewViewSet, basename='review')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet, basename='comment'
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', views.sign_up, name='register'),
    path('v1/auth/token/', views.get_token, name='token'),
]
