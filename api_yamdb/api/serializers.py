import datetime as dt

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Пожалуйста, придумайте другое имя'
            )
        return data


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


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
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg('score'))['score__avg']


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        current_year = dt.date.today().year
        if value > current_year:
            raise serializers.ValidationError('Некорректный год выхода!')
        return value
