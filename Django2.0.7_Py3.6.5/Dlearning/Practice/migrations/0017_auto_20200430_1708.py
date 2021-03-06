# Generated by Django 2.0.7 on 2020-04-30 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Practice', '0016_auto_20200430_1704'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employe',
            options={'ordering': ['-Efname'], 'verbose_name': 'Employe model'},
        ),
        migrations.AlterModelOptions(
            name='onboard',
            options={'verbose_name_plural': 'Onboard model'},
        ),
        migrations.AlterModelOptions(
            name='techgroup',
            options={'ordering': ['Gname'], 'verbose_name': 'Techgroup model'},
        ),
        migrations.AlterOrderWithRespectTo(
            name='onboard',
            order_with_respect_to='emp',
        ),
    ]
