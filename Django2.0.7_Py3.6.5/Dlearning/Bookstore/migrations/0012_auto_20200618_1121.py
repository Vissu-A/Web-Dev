# Generated by Django 2.0.7 on 2020-06-18 05:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bookstore', '0011_auto_20200605_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='pubdate',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 18, 11, 21, 10, 844107), verbose_name='published date'),
        ),
        migrations.AlterField(
            model_name='vichel',
            name='image',
            field=models.ImageField(upload_to='vichel'),
        ),
    ]