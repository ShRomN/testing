# Generated by Django 3.1.5 on 2021-01-19 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('tests', '0004_auto_20210114_2002'),
    ]

    operations = [
        migrations.CreateModel(
            name='InformationTestUser',
            fields=[
                ('user_id', models.OneToOneField(db_column='user_id', help_text='Идентификатор пользователя.', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user', verbose_name='Идентификатор пользователя:')),
                ('last_name', models.TextField(db_column='last_name', default='NoLastName', help_text='Фамилия.', max_length=20, verbose_name='Фамилия:')),
                ('first_name', models.TextField(db_column='first_name', default='NoFirstName', help_text='Имя.', max_length=20, verbose_name='Имя:')),
                ('patronymic', models.TextField(db_column='patronymic', default='NoPatronymic', help_text='Отчество.', max_length=20, verbose_name='Отчество:')),
                ('available_tests', models.JSONField(db_column='available_tests', help_text='Список доступных для пользователя тестов и отметка о их прохождении:', verbose_name='Список доступных для пользователя тестов и отметка о их прохождении:')),
            ],
            options={
                'ordering': ['user_id'],
            },
        ),
        migrations.DeleteModel(
            name='AvailableTests',
        ),
        migrations.AddField(
            model_name='kettellanswer',
            name='user_id',
            field=models.IntegerField(db_column='user_id', default=0, help_text='Идентификатор пользователя.', verbose_name='Идентификатор пользователя:'),
        ),
    ]
