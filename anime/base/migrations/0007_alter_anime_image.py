# Generated by Django 4.2.6 on 2023-11-28 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_genre_anime_image_anime_genres'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anime',
            name='image',
            field=models.ImageField(default='avatar.svg', null=True, upload_to=''),
        ),
    ]