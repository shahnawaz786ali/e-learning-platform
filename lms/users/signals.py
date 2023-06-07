from django.contrib.auth.signals import user_logged_in,user_logged_out,user_login_failed
from django.db.models.signals import post_save,pre_save
from .models import User,user_profile_student,UserLoginActivity
from django.dispatch import receiver
import datetime as dt
from django.core.cache import cache
from django.core.mail import send_mail

from curriculum import models
import logging

# @receiver(user_logged_in,sender=User)
# def successfull_login(sender,request,user,**kwargs):
#     user=request.user
#     student=User.objects.get(username=user)
#     student_obj = user_profile_student.objects.get(user=student)
#     request.session['last_login']=str(dt.datetime.now())
#     time_in=request.session.get('last_login')
#     print(time_in)
#     ct=cache.get('count', 0, version=student_obj.grade)
#     newcount=ct+1
#     cache.set('count',newcount,60*60*24,version=student_obj.grade)



@receiver(user_logged_out,sender=User)
def succesful_logout(sender,request,user,**kwargs):
    if 'last_logout' in request.session:
        ct_out=request.session.get('last_logout')
    else:
        request.session['last_logout']=str(dt.datetime.now())
        ct_out=request.session.get('last_logout')

    login_time=request.session.get('last_login')
    time_in=dt.datetime.strptime(login_time, '%Y-%m-%d %H:%M:%S.%f')
    time_out=dt.datetime.strptime(ct_out, '%Y-%m-%d %H:%M:%S.%f')

    time_out_minute=time_out.minute
    time_in_minute=time_in.minute
    absent=time_out_minute-time_in_minute

    if absent < 20:
        absent=cache.get('absent', 0,version=user.username)
        new_absent=absent+1
        cache.set('absent', new_absent, 60*60*24, version=user.username)
    else:
        present=cache.get('present', 0, version=user.username)
        new_present=present+1
        cache.set('present',new_present,  60*60*24, version=user.username)        

@receiver(post_save,sender=models.Subject)
def subject_added(sender,instance,created,**kwargs):
    if created:
        # import inspect
        # request=None
        # for fr in inspect.stack():
        #     if fr[3] == 'get_response':
        #         request = fr[0].f_locals['request']
        #         break
        # log_user = request.user
        users=User.objects.all()
        for user in users: 
            if user.is_student:
                send_mail("Subject added on LMS", "New subject added", "manager.lnd@thinnkware.com", [user.email])

@receiver(post_save,sender=models.Subject)
def lesson_added(sender,instance,created,**kwargs):
    if created:
        # import inspect
        # request=None
        # for fr in inspect.stack():
        #     if fr[3] == 'get_response':
        #         request = fr[0].f_locals['request']
        #         break
        # log_user = request.user
        users=User.objects.all()
        for user in users: 
            if user.is_student:
                send_mail("Subject added on LMS", "New lesson added", "manager.lnd@thinnkware.com", [user.email])

error_log = logging.getLogger('error')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@receiver(user_logged_in)
def log_user_logged_in_success(sender, user, request, **kwargs):
    user=request.user
    ct=cache.get('count', 0, version=user.username)
    newcount=ct+1
    cache.set('count',newcount,60*60*24,version=user.username)

    request.session['last_login']=str(dt.datetime.now())
    try:
        user_agent_info = request.META.get('HTTP_USER_AGENT', '<unknown>')[:255],
        login_time=dt.datetime.now()
        login_count=cache.get('count',version=request.user.username)
        user_login_activity_log = UserLoginActivity(login_IP=get_client_ip(request),login_datetime=login_time,login_num=login_count,
                                                    login_username=user.username,
                                                    user_agent_info=user_agent_info,
                                                    status=UserLoginActivity.SUCCESS)
        user_login_activity_log.save()
    except Exception as e:
        # log the error
        error_log.error("log_user_logged_in request: %s, error: %s" % (request, e))


@receiver(user_login_failed)
def log_user_logged_in_failed(sender, credentials, request, **kwargs):
    try:
        user_agent_info = request.META.get('HTTP_USER_AGENT', '<unknown>')[:255],
        user_login_activity_log = UserLoginActivity(login_IP=get_client_ip(request),
                                                    login_username=credentials['username'],
                                                    user_agent_info=user_agent_info,
                                                    status=UserLoginActivity.FAILED)
        user_login_activity_log.save()
    except Exception as e:
        # log the error
        error_log.error("log_user_logged_in request: %s, error: %s" % (request, e))  