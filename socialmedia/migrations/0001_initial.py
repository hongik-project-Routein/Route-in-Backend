# Generated by Django 4.2.1 on 2023-05-31 00:29

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
            name='Hashtag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='NAME')),
            ],
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='LATITUDE')),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='LONGITUDE')),
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
                ('main_image', models.ImageField(upload_to=socialmedia.models.upload_to_func, verbose_name='MAIN_IMAGE')),
                ('pin_count', models.IntegerField(default=0, verbose_name='PIN_COUNT')),
                ('report_count', models.IntegerField(default=0, verbose_name='REPORT_COUNT')),
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
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='LATITUDE')),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='LONGITUDE')),
                ('image', models.ImageField(upload_to=socialmedia.models.upload_to_func, verbose_name='IMAGE')),
                ('content', models.TextField(blank=True, max_length=200, verbose_name='SUB_CONTENT')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialmedia.post')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('content', models.TextField(blank=True, max_length=200, verbose_name='CONTENT')),
                ('is_reply', models.BooleanField(default=False)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialmedia.post')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
