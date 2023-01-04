from reviews.models import Category, Comment, Genre, Review, Title
from rest_framework import serializers
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_object_or_404


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализация для Review. Валидирует его уникальность и оценку."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    score = serializers.IntegerField(
        validators=[
            MinValueValidator(1, 'Оценка должна быть >=1'),
            MaxValueValidator(10, 'Оценка должна быть <= 10')
        ]
    )

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title_obj = get_object_or_404(
                Title, id=self.context.get('view').kwargs.get('title_id'))
            user = self.context['request'].user
            if Review.objects.filter(author=user, title=title_obj).count():
                raise serializers.ValidationError('Отзыв этого автора к '
                                                  'этому тайтлу уже есть!')
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'author')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'author')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'
