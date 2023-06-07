from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from users.utils import activate
from .editor_views import *
from . import StudentViews

urlpatterns = [
    path('', views.index, name="index"),
    path('contact/', views.contact, name="contact"),
    path('student/', views.StudentSignUpView.as_view(), name="user_student"),
    path('parent/', views.ParentSignUpView.as_view(), name="user_parent"),
    path('teacher/', views.TeacherSignUpView.as_view(), name="user_teacher"),
    path('principal/', views.PrincipalSignUpView.as_view(), name="user_principal"),
    path('school/', views.SchoolSignUpView.as_view(), name="user_school"),
    path('login/',views.user_login, name="login"),
    path('account/login/',views.user_login, name="login"),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/', views.register, name='register'),
    path('student_report/',views.studentreport, name="student_report"),
    path('reset_password/', auth_views.PasswordResetView.as_view(
                    template_name="registration/password_reset.html"
    ),name="reset_password"),
    path('reset_password_sent',auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),name="pasword_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"),name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"),name="password_reset_complete"),
    path('editor/',views.editor, name="editor"),
    path('editor_index/',views.editor_index, name="editor_index"),
    path('activate/<uidb64>/<token>/',activate, name="activate"),
    path('home/',greetings,name="greetings"),
    path('home/run',runcode,name="runcode"),
    # path('student_profile/',student_home, name="student_dashboard"),
    path('enquiry',views.enquiry, name="enquiry"),
    path('message',views.message, name="message"),
    
    # URSL for Student
    path('student_home/', StudentViews.student_home, name="student_home"),
    path('student_view_attendance/', StudentViews.student_view_attendance, name="student_view_attendance"),
    path('student_view_attendance_post/', StudentViews.student_view_attendance_post, name="student_view_attendance_post"),
    path('student_feedback/', StudentViews.student_feedback, name="student_feedback"),
    path('student_feedback_save/', StudentViews.student_feedback_save, name="student_feedback_save"),
    path('student_profile/', StudentViews.student_profile, name="student_profile"),
    path('student_profile_update/', StudentViews.student_profile_update, name="student_profile_update"),
    path('student_view_result/', StudentViews.student_view_result, name="student_view_result"),
]
