# Generated by Django 4.2.1 on 2023-06-04 17:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import socialmedia.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('mapID', models.CharField(blank=True, max_length=30, verbose_name='MAPID')),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='LATITUDE')),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='LONGITUDE')),
                ('image', models.ImageField(upload_to=socialmedia.models.upload_to_func, verbose_name='IMAGE')),
                ('report_count', models.IntegerField(default=0, verbose_name='REPORT_COUNT')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('content', models.TextField(blank=True, max_length=200, verbose_name='CONTENT')),
                ('report_count', models.IntegerField(default=0, verbose_name='REPORT_COUNT')),
                ('bookmark_users', models.ManyToManyField(blank=True, related_name='bookmark_posts', to=settings.AUTH_USER_MODEL)),
                ('like_users', models.ManyToManyField(blank=True, related_name='like_posts', to=settings.AUTH_USER_MODEL)),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mapID', models.CharField(blank=True, max_length=30, verbose_name='MAPID')),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='LATITUDE')),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='LONGITUDE')),
                ('image', models.ImageField(upload_to=socialmedia.models.upload_to_func, verbose_name='IMAGE')),
                ('pin_hashtag', models.CharField(blank=True, max_length=20, null=True, verbose_name='PIN_HASHTAG')),
                ('content', models.TextField(blank=True, max_length=200, null=True, verbose_name='SUB_CONTENT')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pins', to='socialmedia.post')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='NAME')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialmedia.post')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('content', models.TextField(max_length=200, verbose_name='CONTENT')),
                ('like_users', models.ManyToManyField(blank=True, related_name='like_comments', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='socialmedia.post')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
