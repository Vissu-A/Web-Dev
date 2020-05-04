# Generated by Django 2.0.7 on 2020-04-30 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Practice', '0020_auto_20200430_2024'),
    ]

    operations = [
        migrations.CreateModel(
            name='People',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_name', models.CharField(max_length=30)),
                ('l_name', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name': 'People Model',
            },
        ),
        migrations.CreateModel(
            name='Mypeople',
            fields=[
            ],
            options={
                'verbose_name': 'Mypeople model',
                'proxy': True,
                'indexes': [],
            },
            bases=('Practice.people',),
        ),
    ]
