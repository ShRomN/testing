# Generated by Django 3.1.5 on 2021-01-25 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0013_informationtestuser_gender'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='informationtestuser',
            options={'ordering': ['user_id'], 'verbose_name': 'информацию о тестируемом пользователе', 'verbose_name_plural': 'Информация о тестируемых пользователях'},
        ),
        migrations.AlterModelOptions(
            name='kettellanswer',
            options={'ordering': ['-id'], 'verbose_name': 'ответ теста Кеттелла', 'verbose_name_plural': 'Ответы теста Кеттелла'},
        ),
        migrations.AlterModelOptions(
            name='kettellquestion',
            options={'ordering': ['number'], 'verbose_name': 'вопрос теста Кеттелла', 'verbose_name_plural': 'Вопросы теста Кеттелла'},
        ),
        migrations.AlterModelOptions(
            name='mmpianswer',
            options={'ordering': ['-id'], 'verbose_name': 'ответ теста СМИЛ', 'verbose_name_plural': 'Ответы теста СМИЛ'},
        ),
        migrations.AlterModelOptions(
            name='mmpiquestion',
            options={'ordering': ['number'], 'verbose_name': 'вопрос теста СМИЛ', 'verbose_name_plural': 'Вопросы теста СМИЛ'},
        ),
        migrations.AlterModelOptions(
            name='sclanswer',
            options={'ordering': ['-id'], 'verbose_name': 'ответ теста УСК', 'verbose_name_plural': 'Ответы теста УСК'},
        ),
        migrations.AlterModelOptions(
            name='sclquestion',
            options={'ordering': ['number'], 'verbose_name': 'вопрос теста УСК', 'verbose_name_plural': 'Вопросы теста УСК'},
        ),
        migrations.AlterField(
            model_name='informationtestuser',
            name='gender',
            field=models.IntegerField(choices=[(1, 'МУЖСКОЙ'), (2, 'ЖЕНСКИЙ')], db_column='gender', default=1, help_text='Пол пользователя.', verbose_name='Пол пользователя:'),
        ),
        migrations.AlterField(
            model_name='mmpiquestion',
            name='gender',
            field=models.IntegerField(choices=[(1, 'МУЖСКОЙ'), (2, 'ЖЕНСКИЙ')], db_column='gender', help_text='Признак половой принадлежности вопроса.', verbose_name='Признак половой принадлежности вопроса:'),
        ),
    ]