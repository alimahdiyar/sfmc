from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from dorm.models import DormUser

def register_view(request):
    template = 'register.html'
    if request.user.is_authenticated and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('index'))

    if request.method == 'POST':
        if User.objects.filter(username=request.POST['national_id'].strip()).exists():
            return render(request, template,
                  {
                      'registration_error': 'ایمیل سرگروه از قبل وجود دارد',
                      'form_data_json': request.POST['form_data_json']
                  })
        with transaction.atomic():
            the_user = User.objects.create_user(
                username=request.POST['national_id'].strip(),
                password=request.POST['password_1'],
            )


            dorm_user = DormUser.objects.create(
                user=the_user,
                name=request.POST['name'].strip(),
                gender=int(request.POST['gender'].strip()),
                national_id=request.POST['national_id'].strip(),
                student_card_image=request.FILES['student_card_image'],
                national_card_image=request.FILES['national_card_image']
            )
            if 'day1' in request.POST:
                if request.POST['day1']:
                    dorm_user.day1=True
            if 'day2' in request.POST:
                if request.POST['day2']:
                    dorm_user.day2=True

            dorm_user.save()

        login(request, the_user)
        return HttpResponseRedirect(reverse('index'))
    return render(request, template,{'registration_error': None})


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    err = False
    if request.method == 'POST':
        try:
            u = User.objects.get(username = request.POST['username'].strip())
        except:
            err = True
        else:
            if u.check_password(request.POST['password']):
                login(request, u)
                return HttpResponseRedirect(reverse('index'))
            else:
                err = True
    return render(request, "login.html", {'err': err})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def index_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dorm:dorm_users'))
    else:
        return HttpResponseRedirect(reverse('register'))
