from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.login_view, name='login_view'),
    path("login/", views.login_view, name='login_view'),
    path("logout/", views.logout_view, name='logout_view'),
    path("login/student/", views.student_view, name='student_view'),
    path("login/student/taskstodo/", views.student_to_do_tasks, name='student_to_do_tasks'),
    path("login/student/donetasks/", views.student_done_tasks, name='student_done_tasks'),
    path("login/student/lessons/",views.student_incomming_lesson_view,name = 'student_lessons'),

    path("login/student/incomming-lessons/",views.student_incomming_lesson_view,name="student_incomming_lesson_view"),
    path("login/student/progress/",views.student_progress,name="student_progress"),
    path("login/teacher/", views.teacher_view, name='teacher_view'),
    path("login/parent/", views.parent_view, name='parent_view'),
    path("childlessons/<int:id>/",views.child_lesson_parent_view,name="child_lesson_parent_view"),
    path("childtodotasks/<int:id>/",views.parent_child_task_view,name="parent_child_task_view"),
    path("childresults/<int:id>/",views.child_progress_view, name = "child_progress_view"),


    path("login/teacher/addtask/", views.create_task, name='create_task'),
    path("login/teacher/addtask/savetask/", views.add_task, name='add_task'),
    path('login/teacher/addpost/', views.add_post_view, name='add_post_view'),
    path('login/teacher/addpost/savepost/', views.add_post, name='add_post'),
    path('login/teacher/addlesson/', views.add_lesson_view, name='add_lesson_view'),
    path('login/teacher/addlesson/savelesson/', views.add_lesson, name='add_lesson'),

    path('login/teacher/addgrouplesson/', views.add_group_lesson_view, name='add_group_lesson_view'),
    path('login/teacher/addgrouplesson/savegrouplesson/', views.add_group_lesson, name='add_group_lesson'),


    path("login/teacher/lessons/", views.teacher_lessons_view, name='teacher_lessons_view'),
    path("login/teacher/listoftask/", views.teacher_created_task_view, name='teacher_created_task_view'),
    path("login/teacher/deletetask/<int:id>", views.delete_task, name='delete_task'),
    path("statistic/<int:id>/", views.group_statistics,name="group_statistics"),
    path("ranking/<int:id>/", views.group_ranking, name="group_ranking"),

    path("login/teacher/allgrouplessons/", views.all_teacher_group_lessons_view, name='all_teacher_group_lessons_view'),
    path("login/teacher/allindividuallessons/", views.all_teacher_individual_lesson_view, name='all_teacher_individual_lesson_view'),
    path("editlesson/<int:id>/",views.edit_lesson_view,name='edit_lesson_view'),
    path("saveeditedlesson/<int:id>/", views.edit_lesson, name='edit_lesson'),

    path("editgrouplesson/<int:id>/",views.edit_group_lesson_view, name='edit_group_lesson_view'),
    path("saveeditedgrouplesson/<int:id>/", views.edit_group_lesson, name='edit_group_lesson'),

    path("deletegrouplesson/<int:id>",views.delete_group_lesson, name='delete_group_lesson'),
    path("deletelesson/<int:id>", views.delete_lesson, name='delete_lesson'),

    path("login/teacher/listoftask/taskstudents/<int:id>", views.students_assigned_to_task_view,
         name='students_assigned_to_task_view'),

    path("login/teacher/students/", views.teacher_student_view, name='teacher_student_view'),
    path("login/teacher/creategroup/", views.create_students_group_view, name='create_students_group_view'),
    path("login/teacher/creategroup/savegroup/", views.create_group, name='create_group'),
    path("rozwiazanie/<int:task>/<int:student>/", views.task_assesment, name='task_assesment'),
    path("savegrade/<int:taskid>/<int:studentid>/", views.save_grade, name='save_grade'),
    path("assigntask/<int:id>/", views.assign_task, name='assign_task'),
    path("confirmassigning/<int:student_id>/", views.confirm_assigning, name='confirm.assigning'),
    path("assigngrouptask/<int:id>/", views.assign_task_to_group_view, name='assign_task_to_group_view'),
    path("confirmassigningtasktogroup/<int:id>/", views.confirm_assigning_task_to_group,
         name="confirm_assigning_task_to_group"),
    path("solvetask/<int:id>/", views.solve_task_view, name='solve_task_view'),
    path('savesolution/<int:id>/', views.save_task_solution, name='save_task_solution'),
    path('result/<int:id>/', views.parent_child_task_view, name='parent_child_task_view'),
    path('cancellesson/<int:id>/', views.cancel_lesson, name='cancel_lesson'),
    path('lessonpaid/<int:id>/',views.mark_lesson_as_paid,name="mark_lesson_as_paid"),
    path('payment-list/<int:id>/',views.group_lesson_payment_view,name='group_lesson_payment_view'),
    path('payment/<int:id>/<int:lesson_id>/', views.mark_group_lesson_as_paid, name='mark_group_lesson_as_paid'),
    path('change-password/', views.change_password, name='change_password'),


]


