from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# NAPISAC WYJĄTEK TASK FOR STUDENT ALREADY EXISTS

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return self.user.username


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return self.user.username


class TaskCategory(models.Model):
    name = models.CharField("category_name", max_length=100, unique=True)



class Task(models.Model):
    author = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_task_set')
    name = models.CharField("task_name", max_length=100, unique=True)
    category = models.ForeignKey(TaskCategory, on_delete=models.CASCADE, related_name='task_in_category')
    task_content = models.CharField('task_content', max_length=500)
    max_points = models.PositiveSmallIntegerField(default=10)

    def get_content(self):
        return self.task_content

    def get_author(self):
        return self.author.__str__()


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='children_set')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='student_set')
    lesson_price = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.user.username

    def return_parent(self):
        return self.parent.__str__()

    def return_teacher(self):
        return self.teacher.__str__()


class StudentTask(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='my_tasks')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='student_assigned_to_task')
    text_answer = models.TextField('Answer', blank=True, default=None)  # tu byl charfield
    score = models.IntegerField(default=(-1))
    file_answer = models.ImageField(upload_to='img_solution',blank=True, null=True)

    def __str__(self):
        return self.text_answer

    # dodaj dekorator
    def set_task(self, task_name):
        t = Task.objects.get(name=task_name)
        self.task = t

    def make_answer(self, text):
        self.text_answer = text

    # dodaj dekorator teacher required
    def set_score(self, grade):
        self.score = grade


class Groups(models.Model):
    name = models.CharField("group_name", max_length=100, unique=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_groups')


class GroupInfo(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='student_group')
    group_id = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name="group_members")


class Lesson(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_lessons')
    date = models.DateField(verbose_name="lesson_date")
    time = models.TimeField(verbose_name="lesson_time")
    payment_status = models.BooleanField(default=False)


class GroupLesson(models.Model):
    group_id = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name="group_lessons")
    date = models.DateField(verbose_name="lesson_date")
    time = models.TimeField(verbose_name="lesson_time")


class GroupLessonPayment(models.Model):
    group_lesson = models.ForeignKey(GroupLesson, on_delete=models.CASCADE, related_name='who_paid')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='my_payments')
    payment_data = models.DateField()


class Post(models.Model):
    author = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255, default="")
    content = models.TextField()
    timestamp = models.DateTimeField()
