from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import login, logout

from competition.models import CompetitionField, Participant, Team, TeamTypeConsts
from django.urls import reverse


# Create your views here.
# testing git

def hello(request):
    return HttpResponse("hello")


def home_view(request):
    template = 'competition/home.html'
    error_message = ""
    if request.user.is_authenticated:
        competition_fields = CompetitionField.objects.all()
        manager = Manager.objects.get(user=request.user)
        participants = Participant.objects.filter(manager=manager)
        teams = Team.objects.filter()
        return render(request, template, {'error_message': error_message, 'competition_fields': competition_fields, })
    else:
        return HttpResponseRedirect(reverse('competition:registeration'))


def registeration_view(request):
    template = 'register.html'
    # if request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse('competition:home'))
    # else:
    valid_team_types = [{'title': team_type[1], 'value': team_type[0]} for team_type in TeamTypeConsts.states]

    if request.method == 'POST':

        with transaction.atomic():
            print(request.POST)
            print(request.FILES)

            # myfile = request.FILES['manager_student_card']
            # fs = FileSystemStorage()
            # filename = fs.save(myfile.name, myfile)
            # uploaded_file_url = fs.url(filename)
            # print(uploaded_file_url)

            manager = Participant.objects.create(
                name=request.POST['manager_name'],
                phone_number=request.POST['manager_phone'],
                email=request.POST['manager_email'],
                university=request.POST['manager_university'],
                student_card_image = request.FILES['manager_student_card']
            )
            # manager.save()
            if(request.POST['team_type'] == TeamTypeConsts.TYPE_1):
                pass
            elif(request.POST['team_type'] == TeamTypeConsts.TYPE_2):
                pass
            elif(request.POST['team_type'] == TeamTypeConsts.TYPE_3):
                pass
                # Team.objects.create(
                #     team_type=request.POST['team_type']
                # )
            else:
                raise Http404
        # form = RegisterationForm(request.POST)
        # if form.is_valid():
        #     if User.objects.filter(username=form.cleaned_data['email']).exists():
        #         return render(request, template, {
        #             'form': form,
        #             'error_message': 'شما قبلا ثبت نام کرده اید'
        #         })
        #     else:
        #         # Create the user:
        #         # Create participant
        #         user = User.objects.create_user(
        #             username=form.cleaned_data['email'],
        #             password=form.cleaned_data['password'],
        #         )
        #         user.save()
        #         manager = Manager(
        #             user=user,
        #             first_name=form.cleaned_data['first_name'],
        #             last_name=form.cleaned_data['last_name'],
        #             phone_number=form.cleaned_data['phone_number'],
        #             email=form.cleaned_data['email'],
        #             student_card_image=form.cleaned_data['student_card_image'],
        #             university=form.cleaned_data['university']
        #         )
        #         manager.save()
        #         participant = Participant(
        #             manager=manager,
        #             first_name=form.cleaned_data['first_name'],
        #             last_name=form.cleaned_data['last_name'],
        #             phone_number=form.cleaned_data['phone_number'],
        #             email=form.cleaned_data['email'],
        #             student_card_image=form.cleaned_data['student_card_image'],
        #             university=form.cleaned_data['university']
        #         )
        #         participant.save()
        #         login(request, user)
        #         return HttpResponseRedirect(reverse('competition:home'))
    # else:
    #     form = RegisterationForm()

    # valid_entry = [entry_year_show(x) for x in range(14)]
    return render(request, template, {'competition_fields': CompetitionField.objects.all(), 'valid_team_types': valid_team_types})


# def login_view(request):
#     template = 'competition/login.html'
#     if request.user.is_authenticated:
#         return HttpResponseRedirect(reverse('competition:home'))
#     else:
#         form = LoginForm(request.POST)
#         if request.method == 'POST':
#             if form.is_valid():
#                 if User.objects.filter(username=form.cleaned_data['username']).exists():
#                     user = User.objects.get(username=form.cleaned_data['username'])
#                     if user.check_password(form.cleaned_data['password']):
#                         login(request, user)
#                         return HttpResponseRedirect(reverse('competition:home'))

#                 return render(request, template, {
#                     'form': form,
#                     'error_message': 'اطلاعات ورودی شما صحیح نمی باشد'
#                 })
#         else:
#             form = LoginForm()
#         return render(request, template, {'form': form})
