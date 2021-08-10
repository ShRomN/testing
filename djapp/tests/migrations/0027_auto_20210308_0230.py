# Generated by Django 3.1.5 on 2021-03-07 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0026_kettellanswer_results'),
    ]

    operations = [
        migrations.AddField(
            model_name='sclanswer',
            name='results',
            field=models.JSONField(db_column='results', default=dict, help_text='Результаты обработки ответов.', verbose_name='Результаты обработки ответов:'),
        ),
        migrations.AddField(
            model_name='sclquestion',
            name='scale_Id',
            field=models.IntegerField(db_column='scale_Id', default=0, help_text='Флаг анализа вопроса по шкале - Id.', verbose_name='Флаг анализа вопроса по шкале - Id:'),
        ),
        migrations.AddField(
            model_name='sclquestion',
            name='scale_Im',
            field=models.IntegerField(db_column='scale_Im', default=0, help_text='Флаг анализа вопроса по шкале - Im.', verbose_name='Флаг анализа вопроса по шкале - Im:'),
        ),
        migrations.AddField(
            model_name='sclquestion',
            name='scale_In',
            field=models.IntegerField(db_column='scale_In', default=0, help_text='Флаг анализа вопроса по шкале - In.', verbose_name='Флаг анализа вопроса по шкале - In:'),
        ),
        migrations.AddField(
            model_name='sclquestion',
            name='scale_Io',
            field=models.IntegerField(db_column='scale_Io', default=0, help_text='Флаг анализа вопроса по шкале - Io.', verbose_name='Флаг анализа вопроса по шкале - Io:'),
        ),
        migrations.AddField(
            model_name='sclquestion',
            name='scale_Ip',
            field=models.IntegerField(db_column='scale_Ip', default=0, help_text='Флаг анализа вопроса по шкале - Ip.', verbose_name='Флаг анализа вопроса по шкале - Ip:'),
        ),
        migrations.AddField(
            model_name='sclquestion',
            name='scale_Is',
            field=models.IntegerField(db_column='scale_Is', default=0, help_text='Флаг анализа вопроса по шкале - Is.', verbose_name='Флаг анализа вопроса по шкале - Is:'),
        ),
        migrations.AddField(
            model_name='sclquestion',
            name='scale_Iz',
            field=models.IntegerField(db_column='scale_Iz', default=0, help_text='Флаг анализа вопроса по шкале - Iz.', verbose_name='Флаг анализа вопроса по шкале - Iz:'),
        ),
    ]
