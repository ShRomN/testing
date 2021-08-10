# Generated by Django 3.1.5 on 2021-01-19 17:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tests', '0007_informationtestuser_available_tests'),
    ]

    operations = [
        migrations.AlterField(
            model_name='informationtestuser',
            name='available_tests',
            field=models.JSONField(db_column='available_tests', default='{}', help_text='Список доступных для пользователя тестов и отметка о их прохождении:', verbose_name='Список доступных для пользователя тестов и отметка о их прохождении:'),
        ),
        migrations.AlterField(
            model_name='informationtestuser',
            name='user_id',
            field=models.OneToOneField(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
