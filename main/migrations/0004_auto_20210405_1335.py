# Generated by Django 3.1.7 on 2021-04-05 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210405_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='default.jpg', height_field='height_field', null=True, upload_to='gallery', width_field='width_field'),
        ),
    ]
