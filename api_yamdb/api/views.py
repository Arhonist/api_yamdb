from django.shortcuts import render
from Reviews.models import Title, Category, Genre
from rest_framework import viewsets

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()

class CategoryeViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()


