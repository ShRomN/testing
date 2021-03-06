# Generated by Django 3.1.5 on 2021-01-04 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.TextField(help_text='Имя пользователя.', verbose_name='user_name')),
                ('date', models.DateTimeField(auto_now_add=True, help_text='Дата и время ответов.', verbose_name='date')),
                ('answers', models.JSONField(help_text='Ответы.', verbose_name='answers')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(help_text='Номер вопроса.', verbose_name='number_question')),
                ('question', models.TextField(help_text='Текст вопроса.', verbose_name='text_question')),
                ('answer_1', models.TextField(help_text='Ответ номер - 1.', verbose_name='answer_1')),
                ('answer_2', models.TextField(help_text='Ответ номер - 2.', verbose_name='answer_2')),
                ('answer_3', models.TextField(help_text='Ответ номер - 3.', verbose_name='answer_3')),
            ],
            options={
                'ordering': ['number'],
            },
        ),
    ]
