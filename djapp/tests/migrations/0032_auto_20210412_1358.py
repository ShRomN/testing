# Generated by Django 3.1.5 on 2021-04-12 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0031_auto_20210412_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='informationtestuser',
            name='piq',
            field=models.IntegerField(choices=[(3, 'ПВК III'), (4, 'ПВК IV'), (5, 'ПВК V'), (6, 'ПВК VI'), (7, 'ПВК VII')], db_column='piq', default=0, help_text='Уровень ПВК.', verbose_name='Уровень ПВК:'),
        ),
    ]
