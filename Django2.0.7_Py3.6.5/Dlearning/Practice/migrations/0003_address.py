# Generated by Django 2.0.7 on 2020-04-29 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Practice', '0002_auto_20200429_1428'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(blank=True, max_length=21, null=True)),
                ('village', models.CharField(max_length=21)),
                ('city', models.CharField(max_length=21)),
                ('mandal', models.CharField(max_length=21)),
                ('dist', models.CharField(max_length=21)),
                ('state', models.CharField(max_length=21)),
                ('pincode', models.IntegerField(max_length=6)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Practice.Person')),
            ],
        ),
    ]
