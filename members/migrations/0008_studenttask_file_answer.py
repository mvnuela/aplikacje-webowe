# Generated by Django 4.1.2 on 2022-11-28 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0007_remove_lesson_teacher_lesson_payment_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studenttask',
            name='file_answer',
            field=models.ImageField(blank=True, null=True, upload_to='img_solution'),
        ),
    ]