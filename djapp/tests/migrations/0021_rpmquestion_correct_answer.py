# Generated by Django 3.1.5 on 2021-02-15 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0020_auto_20210215_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='rpmquestion',
            name='correct_answer',
            field=models.IntegerField(db_column='correct_answer', default=1, help_text='Номер правильного ответа.', verbose_name='Номер правильного ответа:'),
        ),
    ]
