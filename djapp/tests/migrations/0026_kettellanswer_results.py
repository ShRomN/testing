# Generated by Django 3.1.5 on 2021-03-05 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0025_auto_20210304_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='kettellanswer',
            name='results',
            field=models.JSONField(db_column='results', default=dict, help_text='Результаты обработки ответов.', verbose_name='Результаты обработки ответов:'),
        ),
    ]