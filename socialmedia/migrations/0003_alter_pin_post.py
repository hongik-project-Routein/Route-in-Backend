# Generated by Django 4.2.1 on 2023-06-04 01:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socialmedia', '0002_alter_pin_mapid_alter_story_mapid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pin',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pins', to='socialmedia.post'),
        ),
    ]