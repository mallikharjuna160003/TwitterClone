# Generated by Django 4.2 on 2024-01-02 21:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tweets', '0004_tweet_likes_tweet_timestamp_tweetlike'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweet',
            name='likes',
        ),
        migrations.AddField(
            model_name='tweet',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='tweet_user', through='tweets.TweetLike', to=settings.AUTH_USER_MODEL),
        ),
    ]