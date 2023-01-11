from api.filters import TitleFilter
from api.mixins import CategoryGenreMixin
from api.permissions import (IsAdmin, IsAdminOrModeratorOrReadOnly,
                             IsAdminOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             SignUpSerializer, TitleCreateSerializer,
                             TitleSerializer, TokenSerializer, UserSerializer)
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title
from users.models import User, UserRole

from api_yamdb.settings import ADMIN_EMAIL


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для расширенной модели пользователя."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (SearchFilter,)
    filterset_fields = ('email',)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        user = request.user
        if request.method == 'GET' and not request.user.role == UserRole.ADMIN:
            return Response(self.get_serializer(user).data)
        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request):
    """Отправляет confirmation code на email корректного юзера."""
    username = request.data.get('username')
    email = request.data.get('email')
    try:
        user = User.objects.get(username=username, email=email)
    except ObjectDoesNotExist:
        user = None
    if User.objects.filter(username=username, email=email).exists():
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Ваш код регистрации',
            f'{confirmation_code}',
            ADMIN_EMAIL,
            [email],
        )
        return Response(status=status.HTTP_200_OK)
    else:
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
        )
        user.save()
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Ваш код регистрации',
            f'{confirmation_code}',
            ADMIN_EMAIL,
            [serializer.data['email']],
        )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    """Возвращает токен, если передан правильный confirmation code."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    if default_token_generator.check_token(
        user,
        serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)
        return Response(
            {'token': f'{token}'},
            status=status.HTTP_200_OK
        )
    return Response(
        {'message': 'К сожалению, пользователь не обнаружен'},
        status=status.HTTP_400_BAD_REQUEST
    )


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет ревью. При создании: тайтл из запроса, автор - текущий юзер."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminOrModeratorOrReadOnly,)

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
    permission_classes = (IsAdminOrModeratorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, id=self.kwargs['review_id'],
                                     title=self.kwargs['title_id'])
        )

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'],
                                   title=self.kwargs['title_id'])
        return review.comments.all()


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет модели тайтлов. Использует два разных сериализатора."""
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleSerializer
        return TitleCreateSerializer


class CategoryViewSet(CategoryGenreMixin):
    """Вьюсет категорий. Небезопасные методы доступны только админу."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreMixin):
    """Вьюсет жанров. Небезопасные методы доступны только админу."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
