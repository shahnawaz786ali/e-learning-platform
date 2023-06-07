from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
import datetime 
from django.contrib.auth.decorators import login_required
from curriculum.models import *
from users.models import *
from curriculum import views
from django.core.cache import cache
from django.contrib.admin.models import LogEntry
import datetime as dt
from .signals import succesful_logout

def student_home(request,subject_id=None):
    user=request.user
    student=User.objects.get(username=user)
    student_obj = user_profile_student.objects.get(user=student)
    
    ct=cache.get('count', version=user.username)
    total_attendance = AttendanceReport.objects.filter(user=student_obj).count()
    attendance_present = AttendanceReport.objects.filter(user=student_obj, status=True).count()
    attendance_absent = AttendanceReport.objects.filter(user=student_obj, status=False).count()

    student_grade = Standard.objects.get(id=student_obj.grade)
    total_subjects = Subject.objects.filter(standard_id=student_grade).count()

    subject_name = []
    data_present = []
    data_absent = []
    subject_data = Subject.objects.filter(standard_id=student_grade)
    for subject in subject_data:
        attendance = Attendance.objects.filter(id=subject.id)
        attendance_present_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=True,user=student_obj).count()
        attendance_absent_count =0
        subject_name.append(subject.name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)

    logs=LogEntry.objects.all()

    for l in logs:
        actionTime=l.action_time
        # print(actionTime)

    # recent_activities=UserLoginActivity.objects.filter(login_username=request.user)
    # print(recent_activities)

    count_absent=cache.get('absent', version=user.username)
    present_count=cache.get('present', version=user.username)

    context={
        "total_attendance": ct,
        "attendance_present": present_count,
        "attendance_absent": count_absent,
        "total_subjects": total_subjects,
        "subject_name": subject_name,
        "data_present": data_present,
        "data_absent": data_absent,
        "profile":student_obj,
        "recent_visit":actionTime
    }
    return render(request, "student_template/student_home_template.html", context)


def student_view_attendance(request):
    student = user_profile_student.objects.get(user=request.user.id) # Getting Logged in Student Data
    course = student.grade # Getting Course Enrolled of LoggedIn Student
    subjects = Subject.objects.filter(standard=course) # Getting the Subjects of Course Enrolled
    print(subjects)
    context = {
        "subjects": subjects
    }
    return render(request, "student_template/student_view_attendance.html", context)


def student_view_attendance_post(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('users:student_view_attendance')
    else:
        # Getting all the Input Data
        subject_id = request.POST.get('subject')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Parsing the date data into Python object
        start_date_parse = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_parse = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        # Getting all the Subject Data based on Selected Subject
        subject_obj = Subject.objects.get(subject_id=subject_id)
        # Getting Logged In User Data
        user_obj = User.objects.get(id=request.user.id)
        # Getting Student Data Based on Logged in Data
        stud_obj = user_profile_student.objects.get(user=user_obj)

        # Now Accessing Attendance Data based on the Range of Date Selected and Subject Selected
        attendance = Attendance.objects.filter(date__range=(start_date_parse, end_date_parse), id=subject_obj.id)
        # Getting Attendance Report based on the attendance details obtained above
        # attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance)

        # for attendance_report in attendance_reports:
        #     print("Date: "+ str(attendance_report.attendance_id.attendance_date), "Status: "+ str(attendance_report.status))

        # messages.success(request, "Attendance View Success")

        context = {
            "subject_obj": subject_obj,
            # "attendance_reports": attendance_reports
        }

        return render(request, 'student_template/student_attendance_data.html', context)


def student_feedback(request):
    student_obj = user_profile_student.objects.get(admin=request.user.id)
    feedback_data = FeedBackStudent.objects.filter(student_id=student_obj)
    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'student_template/student_feedback.html', context)

def student_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('student_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        student_obj = user_profile_student.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackStudent(student_id=student_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('users:student_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('users:student_feedback')


def student_profile(request):
    user = User.objects.get(id=request.user.id)
    student = user_profile_student.objects.get(user=user)

    context={
        "user": user,
        "student": student
    }
    return render(request, 'student_template/student_profile.html', context)


def student_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('users:student_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        middle_name= request.POST.get('middle_name')
        dob= request.POST.get('dob')
        grade= request.POST.get('grade')
        school= request.POST.get('school')
        profile_pic=request.POST.get('profile_pic')

        try:
            customuser = User.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            student = user_profile_student.objects.get(user=customuser.id)
            student.dob=dob
            student.middle_name=middle_name
            student.grade=grade
            student.school=school
            student.profile_pic=profile_pic
            student.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('users:student_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('users:student_profile')

def student_view_result(request):
    student = user_profile_student.objects.get(admin=request.user.id)
    student_result = StudentResult.objects.filter(student_id=student.id)
    context = {
        "student_result": student_result,
    }
    return render(request, "student_template/student_view_result.html", context)