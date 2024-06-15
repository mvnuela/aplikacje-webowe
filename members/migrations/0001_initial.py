# Generated by Django 4.1.2 on 2022-10-18 19:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children_set', to='members.parent')),
            ],
        ),
        migrations.CreateModel(
            name='TaskCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='category_name')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='task_name')),
                ('task_content', models.CharField(max_length=500, verbose_name='task_content')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_task_set', to='members.teacher')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_in_category', to='members.taskcategory')),
            ],
        ),
        migrations.CreateModel(
            name='StudentTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_answer', models.CharField(blank=True, default=None, max_length=255, verbose_name='Answer')),
                ('score', models.IntegerField(default=-1)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_tasks', to='members.student')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_assigned_to_task', to='members.task')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_set', to='members.teacher'),
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]