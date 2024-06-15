import random
import time
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.utils.dateparse import parse_date
from django import template
from typing import List, Any
from django.contrib import messages

from django.contrib.auth import login, logout, update_session_auth_hash, authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.safestring import mark_safe
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_protect

from members.models import *
from random import randint
from django.db.models import Avg, Sum

register = template.Library()


@register.filter(name='required_group')
def required_group(user, group):
    return user.groups.filter(name=group).exists()


@login_required
def home_page(request):
    return render(request, 'teacher/home_page.html')


@login_required
def student_view(request):
    try:
        student = Student.objects.get(user=request.user)
        posts = student.teacher.posts.order_by('-timestamp')
        page_num = request.GET.get('page', 1)
        paginator = Paginator(posts, 2)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
    except:
        page_obj = []
    return render(request, 'student/student.html', {'page_obj': page_obj})


@login_required
def student_done_tasks(request):
    try:
        student = Student.objects.get(user=request.user)
        tasks = student.my_tasks.exclude(text_answer="")
        page_num = request.GET.get('page', 1)
        paginator = Paginator(tasks, 10)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
    except:
        page_obj = []
    return render(request, 'student/student_done_tasks.html', {"page_obj": page_obj})


@login_required
def student_to_do_tasks(request):
    student = Student.objects.get(user=request.user)
    tasks = student.my_tasks.filter(text_answer="")
    # done = student.my_tasks.exclude(text_answer="")
    return render(request, 'student/students_to_do_tasks.html', {"tasks": tasks})


@login_required
def student_lessons(request):
    student = Student.objects.get(user=request.user)
    try:
        gr = GroupInfo.objects.get(student=student)
        lessons = GroupLesson.objects.filter(group_id__group_members__student_id=student.id).order_by('-date')
        page_num = request.GET.get('page', 1)
        paginator = Paginator(lessons, 10)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
    except ObjectDoesNotExist:
        try:
            lessons = student.student_lessons.all()
            page_num = request.GET.get('page', 1)
            paginator = Paginator(lessons, 10)
            try:
                page_obj = paginator.page(page_num)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
        except ObjectDoesNotExist:
            page_obj = []

    return render(request, 'student/student_lessons.html', {'page_obj': page_obj})


def student_incomming_lesson_view(request):
    student = Student.objects.get(user=request.user)
    try:
        gr = GroupInfo.objects.get(student=student)
        lessons = GroupLesson.objects.filter(group_id__group_members__student_id=student.id).order_by('-date')[:6]
    except ObjectDoesNotExist:
        lessons = student.student_lessons.all().order_by('-date')[:6]

    return render(request,'student/student_incomming_lessons.html',{'lessons': lessons})



@login_required
def solve_task_view(request, id):
    studenttask = StudentTask.objects.get(id=id)
    content = studenttask.task.task_content
    return render(request, "student/solvetask.html", {'task_content': content,
                                                      'id': id})


@login_required
def save_task_solution(request, id):
    studenttask = StudentTask.objects.get(id=id)
    x = request.POST.get('content')
    f = request.FILES.get('upload')
    if x is not None and f is not None:
        studenttask.text_answer = x
        studenttask.file_answer = f
    elif x is not None and f is None:
        studenttask.text_answer = x
    elif x is None and f is not None:
        studenttask.file_answer = f
    studenttask.save()
    return redirect('student_view')


# tutaj odrazu wyswietlaja sie posty nauczyciela
@login_required
def teacher_view(request):
    print(request.path)
    try:
        t = Teacher.objects.get(user=request.user)
        posts = t.posts.order_by('-timestamp')
        page_num = request.GET.get('page', 1)
        paginator = Paginator(posts, 2)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
    except:
        page_obj = []
    return render(request, 'teacher/teacher.html', {'page_obj': page_obj})


# żeby nie dodac tej samej lekcji o tej samej godzinie????
@login_required
def add_lesson_view(request):
    individual_students, x = get_individual_and_group_students(request.user.id)
    return render(request, 'teacher/add_lesson.html', {'students': individual_students})


@login_required
def add_lesson(request):
    d = request.POST['l-date']
    print(d)
    t = request.POST['appt']
    print(t)

    s_id = request.POST['student']
    s = Student.objects.get(id=s_id)
    if_lesson=Lesson.objects.filter(student__teacher__user=request.user,date=d, time=t)
    if_group_lesson=GroupLesson.objects.filter(group_id__teacher__user=request.user, date=d, time=t)
    if len(if_lesson)==0 and len(if_group_lesson)==0:
        print("lol")
        lesson = Lesson(student=s, date=d, time=t)
        lesson.save()
    else:
        "lol"
        return redirect('add_lesson_view')
    return redirect('all_teacher_individual_lesson_view')


@login_required
def add_group_lesson_view(request):
    t = Teacher.objects.get(user=request.user)
    groups = t.teacher_groups.all()
    return render(request, 'teacher/add_group_lesson.html', {'groups': groups})


@login_required
def add_group_lesson(request):
    d = request.POST['l-date']
    t = request.POST['appt']
    g_id = request.POST['group']

    if_lesson = Lesson.objects.filter(student__teacher__user=request.user, date=d, time=t)
    if_group_lesson = GroupLesson.objects.filter(group_id__teacher__user=request.user, date=d, time=t)
    if len(if_lesson) ==0 and  len(if_group_lesson)==0:
        lesson = GroupLesson(group_id_id=g_id, date=d, time=t)
        lesson.save()
    else:
        return redirect('add_group_lesson_view')
    return redirect('all_teacher_group_lessons_view')


# edit idiviudal lesson view
@login_required
def edit_lesson_view(request, id, wrong=False):
    today = datetime.today().date()
    time = datetime.today().time()
    return render(request, 'teacher/edit_individual_lesson.html',
                  {'today': today, 'lesson_id': id, 'time': time, 'wrong': wrong})


# edit individual lesson

def edit_lesson(request, id):
    print(id)
    lesson = Lesson.objects.get(id=id)
    dat = request.POST.get('l-date')
    print(dat)
    t = request.POST.get('appt')
    date_obj = datetime.strptime(dat, "%Y-%m-%d").date()
    today = datetime.today().date()
    if date_obj < today:
        return redirect('edit_lesson_view', id, wrong=True)
    else:
        lesson.date = dat
        lesson.time = t
        lesson.save()
        return redirect('all_teacher_individual_lesson_view')


def delete_lesson(request, id):
    lesson = Lesson.objects.get(id=id)
    lesson.delete()
    return redirect('all_teacher_individual_lesson_view')


def edit_group_lesson_view(request, id, wrong=False):
    today = datetime.today().date()
    time = datetime.today().time()
    return render(request, 'teacher/edit_group_lesson.html',
                  {'today': today, 'lesson_id': id, 'time': time, 'wrong': wrong})


def edit_group_lesson(request, id):
    print("editgrouplesson")
    lesson = GroupLesson.objects.get(id=id)
    dat = request.POST.get('l-date')
    t = request.POST.get('l-time')
    date_obj = datetime.strptime(dat, "%Y-%m-%d").date()
    today = datetime.today().date()
    if date_obj < today:
        return redirect('edit_group_lesson_view', id, wrong=True)
    else:
        lesson.date = dat
        lesson.time = t
        lesson.save()
        return redirect('all_teacher_group_lesson_view')


def delete_group_lesson(request, id):
    lesson = GroupLesson.objects.get(id=id)
    lesson.delete()
    return redirect('all_teacher_group_lessons_view')


@login_required
def add_post_view(request):
    return render(request, 'teacher/add_post.html')


@login_required
def add_post(request):
    t = request.POST['post-title']
    c = request.POST['post-content']
    timestamp = datetime.now()
    a = Teacher.objects.get(user=request.user)
    post = Post(title=t, author=a, content=c, timestamp=timestamp)
    post.save()
    return redirect('teacher_view')


@login_required
def create_task(request, mess=None):
    category = TaskCategory.objects.all()
    return render(request, 'teacher/addtask.html', {'categories': category,
                                                    'message': mess})


@login_required
def add_task(request):
    x = request.POST['name']
    y = request.POST['content']
    z = request.POST['category']
    points = request.POST['max-points']
    new_cat=request.POST['new-category']
    teacher = Teacher.objects.get(user=request.user)

    if (str(new_cat)=='') and int(z)==-1:
        print("przyp 1")
        return redirect('create_task')
    elif (str(new_cat)!='') and int(z)!=-1:
        print("przyp2")
        return redirect('create_task')
    elif str(new_cat)!='' and int(z)==-1:
        new_category=TaskCategory(name=new_cat)
        new_category.save()
        task = Task(author=teacher, name=x, task_content=y, category=new_category, max_points=int(points))
        task.save()
    else:
        cat = TaskCategory.objects.get(id=int(z))
        task = Task(author=teacher, name=x, task_content=y, category=cat,max_points=int(points))
        task.save()
    return redirect('teacher_created_task_view')

@login_required
def delete_task(request, id):
    task = Task.objects.get(id=id)
    task.delete()
    return redirect('teacher_view')  # powrot do teacher view


@login_required
def students_assigned_to_task_view(request, id):
    task = Task.objects.get(id=id)
    students = task.student_assigned_to_task.all()
    return render(request, 'teacher/student_assigned_to_task.html', {'students': students,
                                                                     'task_id': id})


@login_required
def task_assesment(request, task, student):
    print(request.path)
    print("task", task)
    print("student", student)
    s = Student.objects.filter(student_group__group_id=2)
    studenttask = StudentTask.objects.get(student_id=student, task_id=task)
    points = [i for i in range (studenttask.task.max_points+1)]

    return render(request, 'teacher/task_assessement.html', {'studentid': student,
                                                             'taskid': task,
                                                             'max_points':points,
                                                             'task_content': studenttask.task.task_content,
                                                             'answer': studenttask.text_answer,
                                                             'file': studenttask.file_answer})


@login_required
def save_grade(request, taskid, studentid):
    x = request.POST['ocena']
    studenttask = StudentTask.objects.get(student=studentid, task=taskid)
    studenttask.set_score(x)
    studenttask.save()

    return redirect('teacher_view')  # redirect do students assigned to task


@login_required
def assign_task(request, id):
    student = Student.objects.get(id=id)
    student_task = student.my_tasks.values()
    ids = []
    for i in student_task:
        ids.append(i['task_id'])
    available_tasks = Task.objects.exclude(id__in=ids)

    return render(request, 'teacher/assigntask.html',
                  {'student': student.user.first_name + " " + student.user.last_name,
                   'tasks': available_tasks,
                   'student_id': id})


@login_required
def assign_task_to_group_view(request, id):
    group = Groups.objects.get(id=id)
    try:
        g = GroupInfo.objects.filter(group_id=id)[0]
        studentzgrupy = Student.objects.get(id=g.student_id)
        student_task = studentzgrupy.my_tasks.values()
        ids = []
        for i in student_task:
            ids.append(i['task_id'])
        available_tasks = Task.objects.exclude(id__in=ids)
    except:
        available_tasks = Task.objects.all()

    return render(request, "teacher/assigntasktogroup.html", {'group_name': group.name,
                                                              'tasks': available_tasks,
                                                              'group_id': id})


@login_required
def confirm_assigning_task_to_group(request, id):
    g = Groups.objects.get(id=id)
    students_in_group = g.group_members.all()
    t_id = request.POST['task_assigned']
    # t_max = Task.objects.get(id=t_id)
    # print(t_max.max_points)
    for s in students_in_group:
        # random_score = randint(1, int(t_max.max_points))
        # time.sleep(3)
        new_task = StudentTask(student=s.student, task_id=t_id, text_answer="")
        new_task.save()
    return redirect('teacher_student_view')


@login_required
def confirm_assigning(request, student_id):
    s = Student.objects.get(id=student_id)
    t_id = request.POST['task_assigned']
    # t_max = Task.objects.get(id=t_id)
    # print("MAX",t_max.max_points)
    # random_score = randint(1, int(t_max.max_points))
    new_task = StudentTask(student=s, task_id=t_id, text_answer="")
    new_task.save()
    return redirect('teacher_student_view')


def get_individual_and_group_students(user_id):
    teacher = Teacher.objects.get(user_id=user_id)
    teacher_students = teacher.student_set.all()
    students_already_assigned_to_group = GroupInfo.objects.filter(student__in=teacher_students).values('student_id')
    ids = []
    for s in students_already_assigned_to_group:
        ids.append(s['student_id'])
    students_without_group = teacher.student_set.exclude(id__in=ids)
    students_with_group = teacher.student_set.filter(id__in=ids)
    return students_without_group, students_with_group


@login_required
def create_students_group_view(request):
    students_without_group, x = get_individual_and_group_students(request.user.id)
    return render(request, 'teacher/create_group.html', {'students': students_without_group})


@login_required
def create_group(request,message=None):
    selected_students = request.POST.getlist('selected_students')
    print(selected_students,"<-selected")
    if (len(selected_students)) < 2:
        return redirect('create_students_group_view')
    group_name = request.POST['group_name']
    teacher = Teacher.objects.get(user=request.user)
    new_group = Groups(name=group_name, teacher=teacher)
    new_group.save()
    new = Groups.objects.get(name=group_name)
    for s in selected_students:
        info = GroupInfo(group_id=new, student_id=s)
        info.save()
    return redirect('teacher_view')


# lista uczniow nauczyciela
@login_required
def teacher_student_view(request):
    students_without_group, students_with_group = get_individual_and_group_students(request.user.id)
    grupy = Groups.objects.all()
    return render(request, 'teacher/students_list.html', {'students': students_without_group,
                                                          'groups': grupy})


@login_required
def teacher_created_task_view(request):
    try:
        t = Teacher.objects.get(user=request.user)
        teacher_tasks = t.teacher_task_set.all()
        page_num = request.GET.get('page', 1)
        paginator = Paginator(teacher_tasks, 10)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
    except:
        page_obj = []
    return render(request, 'teacher/teacher_task.html', {'page_obj': page_obj})


@login_required
def teacher_lessons_view(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
        students = teacher.student_set.all()
        start_date = datetime.today().date()
        end_date = start_date + timedelta(days=7)
        lessons_individual = Lesson.objects.filter(student__in=students, date__range=[start_date, end_date]).order_by(
            '-date')[:8]
        group_lessons = GroupLesson.objects.filter(group_id__teacher=teacher,
                                                   date__range=[start_date, end_date]).order_by('-date')[:8]
    except:
        lessons_individual = []
        group_lessons = []

    return render(request, 'teacher/teacher_lessons.html', {'lessons': lessons_individual,
                                                            'group_lessons': group_lessons})


@login_required
def all_teacher_group_lessons_view(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
        group_lessons = GroupLesson.objects.filter(group_id__teacher=teacher).order_by('-date')
        today = datetime.today().date()
        page_num = request.GET.get('page', 1)
        paginator = Paginator(group_lessons, 20)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
    except:
        page_obj = []
    return render(request, 'teacher/all_teacher_group_lessons.html', {'page_obj': page_obj, 'today': today})


@login_required
def all_teacher_individual_lesson_view(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
        students = teacher.student_set.all()
        lessons_individual = Lesson.objects.filter(student__in=students).order_by('-date')
        page_num = request.GET.get('page', 1)
        today = datetime.today().date()
        paginator = Paginator(lessons_individual, 20)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
    except:
        page_obj = []

    return render(request, 'teacher/all_teacher_individual_lessons.html', {'page_obj': page_obj,
                                                                           'today': today})


@login_required
def parent_view(request):
    parent = Parent.objects.get(user=request.user)
    children = parent.children_set.all()

    return render(request, 'parent/parentview.html', {'children': children})


@login_required
def parent_child_task_view(request, id):
    child = Student.objects.get(id=id)
    child_tasks = child.my_tasks.filter(text_answer="")
    return render(request, 'parent/parent_child_task.html', {"tasks": child_tasks})


def change_password_view(request):
    pass


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/login/")
    return render(request, "logout.html", {})


def group_statistics(request, id):
    group = GroupInfo.objects.filter(group_id_id=id).values('student')
    wyniki = StudentTask.objects.values('task__category__name'). \
                 filter(student__in=group).exclude(score=-1). \
                 annotate(avg_score=Avg('score'))

    avg_values = StudentTask.objects.values('task__category__name'). \
                 filter(student__in=group).exclude(score=-1). \
                 annotate(avg_point=Avg('task__max_points'))
    dict = {}
    for i in avg_values:
        dict[i['task__category__name']] = i['avg_point']
    labels = []
    data = []
    for i in wyniki:
        labels.append(i['task__category__name'])
        result = round((int(i['avg_score']) / int(dict[i['task__category__name']])) * 100)
        data.append(result)
    print(labels)
    print(data)
    return render(request, 'teacher/category_chart.html', {'kategorie': labels, 'dane': data})


def group_ranking(request, id):
    group = GroupInfo.objects.filter(group_id_id=id).values('student')
    wyniki = StudentTask.objects.values('student__user__first_name', 'student__user__last_name'). \
        filter(student__in=group).exclude(score=-1). \
        annotate(sum=Sum('score')).order_by('-sum')
    labels = {}
    for i in wyniki:
        labels[i['student__user__first_name'] + " " + i['student__user__last_name']] = i['sum']
    print("studenci", labels)
    return render(request, 'teacher/group_ranking.html', {'wyniki': labels})


def student_progress(request):
    s = Student.objects.get(user=request.user)
    wyniki = StudentTask.objects.values('task__category__name'). \
        filter(student=s).exclude(score=-1).\
        annotate(sum=Sum('score'))
    print(wyniki)
    max_values = StudentTask.objects.values('task__category__name'). \
        filter(student=s).\
        annotate(sum_point=Sum('task__max_points'))
    print(max_values)
    labels = []
    data = []
    dict = {}
    for i in max_values:
        dict[i['task__category__name']]=i['sum_point']
    for i in wyniki:
        labels.append(i['task__category__name'])
        result = round((int(i['sum'])/int(dict[i['task__category__name']]))*100)
        data.append(result)
    print(labels)
    print(data)
    return render(request, 'teacher/category_chart.html', {'kategorie': labels, 'dane': data})


def child_lesson_parent_view(request, id):
    try:
        student = Student.objects.get(id=id)
        l2 = GroupLesson.objects.filter(group_id__group_members__student_id=student)
        l1 = student.student_lessons.all()
        if len(l1):
            lessons = l1
            is_individual = True
            paid_group_lessons = []

        elif len(l2):
            is_individual = False
            lessons = l2
            paid_group_lessons = GroupLessonPayment.objects.filter(group_lesson__in=l2, student=student).values_list(
                'group_lesson_id', flat=True)

        today = datetime.today().date()
        deadline = today + timedelta(days=2)

        page_num = request.GET.get('page', 1)
        paginator = Paginator(lessons, 10)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
    except:
        page_obj = []
        paid_group_lessons = []
        deadline = []
        is_individual=False
    return render(request, 'parent/parent_child_lesson_view.html', {'page_obj': page_obj, 'deadline': deadline,
                                                                    'is_individual': is_individual,
                                                                    'paid_group_lessons': paid_group_lessons,
                                                                    'student': student})


def child_progress_view(request, id):
    s = Student.objects.get(id=id)
    wyniki = StudentTask.objects.values('task__category__name'). \
        filter(student=s).exclude(score=-1). \
        annotate(sum=Sum('score'))
    print(wyniki)
    max_values = StudentTask.objects.values('task__category__name'). \
        filter(student=s). \
        annotate(sum_point=Sum('task__max_points'))
    print(max_values)
    labels = []
    data = []
    dict = {}
    for i in max_values:
        dict[i['task__category__name']] = i['sum_point']
    for i in wyniki:
        labels.append(i['task__category__name'])
        result = round((int(i['sum']) / int(dict[i['task__category__name']])) * 100)
        data.append(result)
    print(labels)
    print(data)

    all_tasks = StudentTask.objects.filter(student=s).count()
    print("all task", all_tasks)
    done = StudentTask.objects.filter(student=s).exclude(text_answer="").count()
    to_do = all_tasks - done

    labels2 = ['wykonane', 'niewykonane']
    data2 = [done, to_do]

    return render(request, 'parent/parent_child_progress_view.html', {'labels': labels,
                                                                      'data': data,
                                                                      'labels2': labels2,
                                                                      'data2': data2})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) #update hasha sesji zeby nie wylogowalo
            if required_group(user, "Student"):
                return redirect("/login/student/")
            elif required_group(user, "Teacher"):
                return redirect("/login/teacher/")
            else:
                return redirect("/login/parent/")
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user1 = authenticate(request, username=form.request.POST['username'],
                                 password=form.request.POST['password'])
            user = form.get_user()
            if user1.last_login is None:
                print("Jest none")
                login(request, user)
                return redirect('change_password')
            else:
                login(request, user)
                if required_group(user, "Student"):
                    return redirect("/login/student/")
                elif required_group(user, "Teacher"):
                    return redirect("/login/teacher/")
                else:
                    return redirect("/login/parent/")
                return redirect('/')
    else:
        form = AuthenticationForm(request)
    context = {
        "form": form
    }
    return render(request, "login.html", context)


def cancel_lesson(request, id):
    lesson = Lesson.objects.get(id=id)
    st = lesson.student.id
    lesson.delete()
    return redirect('child_lesson_parent_view', id=st)


def mark_lesson_as_paid(request, id):
    lesson = Lesson.objects.get(id=id)
    lesson.payment_status = True
    lesson.save()
    return redirect('all_teacher_individual_lesson_view')


def group_lesson_payment_view(request,id): #group lesson id
    try:
        gr_payment= GroupLessonPayment.objects.filter(group_lesson_id=id).values_list('student_id',flat=True)
        group_members_who_not_paid = GroupInfo.objects.filter(group_id__group_lessons__id=id).exclude(student_id__in=gr_payment).values_list('student_id', flat=True)
        students = Student.objects.filter(id__in=group_members_who_not_paid)
        print(students)
    except ObjectDoesNotExist:
        students=[]
        pass

    return render(request,'teacher/group_payment_list.html',{'students': students,'lesson_id': id})

def mark_group_lesson_as_paid(request, lesson_id, id):
    p = GroupLessonPayment(group_lesson_id=lesson_id,student_id=id,payment_data=datetime.now())
    p.save()
    return redirect('group_lesson_payment_view',id=lesson_id)