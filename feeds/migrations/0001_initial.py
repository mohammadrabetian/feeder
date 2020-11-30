# Generated by Django 2.2.11 on 2020-11-27 11:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4)),
                ('url', models.URLField(db_index=True, unique=True, verbose_name='Url')),
                ('title', models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Title')),
                ('subtitle', models.TextField(blank=True, null=True, verbose_name='Subtitle')),
                ('rights', models.CharField(blank=True, max_length=255, null=True, verbose_name='Rights')),
                ('info', models.CharField(blank=True, max_length=255, null=True, verbose_name='Infos')),
                ('language', models.CharField(blank=True, max_length=50, null=True, verbose_name='Language')),
                ('guid', models.CharField(blank=True, db_index=True, max_length=32, null=True, verbose_name='Global Unique Identifier')),
                ('icon_url', models.URLField(blank=True, null=True, verbose_name='Icon URL')),
                ('image_url', models.URLField(blank=True, null=True, verbose_name='Image URL')),
                ('last_modified', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Last modified')),
                ('last_updated', models.DateTimeField(blank=True, null=True, verbose_name='Last updated')),
                ('is_active', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feeds', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Feed',
                'verbose_name_plural': 'Feeds',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='FollowingFeed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='feeds.Feed')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following_feeds', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FeedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=255, verbose_name='Title')),
                ('url', models.URLField(max_length=1000, verbose_name='Url')),
                ('guid', models.CharField(db_index=True, max_length=32, verbose_name='Guid')),
                ('content', models.TextField(verbose_name='Content')),
                ('comments_url', models.URLField(blank=True, null=True, verbose_name='Comments URL')),
                ('date_modified', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Date modified')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='feeds.Feed')),
            ],
            options={
                'verbose_name': 'Feed Item',
                'verbose_name_plural': 'Feed Items',
                'ordering': ('-created_at', '-date_modified'),
            },
        ),
        migrations.AddConstraint(
            model_name='followingfeed',
            constraint=models.UniqueConstraint(fields=('user', 'feed'), name='follow_feed_once'),
        ),
        migrations.AddConstraint(
            model_name='feeditem',
            constraint=models.UniqueConstraint(fields=('feed', 'guid'), name='unique_guid_per_feed'),
        ),
    ]
