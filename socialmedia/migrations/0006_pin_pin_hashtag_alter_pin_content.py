# Generated by Django 4.2.1 on 2023-06-04 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialmedia', '0005_remove_comment_like_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='pin',
            name='pin_hashtag',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='PIN_HASHTAG'),
        ),
        migrations.AlterField(
            model_name='pin',
            name='content',
            field=models.TextField(blank=True, max_length=200, null=True, verbose_name='SUB_CONTENT'),
        ),
    ]
