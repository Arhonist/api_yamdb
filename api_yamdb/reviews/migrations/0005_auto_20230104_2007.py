# Generated by Django 3.2 on 2023-01-04 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_alter_review_score'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='review',
            name='review-author',
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('title', 'author'), name='review-author-unique'),
        ),
    ]