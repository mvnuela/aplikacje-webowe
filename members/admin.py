from django.contrib import admin

# Register your models here.
from members.models import Student, StudentTask, Teacher, TaskCategory, Parent, Task, Lesson,GroupLesson,Groups,GroupInfo, GroupLessonPayment, Post
admin.site.register(Student)
admin.site.register(StudentTask)
admin.site.register(Teacher)
admin.site.register(TaskCategory)
admin.site.register(Parent)
admin.site.register(Task)
admin.site.register(Lesson)
admin.site.register(GroupLesson)
admin.site.register(GroupInfo)
admin.site.register(Groups)
admin.site.register(Post)
admin.site.register(GroupLessonPayment)
