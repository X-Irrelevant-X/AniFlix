# Generated by Django 4.2.6 on 2023-11-29 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_alter_episode_video_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='video_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]