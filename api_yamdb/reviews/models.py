from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    genre = models.ManyToManyField(Genre, verbose_name='Жанр')
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True
    )
    year = models.IntegerField(verbose_name='Год релиза')
    description = models.CharField(max_length=200, verbose_name='Описание')

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель ревью к произведению."""
    title = models.ForeignKey(
        'Title', on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField()
    pub_date = models.DateTimeField('Дата добавления', auto_now_add=True)

    def __str__(self):
        return self.text[:32]

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author'), name='review-author-unique'
            ),
        )
        ordering = ['-pub_date']


class Comment(models.Model):
    """Модель коммента к ревью."""
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField('Дата добавления', auto_now_add=True)

    def __str__(self):
        return self.text[:32]

    class Meta:
        ordering = ['-pub_date']
