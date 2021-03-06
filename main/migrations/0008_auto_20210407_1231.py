# Generated by Django 3.1.7 on 2021-04-07 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20210407_1156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='content_rating',
            field=models.FloatField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')]),
        ),
        migrations.AlterField(
            model_name='review',
            name='design_rating',
            field=models.FloatField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')]),
        ),
        migrations.AlterField(
            model_name='review',
            name='usability_rating',
            field=models.FloatField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')]),
        ),
    ]
