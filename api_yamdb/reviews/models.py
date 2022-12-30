from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Comment(models.Model):
    title =  models.ForeignKey(
        'Title', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author =  models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.text[:32]
