# Generated by Django 2.0.7 on 2020-04-29 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Practice', '0006_auto_20200429_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='musician',
            name='last_name',
            field=models.CharField(blank=True, max_length=21, null=True),
        ),
    ]
