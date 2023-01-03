from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

v1_router = DefaultRouter() 
v1_router.register('users', views.UserViewSet, basename='user')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]