# Generated by Django 3.1.7 on 2021-04-05 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='ndele.jpeg', height_field='height_field', null=True, upload_to='gallery/', width_field='width_field'),
        ),
    ]