# Generated by Django 3.1.5 on 2021-02-21 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0023_comanaloganswer_comanalogquestion'),
    ]

    operations = [
        migrations.AddField(
            model_name='comanaloganswer',
            name='report',
            field=models.FileField(blank=True, db_column='report', help_text='DOCX результат обработки ответов.', upload_to='docx/', verbose_name='DOCX результат обработки ответов:'),
        ),
    ]