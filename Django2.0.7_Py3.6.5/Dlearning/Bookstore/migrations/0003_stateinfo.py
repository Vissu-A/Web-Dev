# Generated by Django 2.0.7 on 2020-05-13 06:12

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('Bookstore', '0002_cityinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stateinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('population', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'State info',
                'db_table': 'state_information',
                'ordering': ['population'],
            },
            managers=[
                ('modelmanager', django.db.models.manager.Manager()),
            ],
        ),
    ]