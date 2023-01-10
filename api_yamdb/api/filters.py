import django_filters as df
from reviews.models import Title


class TitleFilter(df.FilterSet):
    category = df.CharFilter(field_name='category__slug')
    genre = df.CharFilter(field_name='genre__slug')
    name = df.CharFilter(field_name='name')
    year = df.NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']
