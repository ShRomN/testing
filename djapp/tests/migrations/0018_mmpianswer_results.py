# Generated by Django 3.1.5 on 2021-02-05 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0017_auto_20210204_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='mmpianswer',
            name='results',
            field=models.JSONField(db_column='results', default=dict, help_text='Результаты обработки ответов.', verbose_name='Результаты обработки ответов:'),
        ),
    ]
