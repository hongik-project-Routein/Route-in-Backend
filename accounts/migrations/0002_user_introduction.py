# Generated by Django 4.2.1 on 2023-08-13 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='introduction',
            field=models.TextField(blank=True, max_length=200, null=True, verbose_name='INTRODUCTION'),
        ),
    ]