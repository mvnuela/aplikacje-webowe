# Generated by Django 4.1.2 on 2022-11-11 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0005_alter_studenttask_text_answer_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(default='', max_length=255),
        ),
    ]