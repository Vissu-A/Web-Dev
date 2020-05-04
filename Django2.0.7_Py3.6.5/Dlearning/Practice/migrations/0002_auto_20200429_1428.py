# Generated by Django 2.0.7 on 2020-04-29 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Practice', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='person',
            name='first_name',
            field=models.CharField(max_length=21, verbose_name='firstname'),
        ),
        migrations.AlterField(
            model_name='person',
            name='last_name',
            field=models.CharField(max_length=21, verbose_name='lastname'),
        ),
    ]